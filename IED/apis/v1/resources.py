import os
import hashlib

from flask import jsonify, request
from flask import send_from_directory, send_file
from flask import make_response
from flask.views import MethodView

from IED.apis.v1 import api_v1
from IED.extensions import db
from IED.models.resources import ResourceClass,Resource
from IED.utils.PKGenrate import generate_resource_key
from IED.apis.v1.errors import api_abort
from IED.apis.v1.apiException import ParameterException, FileExistedError
from IED.apis.v1.apiResponse import JsonResponse


class IndexAPI(MethodView):

    def get(self):
        return jsonify({"Hello": "World!"})


# Resource query and creation
class ItemsAPI(MethodView):

    def get(self):
        """get the list of Resources. in pages"""
        pass

    def post(self):
        """create new item"""
        # item = Resource()
        file = request.files.get("resource_file", None)
        name = request.form.get("name", None)

        # 生成文件的存储式的名称
        resource_id = generate_resource_key()

        real_url = None

        if file:
            # 获取文件的md5值
            str_fileMd5 = hashlib.md5(file.read()).hexdigest()

            # 生成存储文件夹
            str_realUrlDirectory = os.path.join(os.getcwd(), 'media', 'resource')

            if not os.path.exists(str_realUrlDirectory):
                os.makedirs(str_realUrlDirectory)

            # 生成路径
            save_name = resource_id + ('.' + file.filename.split('.')[-1]) if len(file.filename.split('.')) > 1 else ''
            real_url = os.path.join(str_realUrlDirectory, save_name)

            # 率先提交至数据库，触发md5唯一性判定
            try:
                item = Resource(id=resource_id, name=file.filename if name is None else name, real_url=real_url,
                                resource_url='/media/resource/' + save_name, class_id=1, file_md5=str_fileMd5)
                db.session.add(item)
                db.session.commit()
            except Exception as e:
                # 如果存在数据库唯一性错误，则报错”文件已存在“
                raise FileExistedError()

            file.save(real_url)
        else:
            # 不存在文件，报参数错误
            raise ParameterException()

        response = JsonResponse().get_response()

        return response


class ItemAPI(MethodView):

    def get(self, item_id):
        """get single file by file id"""
        item = Resource.query.get_or_404(item_id)
        res = make_response(send_from_directory(directory=os.path.dirname(item.real_url), filename=os.path.basename(item.real_url), as_attachment=True, attachment_filename=item.name))
        res.headers["Cache-Control"] = "no_store"
        res.headers["max—age"] = 1
        return res


api_v1.add_url_rule('/hello', view_func=IndexAPI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/resource', view_func=ItemsAPI.as_view("items"), methods=['GET', 'POST'])
api_v1.add_url_rule('/item/<string:item_id>', view_func=ItemAPI.as_view('item'), methods=['GET'])
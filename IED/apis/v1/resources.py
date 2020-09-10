import os
import hashlib

from flask import jsonify, request, current_app, url_for
from flask import send_from_directory, send_file
from flask import make_response
from flask.views import MethodView

from IED.apis.v1 import api_v1
from IED.extensions import db
from IED.models.resources import ResourceClass,Resource
from IED.utils.PKGenrate import generate_resource_key
from IED.apis.v1.errors import api_abort
from IED.apis.v1.apiException import ParameterException, FileExistedError, ObjectNotFound
from IED.apis.v1.apiResponse import JsonResponse
from IED.apis.v1.schemas import items_schema


# Resource query and creation
class ItemsAPI(MethodView):

    def get(self):
        """get the list of Resources. in pages"""
        page = request.args.get('page', 1, type=int)
        class_id = request.args.get('class_id', None)

        if not class_id:
            raise ParameterException()

        page_size = current_app.config['RESOURCE_ITEM_PER_PAGE']
        pagination = Resource.query.filter_by(class_id=class_id).order_by("create_timestamp").paginate(page, page_size)
        items = pagination.items
        current = url_for('.items', page=page, class_id=class_id, _external=True)
        prev = None
        if pagination.has_prev:
            prev = url_for('.items', page=page - 1, class_id=class_id, _external=True)
        next = None
        if pagination.has_next:
            next = url_for('.items', page=page + 1, class_id=class_id, _external=True)
        return JsonResponse(
            data=items_schema(items, current, prev, next, pagination, class_id)
        ).get_response()

    def post(self):
        """create new item"""
        # item = Resource()
        file = request.files.get("resource_file", None)
        class_id = request.form.get("class_id", None)

        if not class_id:
            raise ParameterException

        # 生成文件的存储式的名称 Id
        resource_id = generate_resource_key()

        if file:
            # 获取文件的md5值
            file_data = file.read()
            str_fileMd5 = hashlib.md5(file_data).hexdigest()

            # 生成存储文件夹
            str_realUrlDirectory = os.path.join(os.getcwd(), 'media', 'resource')

            if not os.path.exists(str_realUrlDirectory):
                os.makedirs(str_realUrlDirectory)

            # 生成路径
            save_name = resource_id + ('.' + file.filename.split('.')[-1]) if len(file.filename.split('.')) > 1 else ''
            real_url = os.path.join(str_realUrlDirectory, save_name)

            # 率先提交至数据库，触发md5唯一性判定
            try:
                item = Resource(
                    id=resource_id,
                    name=file.filename,
                    real_url=real_url,
                    resource_url='/media/resource/' + save_name,
                    class_id=class_id,
                    file_md5=str_fileMd5,
                    size=len(file_data)
                )
                db.session.add(item)
                db.session.commit()
            except Exception as e:
                # 如果存在数据库唯一性错误，则报错”文件已存在“
                raise FileExistedError()

            # file.save(real_url)
            # 写入文件
            with open(real_url,'wb') as save_file:
                save_file.write(file_data)
        else:
            # 不存在文件，报参数错误
            raise ParameterException()

        response = JsonResponse().get_response()

        return response


class ItemAPI(MethodView):

    def get(self, item_id):
        """get single file by file id"""
        item = Resource.query.get_or_404(item_id)
        res = make_response(
            send_from_directory(
                directory=os.path.dirname(item.real_url),
                filename=os.path.basename(item.real_url),
                as_attachment=True,
                attachment_filename=item.name
            )
        )
        res.headers["Cache-Control"] = "no_store"
        # res.headers["max—age"] = 1
        return res


class ResourceClassAPI(MethodView):

    """get the single class"""
    def get(self):
        pass

    """create a new class"""
    def post(self):
        name = request.form.get('name', None)
        level = request.form.get('level', None)

        if not name or not level:
            raise ParameterException()

        if int(level) == 1:
            parentId = 0

        object_resClass = ResourceClass(name=name, level=level, parentId=parentId)
        db.session.add(object_resClass)
        db.session.commit()

        return JsonResponse().get_response()


class ResourceClassesAPI(MethodView):

    """get the classes by the level and parentId"""
    def get(self):
        pass


api_v1.add_url_rule('/resource', view_func=ItemsAPI.as_view("items"), methods=['GET', 'POST'])
api_v1.add_url_rule('/item/<string:item_id>', view_func=ItemAPI.as_view('item'), methods=['GET'])
import os

from flask import jsonify, request
from flask.views import MethodView

from IED.apis.v1 import api_v1
from IED.extensions import db
from IED.models.resources import ResourceClass,Resource
from IED.utils.PKGenrate import generate_resource_key
from IED.apis.v1.errors import api_abort


class IndexAPI(MethodView):

    def get(self):
        return jsonify({"Hello": "World!"})


# Resource query and creation
class ItemsAPI(MethodView):

    def get(self):
        pass

    def post(self):
        """create new item"""
        # item = Resource()
        file = request.files.get("resource_file", None)
        name = request.form.get("name", None)

        resource_id = generate_resource_key()

        real_url = None
        if file is not None:
            real_url_directory = os.path.join(os.getcwd(), 'media', 'resource')

            if not os.path.exists(real_url_directory):
                os.makedirs(real_url_directory)

            real_url = os.path.join(real_url_directory, resource_id + '.' + file.filename.split('.')[-1])
            file.save(real_url)
        else:
            return api_abort(code=400, message="Miss parameter.")

        item = Resource(id=resource_id, name=file.filename if name is None else name, real_url=real_url,)
        


        response =jsonify({
            'access': True
        })

        return response


class ItemAPI(MethodView):

    def get(self):
        pass


api_v1.add_url_rule('/hello', view_func=IndexAPI.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/resource', view_func=ItemsAPI.as_view("items"), methods=['GET', 'POST'])
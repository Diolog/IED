from flask import jsonify, request
from flask.views import MethodView

from IED.apis.v1 import api_v1


class IndexAPI(MethodView):

    def get(self):
        return jsonify({"Hello": "World!"})


api_v1.add_url_rule('/hello', view_func=IndexAPI.as_view('index'), methods=['GET'])
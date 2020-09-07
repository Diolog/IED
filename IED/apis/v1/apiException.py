import json

from werkzeug.exceptions import HTTPException
from flask import request, jsonify


class APIException(HTTPException):

    code = 500
    msg = "sorry, we made a mismake"
    error_code = 999
    data = ''

    def __init__(self, msg=None, code=None, error_code=None, data=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if data:
            self.data = data

        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            code=self.code,
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param(),
            data=self.data
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]


class ServerError(APIException):
    code = 500
    msg = "server is invallid"
    error_code = 999
    data = '服务器错误'


class ClientTypeError(APIException):
    code = 400
    msg = "client is invallid"
    error_code = 1006
    data = ''


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000
    data = '参数错误'


class AuthFailed(APIException):
    code = 401
    msg = 'invalid parameter'
    error_code = 1001
    data = ''


class ValError(APIException):
    code = 404
    msg = 'invalid parameter'
    error_code = 1001
    data = ''


class FileExistedError(APIException):
    code = 406
    msg = 'existed file'
    error_code = 4006
    data = '文件已存在，无法再次上传'
import json

from flask import jsonify, Response


class JsonResponse():

    code = 200
    msg = "request success"
    solve_code = 20001
    data = ''

    def __init__(self, msg=None, code=None, solve_code=None, data=None):
        if code:
            self.code = code
        if solve_code:
            self.error_code = solve_code
        if msg:
            self.msg = msg
        if data:
            self.data = data

    def get_response(self):
        body = dict(
            code = self.code,
            msg = self.msg,
            solve_code = self.solve_code,
            data = self.data
        )
        response = jsonify(body)
        return response

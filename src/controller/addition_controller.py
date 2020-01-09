
from flask_restplus import Resource
from flask import request

from src.dto import AdditionDto

api = AdditionDto.api
_request = AdditionDto.request
_response = AdditionDto.response


@api.route('/')
class Addition(Resource):
    @api.response(200, 'Successfully Requested', _response)
    @api.response(400, 'Bad Request')
    @api.doc('Addition of wanted numbers.')
    @api.expect(_request, validate=True)
    @api.marshal_with(fields=_response)
    def post(self):

        data = request.json.get('numbers')
        res = 0

        for elem in data:
            res = res + elem.get('number')

        return {
            "result": float(res)
        }

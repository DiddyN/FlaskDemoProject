
from flask_restplus import Resource
from flask import request
from flask_jwt_extended import jwt_required

from src.dto import MultiplicationDto

api = MultiplicationDto.api
_request = MultiplicationDto.request
_response = MultiplicationDto.response


@api.route('/')
class Multiplication(Resource):
    @jwt_required
    @api.response(200, 'Successfully Requested', _response)
    @api.response(400, 'Bad Request')
    @api.doc('Multiplication of wanted numbers')
    @api.expect(_request, validate=True)
    @api.marshal_with(fields=_response)
    def post(self):

        data = request.json.get('numbers')
        res = 1

        for elem in data:
            res = res * elem.get('number')

        return {
            "result": float(res)
        }


from flask import request
from flask_restplus import Resource
from flask_jwt_extended import create_access_token

from src.dto import LoginDto

api = LoginDto.api
_request = LoginDto.request
_response = LoginDto.response


@api.route('/')
class Login(Resource):
    @api.response(200, 'Successfully Requested', _response)
    @api.response(400, 'Bad Request')
    @api.doc('User login.')
    @api.expect(_request, validate=True)
    @api.marshal_with(fields=_response)
    def post(self):

        username = request.json.get('username')
        password = request.json.get('password')

        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=username+password)
        return {
            "access_token": access_token
        }

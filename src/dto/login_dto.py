
from flask_restplus import Namespace, fields


class LoginDto:
    api = Namespace('login', description='User login.')

    request = api.model('login-request',
                        {
                            'username': fields.String(required=True, description='Username', example='DiddyN'),
                            'password': fields.String(required=True, description='Password', example='Didi123!')
                        })

    response = api.model('login-response', {
        'access_token': fields.String(description='Access token used for auth.')
    })

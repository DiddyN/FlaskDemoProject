
from flask_restplus import Namespace, fields


class UserInfoDto:
    api = Namespace('api/userInfo', description='Info about user.')

    request = api.model('userInfo-request',
                        {
                            'username': fields.String(description='Name of user.', example='DiddyN'),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('userInfo-response', {
        'status': fields.String(description='shows if opp was successfully accomplished'),
        'username': fields.String(description='Name of user.'),
        'password': fields.String(description='Password'),
        'email': fields.String(description='User email.'),
        'date_of_birth': fields.String(description='Date of birth.'),
        'books': fields.String(description="Books user loaned")
    })


from flask_restplus import Namespace, fields


class RegistrationDto:
    api = Namespace('registration', description='Adds user in database.')

    request = api.model('registration-request',
                        {
                            'username': fields.String(description='Name of user.', example='DiddyN'),
                            'password': fields.String(description='Password', example='Didi123!'),
                            'email': fields.String(description='User email.', example='didi@gmail.com'),
                            'date_of_birth': fields.String(description='Date of birth.', example='1.4.1995.')
                        })

    response = api.model('registration-response', {
        'status': fields.String(description='shows if opp was successfully accomplished', example='Success!')
    })


from flask_restplus import Namespace, fields


class UserGetBookDto:
    api = Namespace('api/user/getBook', description='User gets book from library.')

    request = api.model('user-get-book-request',
                        {
                            'username': fields.String(description='Name of user that gets book from library.',
                                                      example='DiddyN'),
                            'title': fields.String(description='Book title.', example='Crime and punishment'),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('user-get-book-response', {
        'status': fields.String(description='shows if opp was successfully accomplished', example='Success!')
    })

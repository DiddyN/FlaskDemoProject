
from flask_restplus import Namespace, fields


class UserReturnBookDto:
    api = Namespace('api/user/returnBook', description='User returns book to library.')

    request = api.model('user-return-book-request',
                        {
                            'username': fields.String(description='Name of user that gets book from library.',
                                                      example='DiddyN'),
                            'title': fields.String(description='Book title.', example='Crime and punishment'),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('user-return-book-response', {
        'status': fields.String(description='shows if opp was successfully accomplished', example='Success!')
    })

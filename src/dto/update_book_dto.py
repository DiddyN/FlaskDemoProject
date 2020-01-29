
from flask_restplus import Namespace, fields


class UpdateBookDto:
    api = Namespace('api/book/update', description='Updates book in database.')

    request = api.model('update-book-request',
                        {
                            'new_title': fields.String(description='Book title.', example='Anna Karenina'),
                            'old_title': fields.String(description='Book title.', example='Crime and punishment'),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('update-book-response', {
        'status': fields.String(description='shows if opp was successfully accomplished', example='Success!')
    })

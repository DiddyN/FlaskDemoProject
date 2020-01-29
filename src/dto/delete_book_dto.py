
from flask_restplus import Namespace, fields


class DeleteBookDto:
    api = Namespace('api/book/delete', description='Deletes book in database.')

    request = api.model('delete-book-request',
                        {
                            'title': fields.String(description='Book title.', example='Crime and punishment'),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('delete-book-response', {
        'status': fields.String(description='shows if opp was successfully accomplished', example='Success!')
    })


from flask_restplus import Namespace, fields


class AddBookDto:
    api = Namespace('api/book/add', description='Adds book in database.')

    request = api.model('add-book-request',
                        {
                            'title': fields.String(description='Book title.', example='Crime and punishment'),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('add-book-response', {
        'status': fields.String(description='shows if opp was successfully accomplished', example='Success!')
    })

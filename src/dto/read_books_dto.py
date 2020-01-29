
from flask_restplus import Namespace, fields


class ReadBookDto:
    api = Namespace('api/book/read', description='Reads books from database.')

    request = api.model('read-book-request',
                        {
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('read-book-response', {
        'books': fields.String(description='shows list of books in database')
    })

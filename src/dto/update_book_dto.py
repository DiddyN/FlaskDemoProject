
from flask_restplus import Namespace, fields


class UpdateBookDto:
    api = Namespace('api/book/update', description='Updates book in database.')

    request = api.model('update-book-request',
                        {
                            'new_title': fields.String(description='New book title.', example='Anna Karenina'),
                            'old_title': fields.String(description='Old book title.', example='Crime and punishment'),
                            'new_year': fields.Integer(description='New edition year', example='1994'),
                            'new_author': fields.String(description='New author(name) of the books.', example='Fyodor Dostoyevsky'),
                            'new_language': fields.String(description='New language in which the book was written.', example='Serbian'),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('update-book-response', {
        'status': fields.String(description='shows if opp was successfully accomplished', example='Success!')
    })

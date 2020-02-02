
from flask_restplus import Namespace, fields


class AddAuthorDto:
    api = Namespace('api/author/add', description='Adds author in database.')

    request = api.model('add-author-request',
                        {
                            'name': fields.String(description='Name of author.', example='Lav Tolstoy'),
                            'date_of_birth': fields.String(description='Date of birth.', example='1.1.1956.'),
                            'nationality': fields.String(description='Author\'s nationality', example='Russian'),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('add-author-response', {
        'status': fields.String(description='shows if opp was successfully accomplished', example='Success!')
    })

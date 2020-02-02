
from flask_restplus import Namespace, fields


class DeleteAuthorDto:
    api = Namespace('api/author/delete', description='Deletes author in database.')

    request = api.model('delete-author-request',
                        {
                            'name': fields.String(description='Name of author.', example='Lav Tolstoy'),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('delete-author-response', {
        'status': fields.String(description='shows if opp was successfully accomplished', example='Success!')
    })

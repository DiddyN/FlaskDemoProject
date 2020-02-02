
from flask_restplus import Namespace, fields


class ReadAuthorDto:
    api = Namespace('api/author/read', description='Reads author from database.')

    request = api.model('read-author-request',
                        {
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('read-author-response', {
        'authors': fields.String(description='shows list of authors in database')
    })

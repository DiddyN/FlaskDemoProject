
from flask_restplus import Namespace, fields


class UpdateAuthorDto:
    api = Namespace('api/author/update', description='Updates author in database.')

    request = api.model('update-author-request',
                        {
                            'new_name': fields.String(description='New author name.', example='Ivo Andric'),
                            'old_name': fields.String(description='Old author name.', example='Lav Tolstoy'),
                            'new_date_of_birth': fields.String(description='New date of birth', example='1965'),
                            'new_nationality': fields.String(description='New nationality of author.', example='Serbian'),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('update-author-response', {
        'status': fields.String(description='shows if opp was successfully accomplished', example='Success!')
    })

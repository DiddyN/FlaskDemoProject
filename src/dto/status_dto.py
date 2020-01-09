
from flask_restplus import Namespace, fields


class StatusDto:
    api = Namespace('status', description='Ping Micro Service')
    status = api.model('status', {
        'message': fields.String(required=True, description=''),
        'status': fields.String(required=True, description='')
    })

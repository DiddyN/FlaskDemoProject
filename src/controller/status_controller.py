
from flask_restplus import Resource

from src.dto import StatusDto

api = StatusDto.api
_status = StatusDto.status


@api.route('/')
class Status(Resource):
    @api.response(200, 'Ping Micro Service.', _status)
    @api.doc('status', params={})
    @api.marshal_with(fields=_status)
    def get(self):
        return {"status": "OK", "message": "ping!"}

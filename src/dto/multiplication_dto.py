
from flask_restplus import Namespace, fields


class MultiplicationDto:
    api = Namespace('api/multiplication', description='Perform multiplication of wanted numbers.')
    m_number = api.model('one-number',
                         {'number': fields.Float(required=True,
                                                 description="Wanted floating point number",
                                                 example="10.5")
                          })

    request = api.model('request',
                        {
                            'numbers': fields.List(fields.Nested(m_number)),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('response', {
        'result': fields.Float(required=True, description='Result of wanted math operation.')
    })

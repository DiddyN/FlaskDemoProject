
from flask_restplus import Namespace, fields


class AdditionDto:
    api = Namespace('api/addition', description='Perform addition for wanted numbers.')
    m_number = api.model('one-number',
                         {'number': fields.Float(required=True,
                                                 description="Wanted floating point number",
                                                 example="10.5")
                          })

    request = api.model('addition-request',
                        {
                            'numbers': fields.List(fields.Nested(m_number)),
                            'access_token': fields.String(description='Value of access token.')
                        })

    response = api.model('addition-response', {
        'result': fields.Float(required=True, description='Result of wanted math operation.')
    })

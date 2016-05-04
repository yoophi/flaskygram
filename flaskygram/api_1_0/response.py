from flask import jsonify
from . import api

from .schema import EnvelopeSchema


def api_response(data, meta=None, pagination=None):
    if meta is None:
        meta = {
            'code': 200,
            'message': 'OK'
        }

    rv = {'data': data, 'meta': meta}
    if pagination:
        rv['pagination'] = pagination

    return jsonify(EnvelopeSchema().dump(rv).data)


def error_response(status_code=400, message=None):
    default_messages = {
        400: 'Bad request',
        500: 'Internal Server Error'
    }
    if not message:
        message = default_messages.get(status_code, 'unknown error')

    meta = {
        'code': status_code,
        'message': message
    }

    response = api_response({}, meta=meta, pagination=None)
    response.status_code = status_code

    return response


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return error_response(status_code=error.status_code, message=error.message)

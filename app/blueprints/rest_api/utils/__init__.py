from flask import jsonify, make_response, url_for
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    payload = {'error': str(status_code)+ ' ' + 
                        HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message

    response = jsonify(payload)
    response.status_code = status_code
    return response


def error_handler(e):
    code = 500
    error, message = str(e).split(':', 1)

    if isinstance(e, HTTPException):
        code = e.code

    return make_response(jsonify(error=error), code)


def pagination(query, result, page, per_page, endpoint, **kwargs):
    resources = query.paginate(page, per_page, False)

    data = {
        '_meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': resources.pages,
            'total_items': resources.total
        },
        '_links': {
            'self': url_for(endpoint, page=page, per_page=per_page,
                            **kwargs),
            'next': url_for(endpoint, page=page + 1, per_page=per_page,
                            **kwargs) if resources.has_next else None,
            'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                            **kwargs) if resources.has_prev else None
        },
        'items': result
    }
    return data
import traceback
from typing import Union

from connexion.exceptions import ConnexionException
from flask import jsonify
from werkzeug.exceptions import HTTPException

from metron_sites.core.exception import SiteError
from metron_sites.core.logger import ApiLogger


def generate_error_message(message, status_code):
    """
    generate a formated error message
    """
    error_dict = {
        'error': {
            'message': message,
            'code': status_code,
            'details': [
                {
                    'error_id': 'METRON-???'
                }
            ]
        }
    }
    return error_dict


def exception_handler(error: Union[SiteError, ConnexionException, HTTPException, Exception]):
    """
    get a standard error message
    """
    details = ""
    if isinstance(error, SiteError):
        status_code = error.status_code
        message = error.message
        details = error.details
    elif isinstance(error, ConnexionException):
        status_code = error.status
        message = error.detail
    elif isinstance(error, HTTPException):
        status_code = error.code or 500
        message = error.description
    else:
        status_code = 500
        message = f'Unexpected exception. ({error})'

    if not details:
        details = message
    ApiLogger().get_logger().debug(''.join(traceback.format_tb(error.__traceback__)))
    error_dict = generate_error_message(message, status_code)
    ApiLogger().get_logger().error(dict(**error_dict, details=details))
    if status_code == 500:
        traceback.print_exc()
    response = jsonify(error_dict)
    response.status_code = status_code
    return response

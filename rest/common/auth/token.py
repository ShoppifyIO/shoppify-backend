from datetime import datetime, timedelta
from typing import Dict

import jwt
from flask import current_app, request

from rest.common.exceptions.auth_exception import AuthException


def create_token(user_id: int) -> str:
    return jwt.encode({
        'exp': datetime.utcnow() + timedelta(minutes=3000),
        'iat': datetime.utcnow(),
        'id': user_id
    }, current_app.config['SECRET_KEY'], algorithm='HS256')


def handle_request_token(
        req: request
) -> int:
    if 'token' not in req.headers:
        raise AuthException('Musisz być zalogowany')

    encoded_token = req.headers['token']
    token = decode_token(encoded_token)
    user_id: int = token['id']

    return user_id


def decode_token(encoded_token: str) -> Dict[str, any]:
    """
    Decodes token. Then returns dictionary representation of it.

    Raises AuthException.
    :param encoded_token:
    :return:
    """
    try:
        token = jwt.decode(
            encoded_token,
            current_app.config['SECRET_KEY'],
            algorithms='HS256'
        )
    except jwt.ExpiredSignatureError as expired_error:
        raise AuthException('Sesja wygasła. Zaloguj się ponownie') from expired_error
    except jwt.InvalidSignatureError as invalid_error:
        raise AuthException('Podano nieprawidłowy token') from invalid_error
    except jwt.exceptions.DecodeError as decode_error:
        raise AuthException('Nie udało się zdekodować tokenu') from decode_error

    return token

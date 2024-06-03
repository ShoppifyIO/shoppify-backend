from typing import Dict, Any

from flask import Blueprint, Response, request

from rest.common.auth.token import create_token
from rest.common.exceptions.abstract_exception import AbstractException
from rest.common.json.extractor import Extractor
from rest.common.response import respond_created, respond
from rest.sql.db_connection import ProcReturnType, DBConnection
from rest.sql.db_repository import get_db_connection, call_procedure
from rest.sql.procedures import db_login

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['PUT'])
def register() -> Response:
    try:
        extractor: Extractor = Extractor(request.json)

        username: str = extractor.str_required('username')
        email: str = extractor.str_required('email')
        password: str = extractor.str_required('password')

        user_id: int = call_procedure(
            'add_user',
            [username, email, password],
            ProcReturnType.ID
        )

        return respond_created({
            'id': user_id,
            'username': username,
            'email': email
        })
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()


@user_blueprint.route('/login', methods=['POST'])
def login() -> Response:
    try:
        extractor: Extractor = Extractor(request.json)

        username: str = extractor.str_required('username')
        password: str = extractor.str_required('password')

        user: Dict[str, Any] = db_login(username, password)

        token: str = create_token(user['id'])

        return respond(
            {
                'token': token,
                'user': user
            },
            200
        )
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()

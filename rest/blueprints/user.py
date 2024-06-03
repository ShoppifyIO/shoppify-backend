from flask import Blueprint, Response, request

from rest.common.exceptions.abstract_exception import AbstractException
from rest.common.json.extractor import Extractor
from rest.common.response import respond_created
from rest.sql.procedures import add_user


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['PUT'])
def register() -> Response:
    try:
        extractor: Extractor = Extractor(request.json)

        username: str = extractor.str_required('username')
        email: str = extractor.str_required('email')
        password: str = extractor.str_required('password')

        add_user(username, email, password)

        return respond_created()
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()


@user_blueprint.route('/login', methods=['POST'])
def login() -> Response:
    try:
        extractor: Extractor = Extractor(request.json)

        username: str = extractor.str_required('username')
        password: str = extractor.str_required('password')

        # login_user(username, password)
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()

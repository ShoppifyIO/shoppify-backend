from typing import Dict, Any, List

from flask import Blueprint, Response, request

from rest.common.auth.token import create_token, handle_request_token
from rest.common.exceptions.abstract_exception import AbstractException
from rest.common.json.extractor import Extractor
from rest.common.models.user_item import UserItem
from rest.common.response import respond_created, respond
from rest.sql.operator.db_inserter import DBInserter
from rest.sql.operator.db_operator import DBOperator

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register', methods=['PUT'])
def register() -> Response:
    try:
        extractor: Extractor = Extractor(request.json)

        username: str = extractor.str_required('username')
        email: str = extractor.str_required('email')
        password: str = extractor.str_required('password')

        user_id: int = DBInserter.db_insert_user(username, email, password)

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

        user: Dict[str, Any] = DBOperator.db_login(username, password)

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


@user_blueprint.route('/user/items', methods=['GET'])
def get_items() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        user_items: List[UserItem] = UserItem.load_user_items(logged_user)
        return respond(UserItem.to_dict_multiple(user_items), 200)
    except AbstractException as aex:
        return aex.to_response()


@user_blueprint.route('/user/items/add', methods=['POST'])
def add_item() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        extractor: Extractor = Extractor(request.json)

        category_id: int = extractor.int_optional('category_id')
        name: str = extractor.str_required('name')

        user_item_id: int = DBInserter.db_insert_user_item(logged_user, category_id, name)
        user_item: UserItem = UserItem(user_item_id)

        return respond_created(user_item.to_dict())
    except AbstractException as aex:
        return aex.to_response()

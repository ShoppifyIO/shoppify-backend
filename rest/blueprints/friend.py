from typing import List

from flask import Blueprint, Response, request

from rest.common.auth.token import handle_request_token
from rest.common.exceptions.abstract_exception import AbstractException
from rest.common.json.extractor import Extractor
from rest.common.models.user import User
from rest.common.response import respond_created, respond
from rest.sql.operator.db_inserter import DBInserter

friend_blueprint = Blueprint('friend', __name__)


@friend_blueprint.route('/add', methods=['PUT'])
def add() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        extractor: Extractor = Extractor(request.json)

        new_friend_username: str = extractor.str_required('username')
        DBInserter().db_insert_friend(logged_user, new_friend_username)

        return respond_created(None)
    except AbstractException as aex:
        return aex.to_response()


@friend_blueprint.route('', methods=['GET'])
def get_friends() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        friends: List[User] = User.load_user_friends(logged_user)
        return respond(User.to_dict_multiple(friends), 200)
    except AbstractException as aex:
        return aex.to_response()

from flask import Blueprint, Response, request

from rest.common.auth.token import handle_request_token
from rest.common.exceptions.abstract_exception import AbstractException
from rest.common.response import respond
from rest.sql.operator.db_updater import DBUpdater

shopping_item_blueprint = Blueprint('shopping_item', __name__)


@shopping_item_blueprint.route('/complete/<shopping_item_id>', methods=['POST'])
def complete(shopping_item_id: int) -> Response:
    try:
        logged_user: int = handle_request_token(request)
        db_updater: DBUpdater = DBUpdater(logged_user)
        db_updater.change_completed_status_shopping_item(shopping_item_id, True)
        return respond(None, 200)
    except AbstractException as aex:
        return aex.to_response()


@shopping_item_blueprint.route('/incomplete/<shopping_item_id>', methods=['POST'])
def incomplete(shopping_item_id: int) -> Response:
    try:
        logged_user: int = handle_request_token(request)
        db_updater: DBUpdater = DBUpdater(logged_user)
        db_updater.change_completed_status_shopping_item(shopping_item_id, False)
        return respond(None, 200)
    except AbstractException as aex:
        return aex.to_response()

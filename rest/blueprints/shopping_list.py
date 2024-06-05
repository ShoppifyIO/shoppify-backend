from flask import Blueprint, Response, request

from rest.common.auth.token import handle_request_token
from rest.common.exceptions.abstract_exception import AbstractException
from rest.common.json.extractor import Extractor
from rest.common.models.shopping_list import ShoppingList
from rest.common.response import respond_created
from rest.sql.procedures import db_add_shopping_list

shopping_list_blueprint = Blueprint('shopping_list', __name__)


@shopping_list_blueprint.route('/add', methods=['POST'])
def add() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        extractor: Extractor = Extractor(request.json)

        title: str = extractor.str_required('title')
        category_id: int | None = extractor.int_optional('category_id')

        shopping_list_id: int = db_add_shopping_list(logged_user, title, category_id)
        shopping_list: ShoppingList = ShoppingList(shopping_list_id)

        return respond_created(shopping_list.to_dict())
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()

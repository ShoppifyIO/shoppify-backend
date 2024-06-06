from typing import List, Dict, Any

from flask import Blueprint, Response, request

from rest.common.auth.token import handle_request_token
from rest.common.exceptions.abstract_exception import AbstractException
from rest.common.json.extractor import Extractor
from rest.common.models.shopping_list_header import ShoppingListHeader
from rest.common.models.shopping_list import ShoppingList
from rest.common.response import respond_created, respond
from rest.sql.db_operator import DBOperator

shopping_list_blueprint = Blueprint('shopping_list', __name__)


@shopping_list_blueprint.route('/add', methods=['POST'])
def add() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        extractor: Extractor = Extractor(request.json)

        title: str = extractor.str_required('title')
        category_id: int | None = extractor.int_optional('category_id')

        db_operator: DBOperator = DBOperator()
        db_operator.start_transaction()

        shopping_list_id: int = db_operator.add_shopping_list(logged_user, title, category_id)

        for shopping_item in extractor.array_optional('shopping_items'):
            item_extractor: Extractor = Extractor(shopping_item)

            name: str = item_extractor.str_required('name')
            quantity: int | None = item_extractor.int_optional('quantity')
            category_id: int | None = item_extractor.int_optional('category_id')

            db_operator.add_shopping_item(shopping_list_id, name, logged_user, quantity, category_id)

        db_operator.end_transaction()

        shopping_list: ShoppingList = ShoppingList(shopping_list_id)
        return respond_created(shopping_list.to_dict_with_children())
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()


@shopping_list_blueprint.route('/active', methods=['GET'])
def active() -> Response:
    try:
        logged_user: int = handle_request_token(request)

        headers: List[ShoppingListHeader] = ShoppingListHeader.load_active_shopping_list_headers(logged_user)
        headers_dict: List[Dict[str, Any]] = ShoppingListHeader.multiple_to_dict(headers)

        return respond(headers_dict, 200)
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()


@shopping_list_blueprint.route('/archive', methods=['GET'])
def archive() -> Response:
    try:
        logged_user: int = handle_request_token(request)

        headers: List[ShoppingListHeader] = ShoppingListHeader.load_archived_shopping_list_headers(logged_user)
        headers_dict: List[Dict[str, Any]] = ShoppingListHeader.multiple_to_dict(headers)

        return respond(headers_dict, 200)
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()

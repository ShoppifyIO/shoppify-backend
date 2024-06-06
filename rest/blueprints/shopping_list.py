from typing import List, Dict, Any

from flask import Blueprint, Response, request

from rest.common.auth.token import handle_request_token
from rest.common.exceptions.abstract_exception import AbstractException
from rest.common.json.extractor import Extractor
from rest.common.models.shopping_list_header import ShoppingListHeader
from rest.common.models.shopping_list import ShoppingList
from rest.common.response import respond_created, respond
from rest.sql.operator.db_deleter import DBDeleter
from rest.sql.operator.db_inserter import DBInserter
from rest.sql.operator.db_updater import DBUpdater

shopping_list_blueprint = Blueprint('shopping_list', __name__)


@shopping_list_blueprint.route('/<shopping_list_id>', methods=['GET'])
def get(shopping_list_id: int) -> Response:
    try:
        logged_user: int = handle_request_token(request)

        ShoppingList.verify_authorisation(logged_user, shopping_list_id)

        sl: ShoppingList = ShoppingList(shopping_list_id)

        return respond(sl.to_dict_with_children(), 200)
    except AbstractException as ex:
        return ex.to_response()


@shopping_list_blueprint.route('/add', methods=['POST'])
def add() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        extractor: Extractor = Extractor(request.json)

        title: str = extractor.str_required('title')
        category_id: int | None = extractor.int_optional('category_id')

        db_inserter: DBInserter = DBInserter()
        db_inserter.start_transaction()

        shopping_list_id: int = db_inserter.insert_shopping_list(logged_user, title, category_id)

        __add_new_shopping_items(
            extractor.array_optional('shopping_items'),
            db_inserter,
            shopping_list_id,
            logged_user
        )

        db_inserter.end_transaction()

        new_shopping_list: ShoppingList = ShoppingList(shopping_list_id)
        return respond_created(new_shopping_list.to_dict_with_children())
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()


@shopping_list_blueprint.route('/modify', methods=['POST'])
def modify() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        extractor: Extractor = Extractor(request.json)

        shopping_list_id: int = extractor.int_required('id')
        new_title: str | None = extractor.str_optional('title')
        new_category_id: int | None = extractor.int_optional('category_id')

        db_updater: DBUpdater = DBUpdater(logged_user)
        db_updater.start_transaction()
        db_updater.update_shopping_list(shopping_list_id, new_title, new_category_id)

        db_inserter: DBInserter = DBInserter(db_updater)
        db_deleter: DBDeleter = DBDeleter(db_updater)

        __add_new_shopping_items(
            extractor.array_optional('new_shopping_items'),
            db_inserter,
            shopping_list_id,
            logged_user
        )

        for shopping_item in extractor.array_optional('modified_shopping_items'):
            item_extractor: Extractor = Extractor(shopping_item)

            shopping_item_id: int = item_extractor.int_required('id')
            new_name: str | None = item_extractor.str_optional('name')
            new_category_id: int = item_extractor.int_optional('category_id')
            new_quantity: int = item_extractor.int_optional('quantity')

            db_updater.update_shopping_item(shopping_item_id, new_name, new_category_id, new_quantity)

        for shopping_item in extractor.array_optional('deleted_shopping_items'):
            item_extractor: Extractor = Extractor(shopping_item)

            shopping_item_id: int = item_extractor.int_required('id')

            db_deleter.delete_shopping_item(shopping_item_id)

        db_updater.end_transaction()

        modified_shopping_list: ShoppingList = ShoppingList(shopping_list_id)
        return respond(modified_shopping_list.to_dict_with_children(), 200)
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


def __add_new_shopping_items(
        shopping_items: List[Dict[str, Any]],
        db_inserter: DBInserter,
        shopping_list_id: int,
        logged_user: int
) -> None:
    for shopping_item in shopping_items:
        item_extractor: Extractor = Extractor(shopping_item)

        name: str = item_extractor.str_required('name')
        quantity: int | None = item_extractor.int_optional('quantity')
        category_id: int | None = item_extractor.int_optional('category_id')

        db_inserter.insert_shopping_item(shopping_list_id, name, logged_user, quantity, category_id)

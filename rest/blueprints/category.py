from typing import List

from flask import Blueprint, Response, request

from rest.common.auth.token import handle_request_token
from rest.common.exceptions.abstract_exception import AbstractException
from rest.common.json.extractor import Extractor
from rest.common.models.category import Category
from rest.common.models.enums.category_type import CategoryType
from rest.common.response import respond_created, respond
from rest.sql.operator.db_inserter import DBInserter

category_blueprint = Blueprint('category', __name__)


@category_blueprint.route('/add', methods=['POST'])
def add_category() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        extractor: Extractor = Extractor(request.json)

        title: str = extractor.str_required('title')
        cat_type: CategoryType = CategoryType.from_str(extractor.str_required('type'))
        description: str = extractor.str_optional('description', '')
        color: str = extractor.str_required('color')

        category_id: int = DBInserter.db_insert_category(logged_user, cat_type.to_int(), title, description, color)
        category: Category = Category(category_id)

        return respond_created(category.to_dict())
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()


@category_blueprint.route('/list', methods=['GET'])
def list_categories() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        categories: List[Category] = Category.load_list_categories(logged_user)
        return respond(Category.to_dict_multiple(categories), 200)
    except AbstractException as aex:
        return aex.to_response()


@category_blueprint.route('/item', methods=['GET'])
def item_categories() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        categories: List[Category] = Category.load_item_categories(logged_user)
        return respond(Category.to_dict_multiple(categories), 200)
    except AbstractException as aex:
        return aex.to_response()

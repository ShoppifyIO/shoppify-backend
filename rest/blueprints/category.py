from flask import Blueprint, Response, request

from rest.common.auth.token import handle_request_token
from rest.common.exceptions.abstract_exception import AbstractException
from rest.common.json.extractor import Extractor
from rest.common.response import respond_created
from rest.sql.operator.db_operator import DBOperator

category_blueprint = Blueprint('category', __name__)


@category_blueprint.route('/add', methods=['POST'])
def add_category() -> Response:
    try:
        logged_user: int = handle_request_token(request)
        extractor: Extractor = Extractor(request.json)

        title: str = extractor.str_required('title')
        cat_type: int = extractor.int_required('type')
        description: str = extractor.str_optional('description', '')
        color: str = extractor.str_required('color')

        category_id: int = DBOperator.db_add_category(logged_user, cat_type, title, description, color)

        return respond_created({'id': category_id, 'title': title, 'type': cat_type, 'description': description, 'color': color})
    except AbstractException as abstract_exception:
        return abstract_exception.to_response()

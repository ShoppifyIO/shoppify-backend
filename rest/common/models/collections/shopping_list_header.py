from __future__ import annotations
from datetime import datetime
from typing import List, Any, Dict

from psycopg2.extras import RealDictRow

from rest.sql.db_repository import call_query
from rest.sql.query_return_type import QueryReturnType


class ShoppingListHeader:
    id: int
    title: str
    update_date: datetime
    updated_by: str
    category_name: str
    category_color: str
    user_id: int
    is_user_owner: bool

    def __init__(
        self,
        shopping_list_header_id: int,
        title: str,
        update_date: datetime,
        updated_by: str,
        category_name: str,
        category_color: str,
        user_id: int,
        is_user_owner: bool,
    ):
        self.id = shopping_list_header_id
        self.title = title
        self.update_date = update_date
        self.updated_by = updated_by
        self.category_name = category_name
        self.category_color = category_color
        self.user_id = user_id
        self.is_user_owner = is_user_owner

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'update_date': self.update_date,
            'updated_by': self.updated_by,
            'category_name': self.category_name,
            'category_color': self.category_color,
            'user_id': self.user_id,
            'is_user_owner': self.is_user_owner
        }

    @staticmethod
    def multiple_to_dict(
            shopping_list_headers: List[ShoppingListHeader]
    ) -> List[Dict[str, Any]]:
        shopping_list_headers_dict = []
        for shopping_list_header in shopping_list_headers:
            shopping_list_headers_dict.append(shopping_list_header.to_dict())
        return shopping_list_headers_dict

    @staticmethod
    def load_active_shopping_list_headers(user_id: int) -> List[ShoppingListHeader]:
        headers: List[RealDictRow] = call_query(
            'SELECT * FROM active_shopping_lists WHERE user_id = %s',
            (user_id,),
            QueryReturnType.LIST
        )

        shopping_list_headers: List[ShoppingListHeader] = []
        for header in headers:
            shopping_list_headers.append(ShoppingListHeader(
                header['shopping_list_id'],
                header['title'],
                header['update_date'],
                header['updated_by'],
                header['category_name'],
                header['category_color'],
                header['user_id'],
                header['is_user_owner'] == 1
            ))

        return shopping_list_headers

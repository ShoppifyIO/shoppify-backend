from __future__ import annotations
from typing import Any, Dict, List

from psycopg2.extras import RealDictRow

from rest.common.exceptions.not_found_exception import NotFoundException
from rest.common.models.enums.category_type import CategoryType
from rest.sql.db_repository import call_query
from rest.sql.query_return_type import QueryReturnType


class Category:
    id: int
    owner_id: int
    type: CategoryType
    title: str
    description: str
    color: str

    def __init__(self, category_id: int, _load: bool = True):
        self.id = category_id

        if _load:
            self.__load_db()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "type": self.type.value,
            "title": self.title,
            "description": self.description,
            "color": self.color
        }

    @staticmethod
    def to_dict_multiple(categories: List[Category]) -> List[Dict[str, Any]]:
        category_list: List[Dict[str, Any]] = []
        for category in categories:
            category_list.append(category.to_dict())
        return category_list

    @staticmethod
    def load_list_categories(user_id: int) -> List[Category]:
        return Category.__load_categories(user_id, CategoryType.SHOPPING_LIST)

    @staticmethod
    def load_item_categories(user_id: int) -> List[Category]:
        return Category.__load_categories(user_id, CategoryType.ITEM)

    @staticmethod
    def __load_categories(user_id: int, category_type: CategoryType) -> List[Category]:
        rows: List[RealDictRow] | None = call_query(
            'SELECT * FROM categories WHERE owner_id = %s AND type = %s',
            (user_id, category_type.to_int()),
            QueryReturnType.LIST
        )

        if rows is None or len(rows) == 0:
            return []

        category_list: List[Category] = []
        for row in rows:
            category: Category = Category(row['id'], False)
            category.owner_id = row['owner_id']
            category.type = CategoryType.from_int(row['type'])
            category.title = row['title']
            category.description = row['description']
            category.color = row['color']
            category_list.append(category)

        return category_list

    def __load_db(self) -> None:
        row: RealDictRow | None = call_query(
            'SELECT * FROM categories WHERE id = %s',
            (self.id,),
            QueryReturnType.ROW
        )

        if row is None:
            raise NotFoundException('Kategorii', self.id)

        self.owner_id = row['owner_id']
        self.type = CategoryType.from_int(row['type'])
        self.title = row['title']
        self.description = row['description']
        self.color = row['color']

    @staticmethod
    def verify_authorization(logged_user_id: int, category_id: int) -> None:
        pass

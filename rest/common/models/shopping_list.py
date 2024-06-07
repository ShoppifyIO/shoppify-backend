from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List

from psycopg2.extras import RealDictRow

from rest.common.dates import datetime_to_string
from rest.common.exceptions.not_found_exception import NotFoundException
from rest.common.models.category import Category
from rest.common.models.shopping_item import ShoppingItem
from rest.sql.db_repository import call_query


class ShoppingList:
    id: int
    owner_id: int
    category: Category | None
    title: str
    creation_date: datetime
    update_date: datetime
    updated_by: int
    is_completed: bool

    items: List[ShoppingItem]
    items_loaded: bool

    def __init__(self, shopping_list_id: int, init_children: bool = True):
        self.id = shopping_list_id
        self.__load_db()

        self.items_loaded = False
        self.items = []
        if init_children:
            self.load_items()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'title': self.title,
            'creation_date': datetime_to_string(self.creation_date),
            'update_date': datetime_to_string(self.update_date),
            'updated_by': self.updated_by,
            'is_completed': self.is_completed,
            'category': None if self.category is None else self.category.to_dict(),
        }

    def to_dict_with_children(self) -> Dict[str, Any]:
        self.load_items()

        dictionary: Dict[str, Any] = self.to_dict()
        dictionary['shopping_items'] = []

        for item in self.items:
            dictionary['shopping_items'].append(item.to_dict())

        return dictionary

    def load_items(self) -> None:
        if self.items_loaded:
            return

        self.items_loaded = True
        self.items = ShoppingItem.load_by_shopping_list(self.id)

    def __load_db(self) -> None:
        row: RealDictRow | None = call_query(
            'SELECT * FROM shopping_lists WHERE id = %s',
            (self.id,)
        )

        if row is None:
            raise NotFoundException('listy zakupów', self.id)

        self.owner_id = row['owner_id']
        self.title = row['title']
        self.creation_date = row['creation_date']
        self.update_date = row['update_date']
        self.updated_by = row['updated_by']
        self.is_completed = row['is_completed']
        self.category = None if row['category_id'] is None else Category(row['category_id'])

    @staticmethod
    def verify_authorisation(logged_user_id: int, shopping_list_id: int) -> None:
        pass

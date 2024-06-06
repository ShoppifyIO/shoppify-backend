from __future__ import annotations
from datetime import datetime
from typing import List, Any, Dict

from psycopg2.extras import RealDictRow

from rest.common.dates import datetime_to_string
from rest.sql.db_repository import call_query
from rest.sql.query_return_type import QueryReturnType


class ShoppingItem:
    id: int
    shopping_list_id: int
    category_id: int | None
    name: str
    quantity: int | None
    is_completed: bool
    added_date: datetime
    added_by: int
    completion_date: datetime | None
    completed_by: int | None

    def __init__(
            self,
            shopping_item_id: int,
            shopping_list_id: int,
            category_id: int | None,
            name: str,
            quantity: int | None,
            is_completed: bool,
            added_date: datetime,
            added_by: int,
            completion_date: datetime | None,
            completed_by: int | None,
    ):
        self.id = shopping_item_id
        self.shopping_list_id = shopping_list_id
        self.category_id = category_id
        self.name = name
        self.quantity = quantity
        self.is_completed = is_completed
        self.added_date = added_date
        self.added_by = added_by
        self.completion_date = completion_date
        self.completed_by = completed_by

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'shopping_list_id': self.shopping_list_id,
            'category_id': self.category_id,
            'name': self.name,
            'quantity': self.quantity,
            'is_completed': self.is_completed,
            'added_date': datetime_to_string(self.added_date),
            'added_by': self.added_by,
            'completion_date': datetime_to_string(self.completion_date),
            'completed_by': self.completed_by,
        }

    @staticmethod
    def load_by_shopping_list(shopping_list_id: int) -> List[ShoppingItem]:
        rows: List[RealDictRow] = call_query(
            'SELECT * FROM shopping_list_items WHERE shopping_list_id = %s',
            (shopping_list_id,),
            QueryReturnType.LIST
        )

        if rows is None or len(rows) == 0:
            return []

        items: List[ShoppingItem] = []
        for row in rows:
            items.append(ShoppingItem(
                row['id'],
                row['shopping_list_id'],
                row['category_id'],
                row['name'],
                row['quantity'],
                row['is_completed'],
                row['added_date'],
                row['added_by'],
                row['completion_date'],
                row['completed_by'],
            ))

        return items

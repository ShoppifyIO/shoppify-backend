from datetime import datetime
from typing import Any, Dict

from psycopg2.extras import RealDictRow

from rest.common.dates import datetime_to_string
from rest.common.exceptions.not_found_exception import NotFoundException
from rest.sql.db_repository import call_query


class ShoppingList:
    id: int
    owner_id: int
    category_id: int | None
    title: str
    creation_date: datetime
    update_date: datetime
    updated_by: int
    is_completed: bool

    def __init__(self, shopping_list_id: int):
        self.id = shopping_list_id
        self.__load_db()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'title': self.title,
            'creation_date': datetime_to_string(self.creation_date),
            'update_date': datetime_to_string(self.update_date),
            'updated_by': self.updated_by,
            'is_completed': self.is_completed,
            'category': None
        }

    def __load_db(self) -> None:
        row: RealDictRow | None = call_query(
            'SELECT * FROM shopping_lists WHERE id = %s',
            (self.id,)
        )

        if row is None:
            raise NotFoundException('listy zakupów', self.id)

        self.owner_id = row['owner_id']
        self.category_id = row['category_id']
        self.title = row['title']
        self.creation_date = row['creation_date']
        self.update_date = row['update_date']
        self.updated_by = row['updated_by']
        self.is_completed = row['is_completed']

from __future__ import annotations
from typing import Dict, Any, List

from psycopg2.extras import RealDictRow

from rest.common.exceptions.not_found_exception import NotFoundException
from rest.sql.db_repository import call_query
from rest.sql.query_return_type import QueryReturnType


class UserItem:
    id: int
    owner_id: int
    category_id: int
    name: int

    def __init__(self, user_item_id: int, load: bool = True):
        self.id = user_item_id

        if load:
            self.__load_db()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'category_id': self.category_id,
            'name': self.name
        }

    def __load_db(self) -> None:
        row: RealDictRow | None = call_query(
            'SELECT * FROM user_items WHERE id = %s',
            (self.id,),
            QueryReturnType.ROW
        )

        if row is None:
            raise NotFoundException('Przedmiotu użytkownika', self.id)

        self.owner_id = row['owner_id']
        self.category_id = row['category_id']
        self.name = row['name']

    @staticmethod
    def to_dict_multiple(user_items: List[UserItem]) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for user_item in user_items:
            result.append(user_item.to_dict())
        return result

    @staticmethod
    def load_user_items(user_id) -> List[UserItem]:
        rows: List[RealDictRow] | None = call_query(
            'SELECT * FROM user_items WHERE owner_id = %s',
            (user_id,),
            QueryReturnType.LIST
        )

        if rows is None or len(rows) == 0:
            return []

        user_items: List[UserItem] = []
        for row in rows:
            user_item: UserItem = UserItem(row['id'], False)
            user_item.owner_id = row['owner_id']
            user_item.category_id = row['category_id']
            user_item.name = row['name']
            user_items.append(user_item)

        return user_items

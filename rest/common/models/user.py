from __future__ import annotations
from typing import Dict, Any, List

from psycopg2.extras import RealDictRow

from rest.common.exceptions.not_found_exception import NotFoundException
from rest.sql.db_repository import call_query
from rest.sql.query_return_type import QueryReturnType


class User:
    id: int
    username: str
    email: str

    def __init__(self, user_id: int, load: bool = True):
        self.id = user_id

        if load:
            self.__load_db()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

    def __load_db(self) -> None:
        row: RealDictRow | None = call_query(
            'SELECT * FROM users WHERE id = %s',
            (self.id,),
            QueryReturnType.ROW
        )

        if row is None:
            raise NotFoundException('Użytkownika', self.id)

        self.username = row['username']
        self.email = row['email']

    @staticmethod
    def to_dict_multiple(users: List[User]) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for user in users:
            result.append(user.to_dict())
        return result

    @staticmethod
    def load_user_friends(user_id) -> List[User]:
        rows: List[RealDictRow] | None = call_query(
            'SELECT * FROM user_friends WHERE user_id = %s',
            (user_id,),
            QueryReturnType.LIST
        )

        if rows is None or len(rows) == 0:
            return []

        friends: List[User] = []
        for row in rows:
            user: User = User(row['friend_id'], False)
            user.username = row['friend_username']
            user.email = row['friend_email']
            friends.append(user)

        return friends

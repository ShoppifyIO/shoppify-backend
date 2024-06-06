from psycopg2.extras import RealDictRow

from rest.common.exceptions.not_found_exception import NotFoundException
from rest.sql.operator.db_operator import DBOperator
from rest.sql.proc_return_type import ProcReturnType
from rest.sql.query_return_type import QueryReturnType


class DBInserter(DBOperator):
    @staticmethod
    def db_insert_user(username: str, email: str, password: str) -> int:
        return DBInserter().insert_user(username, email, password)

    def insert_user(self, username: str, email: str, password: str) -> int:
        return self._db_connection.call_procedure(
            'add_user',
            [username, email, password],
            ProcReturnType.ID,
            self._is_transaction_mode
        )

    @staticmethod
    def db_insert_friend(logged_user: int, username: str) -> None:
        return DBInserter().insert_friend(logged_user, username)

    def insert_friend(self, logged_user: int, username: str) -> None:
        friend: RealDictRow | None = self._db_connection.call_query(
            'SELECT id FROM users WHERE username = %s',
            (username,),
            QueryReturnType.ROW
        )

        if friend is None:
            raise NotFoundException('Użytkownika', username)

        friend_id: int = friend['id']
        self._db_connection.call_procedure(
            'add_friend',
            [logged_user, friend_id],
            ProcReturnType.NONE,
            self._is_transaction_mode
        )

    @staticmethod
    def db_insert_shopping_list(owner_id: int, title: str, category_id: int | None) -> int:
        return DBInserter().insert_shopping_list(owner_id, title, category_id)

    def insert_shopping_list(self, owner_id: int, title: str, category_id: int) -> int:
        return self._db_connection.call_procedure(
            'add_shopping_list',
            [owner_id, title, category_id],
            ProcReturnType.ID,
            self._is_transaction_mode
        )

    @staticmethod
    def db_insert_category(owner_id: int, cat_type: int, title: str, description: str, color: str) -> int:
        return DBInserter().insert_category(owner_id, cat_type, title, description, color)

    def insert_category(self, owner_id: int, cat_type: int, title: str, description: str, color: str) -> int:
        return self._db_connection.call_procedure(
            'add_category',
            [owner_id, cat_type, title, description, color],
            ProcReturnType.ID,
            self._is_transaction_mode
        )

    @staticmethod
    def db_insert_shopping_item(
        shopping_list_id: int,
        name: str,
        added_by: int,
        quantity: int | None,
        category_id: int | None,
    ) -> int:
        return DBInserter().insert_shopping_item(shopping_list_id, name, added_by, quantity, category_id)

    def insert_shopping_item(
        self,
        shopping_list_id: int,
        name: str,
        added_by: int,
        quantity: int | None,
        category_id: int | None,
    ) -> int:
        return self._db_connection.call_procedure(
            'add_shopping_item',
            [shopping_list_id, name, added_by, quantity, category_id],
            ProcReturnType.ID,
            self._is_transaction_mode
        )

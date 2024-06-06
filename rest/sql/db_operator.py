from typing import Dict, Any, Tuple

from rest.sql.db_connection import DBConnection
from rest.sql.db_repository import get_db_connection
from rest.sql.proc_return_type import ProcReturnType


class DBOperator:
    __db_connection: DBConnection
    __is_transaction_mode: bool

    def __init__(self):
        self.__db_connection = get_db_connection()
        self.__is_transaction_mode = False

    def start_transaction(self):
        self.__is_transaction_mode = True

    def end_transaction(self):
        self.__is_transaction_mode = False
        self.__db_connection.commit_open_transaction()

    @staticmethod
    def db_add_user(username: str, email: str, password: str) -> int:
        return DBOperator().add_user(username, email, password)

    def add_user(self, username: str, email: str, password: str) -> int:
        return self.__db_connection.call_procedure(
            'add_user',
            [username, email, password],
            ProcReturnType.ID,
            self.__is_transaction_mode
        )

    @staticmethod
    def db_login(username: str, password: str) -> Dict[str, Any]:
        return DBOperator().login(username, password)

    def login(self, username: str, password: str) -> Dict[str, Any]:
        user_tuple: Tuple[Any] = self.__db_connection.call_procedure(
            'login',
            [username, password],
            ProcReturnType.TABLE,
            self.__is_transaction_mode
        )

        return {
            'id': user_tuple[0],
            'username': user_tuple[1],
            'email': user_tuple[2]
        }

    @staticmethod
    def db_add_shopping_list(owner_id: int, title: str, category_id: int | None) -> int:
        return DBOperator().add_shopping_list(owner_id, title, category_id)

    def add_shopping_list(self, owner_id: int, title: str, category_id: int) -> int:
        return self.__db_connection.call_procedure(
            'add_shopping_list',
            [owner_id, title, category_id],
            ProcReturnType.ID,
            self.__is_transaction_mode
        )

    @staticmethod
    def db_add_category(owner_id: int, cat_type: int, title: str, description: str, color: str) -> int:
        return DBOperator().add_category(owner_id, cat_type, title, description, color)

    def add_category(self, owner_id: int, cat_type: int, title: str, description: str, color: str) -> int:
        return self.__db_connection.call_procedure(
            'add_category',
            [owner_id, cat_type, title, description, color],
            ProcReturnType.ID,
            self.__is_transaction_mode
        )

    @staticmethod
    def db_add_shopping_item(
        shopping_list_id: int,
        name: str,
        added_by: int,
        quantity: int | None,
        category_id: int | None,
    ) -> int:
        return DBOperator().add_shopping_item(shopping_list_id, name, added_by, quantity, category_id)

    def add_shopping_item(
        self,
        shopping_list_id: int,
        name: str,
        added_by: int,
        quantity: int | None,
        category_id: int | None,
    ) -> int:
        return self.__db_connection.call_procedure(
            'add_shopping_item',
            [shopping_list_id, name, added_by, quantity, category_id],
            ProcReturnType.ID,
            self.__is_transaction_mode
        )

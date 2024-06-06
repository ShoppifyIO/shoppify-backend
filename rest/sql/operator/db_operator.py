from __future__ import annotations
from typing import Dict, Any, Tuple

from rest.sql.db_connection import DBConnection
from rest.sql.db_repository import get_db_connection
from rest.sql.proc_return_type import ProcReturnType


class DBOperator:
    _db_connection: DBConnection
    _is_transaction_mode: bool

    def __init__(self, db_operator: DBOperator | None = None):
        if db_operator is not None and db_operator._is_transaction_mode:
            self._is_transaction_mode = True
            self._db_connection = db_operator._db_connection
            return

        self._db_connection = get_db_connection()
        self._is_transaction_mode = False

    def start_transaction(self):
        self._is_transaction_mode = True

    def end_transaction(self):
        self._is_transaction_mode = False
        self._db_connection.commit_open_transaction()

    @staticmethod
    def db_login(username: str, password: str) -> Dict[str, Any]:
        return DBOperator().login(username, password)

    def login(self, username: str, password: str) -> Dict[str, Any]:
        user_tuple: Tuple[Any] = self._db_connection.call_procedure(
            'login',
            [username, password],
            ProcReturnType.TABLE,
            self._is_transaction_mode
        )

        return {
            'id': user_tuple[0],
            'username': user_tuple[1],
            'email': user_tuple[2]
        }

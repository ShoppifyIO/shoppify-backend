from typing import Set, List, Any, Tuple
import psycopg2
from psycopg2._psycopg import cursor
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.extensions import connection

from rest.common.exceptions.sql_exception import SqlException
from rest.sql.proc_return_type import ProcReturnType
from rest.sql.query_return_type import QueryReturnType

custom_error_letters: Set[str] = {'U'}


class DBConnection:
    name: str
    user: str
    password: str
    host: str

    __connection: connection | None

    def __init__(self, name: str, user: str, password: str, host: str):
        self.name = name
        self.user = user
        self.password = password
        self.host = host

        self.__connection = None

    def commit_open_transaction(self):
        if self.__connection is None:
            raise 'Connection is not open'

        self.__connection.commit()
        self.__connection.close()

    def rollback_open_transaction(self):
        if self.__connection is None:
            raise 'Connection is not open'

        self.__connection.rollback()
        self.__connection.close()

    def call_procedure(
            self,
            procname: str,
            proc_params: List[Any],
            return_type: ProcReturnType,
            keep_transaction: bool = False,
    ) -> Tuple[Any, ...] | int | None:
        cur: cursor = self.__prepare_operation_objects()

        try:
            cur.callproc(procname, proc_params)
            result = cur.fetchone()

            if not keep_transaction:
                self.__connection.commit()

            if return_type == ProcReturnType.ID:
                return result[0]

            if return_type == ProcReturnType.TABLE:
                return result

            return None
        except psycopg2.Error as e:
            self.__connection.rollback()
            self.__handle_db_exception(e)
        finally:
            self.__cleanup_after_operation(cur, keep_transaction)

    def call_simple_delete_query(self, table_name: str, object_id: int, keep_transaction: bool) -> None:
        cur: cursor = self.__prepare_operation_objects()

        try:
            cur.execute(f'DELETE FROM {table_name} WHERE id = %s', (object_id,))
        except psycopg2.Error as e:
            self.__connection.rollback()
            self.__handle_db_exception(e)
        finally:
            self.__cleanup_after_operation(cur, keep_transaction)

    def call_update_query(self, query: str, params: Tuple[Any, ...], keep_transaction: bool) -> None:
        cur: cursor = self.__prepare_operation_objects()

        try:
            cur.execute(query, params)
        except psycopg2.Error as e:
            self.__connection.rollback()
            self.__handle_db_exception(e)
        finally:
            self.__cleanup_after_operation(cur, keep_transaction)

    def call_query(
            self,
            query: str,
            params: Tuple[Any],
            query_return_type: QueryReturnType
    ) -> None | RealDictRow | list[RealDictRow]:
        conn = self.__create_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute(query, params)

            if query_return_type == QueryReturnType.NONE:
                return None

            if query_return_type == QueryReturnType.ROW:
                return cur.fetchone()

            if query_return_type == QueryReturnType.LIST:
                return cur.fetchall()

            raise f'Unknown QueryReturnType: {query_return_type}'
        except psycopg2.Error as e:
            self.__handle_db_exception(e)
        finally:
            cur.close()
            conn.close()

    def __prepare_operation_objects(self) -> cursor:
        if self.__connection is None:
            self.__connection = self.__create_connection()
        return self.__connection.cursor()

    def __cleanup_after_operation(self, cur: cursor, keep_transaction: bool) -> None:
        cur.close()

        if not keep_transaction:
            self.__connection.close()
            self.__connection = None

    def __create_connection(self):
        return psycopg2.connect(
            dbname=self.name,
            user=self.user,
            password=self.password,
            host=self.host)

    @staticmethod
    def __handle_db_exception(e):
        if e.pgcode[0] not in custom_error_letters:
            print('Unknown Error', e)
            raise e
        print('Custom Error', e)
        raise SqlException(e.pgerror)

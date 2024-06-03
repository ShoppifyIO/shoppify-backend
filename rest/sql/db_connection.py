from enum import Enum
from typing import Set, List, Any
import psycopg2
from rest.common.exceptions.sql_exception import SqlException


custom_error_letters: Set[str] = {'U'}


class ProcReturnType(Enum):
    NONE = "None"
    ID = "ID"


class DBConnection:
    name: str
    user: str
    password: str
    host: str

    def __init__(self, name: str, user: str, password: str, host: str):
        self.name = name
        self.user = user
        self.password = password
        self.host = host

    def call_procedure(
            self,
            procname: str,
            proc_params: List[Any],
            return_type: ProcReturnType = ProcReturnType.NONE
    ) -> int | None:
        conn = self.__create_connection()
        cur = conn.cursor()

        try:
            cur.callproc(procname, proc_params)
            result = cur.fetchone()
            conn.commit()

            if return_type == ProcReturnType.ID:
                return result[0]

            return None
        except psycopg2.Error as e:
            self.__handle_db_exception(e)
        finally:
            cur.close()
            conn.close()

    def __create_connection(self):
        return psycopg2.connect(
            dbname=self.name,
            user=self.user,
            password=self.password,
            host=self.host)

    @staticmethod
    def __handle_db_exception(e):
        if e.pgcode[0] not in custom_error_letters:
            raise e
        raise SqlException(e.pgerror)

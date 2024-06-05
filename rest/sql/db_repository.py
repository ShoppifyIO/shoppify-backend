from typing import List, Any, Tuple

from psycopg2.extras import RealDictRow

from rest.sql.db_connection import DBConnection
from rest.sql.proc_return_type import ProcReturnType
from rest.sql.query_return_type import QueryReturnType

db_name = 'shoppify-db'
db_user = 'postgres'
db_password = 'mleko'
db_host = 'localhost'


def get_db_connection() -> DBConnection:
    return DBConnection(db_name, db_user, db_password, db_host)


def call_procedure(
    proc_name: str,
    proc_params: List[Any],
    return_type: ProcReturnType
) -> Tuple[Any] | int | None:
    conn: DBConnection = get_db_connection()
    return conn.call_procedure(proc_name, proc_params, return_type)


def call_query(
        query: str,
        params: Tuple[Any],
        return_type: QueryReturnType = QueryReturnType.ROW
) -> None | RealDictRow | list[RealDictRow]:
    conn: DBConnection = get_db_connection()
    return conn.call_query(query, params, return_type)

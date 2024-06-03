from typing import List, Any, Tuple

from rest.sql.db_connection import DBConnection
from rest.sql.proc_return_type import ProcReturnType

db_name = 'shoppify-db'
db_user = 'postgres'
db_password = 'mleko'
db_host = 'localhost'


def get_db_connection() -> DBConnection:
    return DBConnection(db_name, db_user, db_password, db_host)


def call_procedure(
    procname: str,
    proc_params: List[Any],
    return_type: ProcReturnType
) -> Tuple[Any] | int | None:
    conn: DBConnection = get_db_connection()
    return conn.call_procedure(procname, proc_params, return_type)

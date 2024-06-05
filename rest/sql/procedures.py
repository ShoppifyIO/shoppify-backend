from typing import Any, Dict, Tuple

from rest.sql.db_repository import call_procedure
from rest.sql.proc_return_type import ProcReturnType


def db_login(username: str, password: str) -> Dict[str, Any]:
    user_tuple: Tuple[Any] = call_procedure(
        'login',
        [username, password],
        ProcReturnType.TABLE
    )

    return {
        'id': user_tuple[0],
        'username': user_tuple[1],
        'email': user_tuple[2]
    }


def db_add_shopping_list(owner_id: int, title: str, category_id: int) -> int:
    return call_procedure(
        'add_shopping_list',
        [owner_id, title, category_id],
        ProcReturnType.ID
    )

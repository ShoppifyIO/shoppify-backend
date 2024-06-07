from typing import Any, List

from rest.sql.operator.db_operator import DBOperator


class DBUpdater(DBOperator):
    __logged_user: int

    _query: str | None
    _params: List[Any] | None

    def __init__(self, logged_user_id: int, db_operator: DBOperator | None = None):
        super().__init__(db_operator)
        self.__logged_user = logged_user_id

    def update_shopping_list(self, shopping_list_id: int, new_title: str | None, new_category_id: int | None) -> None:
        if new_title is None and new_category_id is None:
            return

        self.__begin_query('shopping_lists')
        self.__handle_query_param('updated_by', self.__logged_user)
        self.__handle_query_param('title', new_title)
        self.__handle_query_param('category_id', new_category_id)
        self.__finish_and_run_query(shopping_list_id)

    def change_completed_status_shopping_list(self, shopping_list_id: int, is_completed: bool) -> None:
        self.__begin_query('shopping_lists')
        self.__handle_query_param('updated_by', self.__logged_user)
        self.__handle_query_param('is_completed', is_completed)
        self.__finish_and_run_query(shopping_list_id)

    def update_shopping_item(
            self,
            shopping_item_id: int,
            new_name: str | None,
            new_category_id: int | None,
            new_quantity: int | None
    ) -> None:
        if new_name is None and new_category_id is None and new_quantity is None:
            return

        self.__begin_query('shopping_list_items')
        self.__handle_query_param('added_by', self.__logged_user)
        self.__handle_query_param('name', new_name)
        self.__handle_query_param('category_id', new_category_id)
        self.__handle_query_param('quantity', new_quantity)
        self.__finish_and_run_query(shopping_item_id)

    def change_completed_status_shopping_item(self, shopping_item_id: int, is_completed: bool) -> None:
        self.__begin_query('shopping_list_items')
        self.__handle_query_param('completed_by', self.__logged_user)
        self.__handle_query_param('is_completed', is_completed)
        self.__finish_and_run_query(shopping_item_id)

    def __begin_query(self, table_name: str) -> None:
        self._query = f'UPDATE {table_name} SET '
        self._params = []

    def __handle_query_param(self, param_name: str, param: Any) -> None:
        if param is None:
            return

        self._query += f'{param_name} = %s, '
        self._params.append(param)

    def __finish_and_run_query(self, object_id: int) -> None:
        self._query = self._query[:-2]
        self._query += ' WHERE id = %s'
        self._params.append(object_id)

        self._db_connection.call_update_query(self._query, tuple(self._params), self._is_transaction_mode)

        self._query = None
        self._params = None

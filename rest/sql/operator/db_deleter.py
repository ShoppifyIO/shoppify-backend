from rest.sql.operator.db_operator import DBOperator


class DBDeleter(DBOperator):

    def delete_shopping_item(self, shopping_item_id: int) -> None:
        self._db_connection.call_simple_delete_query(
            'shopping_list_items',
            shopping_item_id,
            self._is_transaction_mode
        )

    def delete_shopping_list(self, shopping_list_id: int) -> None:
        self._db_connection.call_simple_delete_query(
            'shopping_lists',
            shopping_list_id,
            self._is_transaction_mode
        )

    def delete_category(self, category_id: int) -> None:
        self._db_connection.call_simple_delete_query(
            'categories',
            category_id,
            self._is_transaction_mode
        )

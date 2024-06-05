from typing import Any

from rest.common.exceptions.not_found_exception import NotFoundException
from rest.common.models.enums.category_type import CategoryType
from rest.sql.db_repository import call_query


class Category:
    id: int
    owner_id: int
    type: CategoryType
    title: str
    description: str
    color: str

    def __init__(self, category_id: int):
        self.id = category_id
        self.__load_db()

    def __load_db(self):
        row: tuple[Any, ...] | None = call_query(
            'SELECT * FROM categories WHERE id = %s',
            (self.id,)
        )

        if row is None:
            raise NotFoundException('Kategorii', self.id)

        print(row)

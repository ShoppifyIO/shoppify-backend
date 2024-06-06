from __future__ import annotations
import enum


class CategoryType(enum.Enum):
    SHOPPING_LIST = "ShoppingList"
    ITEM = "Item"

    def to_int(self) -> int:
        if self == CategoryType.SHOPPING_LIST:
            return 1
        if self == CategoryType.ITEM:
            return 2

        raise ValueError(f'Nie ma wartości int dla CategoryType = {self.name}')

    @staticmethod
    def from_str(name: str) -> CategoryType:
        if name == CategoryType.SHOPPING_LIST.value:
            return CategoryType.SHOPPING_LIST
        if name == CategoryType.ITEM.value:
            return CategoryType.ITEM

        raise ValueError(f'Nie ma CategoryType o wartości {name}')

    @staticmethod
    def from_int(value: int) -> CategoryType:
        if value == 1:
            return CategoryType.SHOPPING_LIST
        if value == 2:
            return CategoryType.ITEM

        raise ValueError(f'Nie ma CategoryType dla int = {value}')

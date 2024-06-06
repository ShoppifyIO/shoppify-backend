from rest.common.exceptions.abstract_exception import AbstractException


class NotFoundException(AbstractException):

    def __init__(self, object_name: str, object_id: int | str):
        super().__init__(404, NotFoundException.__create_message(object_name, object_id))

    @staticmethod
    def __create_message(object_name: str, object_id: int | str) -> str:
        if isinstance(object_id, int):
            return f'Nie znaleziono {object_name} o ID {object_id}'

        return f'Nie znaleziono {object_name} o nazwie {object_id}'

from rest.common.exceptions.abstract_exception import AbstractException


class NotFoundException(AbstractException):

    def __init__(self, object_name: str, object_id: int):
        super().__init__(404, f'Nie znaleziono {object_name} o ID {object_id}')

from rest.common.exceptions.abstract_exception import AbstractException


class MissingParamException(AbstractException):

    def __init__(self, param_name: str):
        super().__init__(400, f'Brakuje parametru: \'{param_name}\'')

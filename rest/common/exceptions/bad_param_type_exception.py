from rest.common.exceptions.abstract_exception import AbstractException


class BadParamTypeException(AbstractException):

    def __init__(self, param_name: str):
        super().__init__(400, f'Parametr {param_name} ma zły typ')

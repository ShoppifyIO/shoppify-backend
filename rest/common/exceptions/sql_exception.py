from rest.common.exceptions.abstract_exception import AbstractException


class SqlException(AbstractException):

    def __init__(self, pg_error: str):
        super().__init__(400, pg_error.split('\n')[0][7:])

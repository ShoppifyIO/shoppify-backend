from rest.common.exceptions.abstract_exception import AbstractException


class AuthException(AbstractException):
    """
    Exception returns 401 statuses.

    Used when a person is trying to access resource they are
    unauthorised to access.
    """

    def __init__(
            self,
            message: str
    ) -> None:
        super().__init__(401, message)
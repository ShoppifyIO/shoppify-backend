import json
from abc import ABC
from flask import Response


class AbstractException(Exception, ABC):

    status: int
    message: str

    def __init__(self, status: int, message: str):
        super().__init__(self)
        self.status = status
        self.message = message

    def to_response(self) -> Response:
        return Response(
            response=json.dumps({'error': self.message}, default=str),
            status=self.status,
            mimetype='application/json'
        )

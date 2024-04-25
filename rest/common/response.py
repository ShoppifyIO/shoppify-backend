import json
from typing import Dict

from flask import Response


def respond_created() -> Response:
    return respond(None, 201)


def respond(
        data: Dict[str, any] | str | None,
        status: int,
        mimetype: str = 'application/json'
) -> Response:
    if data is not None:
        return Response(
            response=json.dumps(data, default=str),
            status=status,
            mimetype=mimetype
        )

    response: Response = Response(status=status)
    response.headers['Content-Length'] = 0
    return response

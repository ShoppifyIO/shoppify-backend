import json
from typing import Dict, Any, List, Union

from flask import Response

JsonType = List[Dict[str, Any]] | Dict[str, Any] | str | None


def respond_created(data: JsonType) -> Response:
    return respond(data, 201)


def respond(
        data: JsonType,
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

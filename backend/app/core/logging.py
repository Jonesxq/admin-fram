from uuid import uuid4

from fastapi import Request


def get_request_id(request: Request) -> str:
    return request.headers.get("x-request-id") or str(uuid4())

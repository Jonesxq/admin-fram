from typing import Any
from uuid import uuid4


def success(data: Any = None, message: str = "ok", request_id: str | None = None) -> dict[str, Any]:
    return {
        "code": 0,
        "message": message,
        "data": data,
        "request_id": request_id or str(uuid4()),
    }

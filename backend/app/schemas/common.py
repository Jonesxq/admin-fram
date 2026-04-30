from typing import Any

from pydantic import BaseModel


class PageResponse(BaseModel):
    items: list[dict[str, Any]]
    total: int
    page: int = 1
    page_size: int = 20

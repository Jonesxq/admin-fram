from typing import Any

from sqlalchemy import func, inspect, select
from sqlalchemy.orm import Session

from app.schemas.common import PageResponse


def page_query(
    db: Session,
    model: type,
    page: int = 1,
    page_size: int = 20,
) -> PageResponse:
    safe_page = max(page, 1)
    safe_page_size = max(min(page_size, 100), 1)
    statement = select(model)
    if hasattr(model, "deleted_at"):
        statement = statement.where(model.deleted_at.is_(None))
    statement = statement.order_by(model.id)

    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = db.scalars(
        statement.offset((safe_page - 1) * safe_page_size).limit(safe_page_size),
    ).all()
    return PageResponse(
        items=[to_dict(item) for item in items],
        total=total,
        page=safe_page,
        page_size=safe_page_size,
    )


def to_dict(instance: object) -> dict[str, Any]:
    mapper = inspect(instance).mapper
    return {
        column.key: getattr(instance, column.key)
        for column in mapper.column_attrs
        if column.key != "password_hash"
    }

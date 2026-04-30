from collections.abc import Iterable
from typing import Any

from sqlalchemy import func, inspect, select
from sqlalchemy.sql.elements import UnaryExpression
from sqlalchemy.orm import Session

from app.models.system import Config, Dept, DictType, LoginLog, Menu, OperationLog, Post, Role, User
from app.schemas.common import PageResponse

LIST_FIELDS = {
    User: (
        "id",
        "username",
        "nickname",
        "email",
        "mobile",
        "dept_id",
        "status",
        "last_login_at",
    ),
    Role: ("id", "code", "name", "data_scope", "sort", "status"),
    Menu: (
        "id",
        "parent_id",
        "type",
        "title",
        "path",
        "component",
        "permission",
        "icon",
        "sort",
        "status",
    ),
    Dept: ("id", "parent_id", "ancestors", "name", "sort", "status"),
    Post: ("id", "code", "name", "sort", "status"),
    DictType: ("id", "code", "name", "status"),
    Config: ("id", "key", "name", "remark"),
    LoginLog: (
        "id",
        "username",
        "success",
        "message",
        "ip_address",
        "user_agent",
        "created_at",
    ),
    OperationLog: (
        "id",
        "username",
        "permission",
        "title",
        "method",
        "path",
        "ip_address",
        "success",
        "message",
        "created_at",
    ),
}


def page_query(
    db: Session,
    model: type,
    page: int = 1,
    page_size: int = 20,
    order_by: Iterable[UnaryExpression[Any]] | None = None,
) -> PageResponse:
    safe_page = max(page, 1)
    safe_page_size = max(min(page_size, 100), 1)
    statement = select(model)
    if hasattr(model, "deleted_at"):
        statement = statement.where(model.deleted_at.is_(None))
    if order_by is not None:
        statement = statement.order_by(*order_by)
    else:
        statement = statement.order_by(model.id)

    total = db.scalar(select(func.count()).select_from(statement.subquery())) or 0
    items = db.scalars(
        statement.offset((safe_page - 1) * safe_page_size).limit(safe_page_size),
    ).all()
    return PageResponse(
        items=[to_dict(item, LIST_FIELDS[model]) for item in items],
        total=total,
        page=safe_page,
        page_size=safe_page_size,
    )


def to_dict(instance: object, fields: Iterable[str]) -> dict[str, Any]:
    mapper = inspect(instance).mapper
    model_fields = {column.key for column in mapper.column_attrs}
    return {
        field: getattr(instance, field)
        for field in fields
        if field in model_fields
    }

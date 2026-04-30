from collections.abc import Iterable
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func, inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import UnaryExpression

from app.core.errors import AppError
from app.models.system import (
    Config,
    Dept,
    DictItem,
    DictType,
    LoginLog,
    Menu,
    OperationLog,
    Post,
    Role,
    User,
)
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
    DictItem: ("id", "dict_type_id", "value", "label", "sort", "status"),
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

UNIQUE_RELEASE_FIELDS = {
    User: {"username": 64},
    Role: {"code": 64},
    Post: {"code": 64},
    DictType: {"code": 64},
    Config: {"key": 128},
}


def create_item(db: Session, model: type, values: dict[str, Any]) -> Any:
    item = model(**values)
    db.add(item)
    flush_or_conflict(db)
    return item


def update_item(db: Session, model: type, item_id: int, values: dict[str, Any]) -> Any:
    item = get_active_item(db, model, item_id)
    for key, value in values.items():
        setattr(item, key, value)
    flush_or_conflict(db)
    return item


def soft_delete_item(db: Session, model: type, item_id: int) -> Any:
    item = get_active_item(db, model, item_id)
    if hasattr(model, "deleted_at"):
        item.deleted_at = datetime.now(timezone.utc)
        release_unique_values(model, item)
    else:
        db.delete(item)
    flush_or_conflict(db)
    return item


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


def to_safe_dict(instance: object) -> dict[str, Any]:
    return to_dict(instance, LIST_FIELDS[type(instance)])


def get_active_item(db: Session, model: type, item_id: int) -> Any:
    statement = select(model).where(model.id == item_id)
    if hasattr(model, "deleted_at"):
        statement = statement.where(model.deleted_at.is_(None))
    item = db.scalar(statement)
    if item is None:
        raise AppError(code=100404, message="资源不存在", status_code=404)
    return item


def flush_or_conflict(db: Session) -> None:
    try:
        db.flush()
    except IntegrityError as exc:
        raise AppError(code=100409, message="资源已存在", status_code=409) from exc


def release_unique_values(model: type, item: Any) -> None:
    for field, max_length in UNIQUE_RELEASE_FIELDS.get(model, {}).items():
        value = getattr(item, field, None)
        if not value:
            continue

        suffix = f"__deleted_{item.id}"
        prefix_length = max(max_length - len(suffix), 0)
        setattr(item, field, f"{value[:prefix_length]}{suffix}"[-max_length:])

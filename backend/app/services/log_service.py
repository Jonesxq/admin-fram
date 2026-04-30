from fastapi import Request
from sqlalchemy.orm import Session

from app.models.system import LoginLog, OperationLog, User
from app.schemas.common import PageResponse
from app.services.system_service import page_query


def log_operation(
    db: Session,
    *,
    user: User,
    permission: str,
    title: str,
    request: Request,
    success: bool,
    message: str | None = None,
) -> OperationLog:
    log = OperationLog(
        username=user.username,
        permission=permission,
        title=title,
        method=request.method,
        path=request.url.path,
        ip_address=request.client.host if request.client else None,
        success=success,
        message=message,
    )
    db.add(log)
    db.flush()
    return log


def list_login_logs(db: Session, page: int = 1, page_size: int = 20) -> PageResponse:
    return page_query(
        db,
        LoginLog,
        page,
        page_size,
        order_by=(LoginLog.created_at.desc(), LoginLog.id.desc()),
    )


def list_operation_logs(db: Session, page: int = 1, page_size: int = 20) -> PageResponse:
    return page_query(
        db,
        OperationLog,
        page,
        page_size,
        order_by=(OperationLog.created_at.desc(), OperationLog.id.desc()),
    )

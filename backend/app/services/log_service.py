from sqlalchemy.orm import Session

from app.models.system import LoginLog, OperationLog
from app.schemas.common import PageResponse
from app.services.system_service import page_query


def list_login_logs(db: Session, page: int = 1, page_size: int = 20) -> PageResponse:
    return page_query(db, LoginLog, page, page_size)


def list_operation_logs(db: Session, page: int = 1, page_size: int = 20) -> PageResponse:
    return page_query(db, OperationLog, page, page_size)

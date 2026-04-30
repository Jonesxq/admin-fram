from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_request_id
from app.core.responses import success
from app.models.system import Config, Dept, DictType, Menu, Post, Role, User
from app.services.log_service import list_login_logs, list_operation_logs
from app.services.rbac_service import require_permission
from app.services.system_service import page_query

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/users", dependencies=[Depends(require_permission("system:user:list"))])
def list_users(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, User, page, page_size).model_dump(), request_id=get_request_id(request))


@router.get("/roles", dependencies=[Depends(require_permission("system:role:list"))])
def list_roles(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, Role, page, page_size).model_dump(), request_id=get_request_id(request))


@router.get("/menus", dependencies=[Depends(require_permission("system:menu:list"))])
def list_menus(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, Menu, page, page_size).model_dump(), request_id=get_request_id(request))


@router.get("/depts", dependencies=[Depends(require_permission("system:dept:list"))])
def list_depts(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, Dept, page, page_size).model_dump(), request_id=get_request_id(request))


@router.get("/posts", dependencies=[Depends(require_permission("system:post:list"))])
def list_posts(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, Post, page, page_size).model_dump(), request_id=get_request_id(request))


@router.get("/dict-types", dependencies=[Depends(require_permission("system:dict:list"))])
def list_dict_types(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, DictType, page, page_size).model_dump(), request_id=get_request_id(request))


@router.get("/configs", dependencies=[Depends(require_permission("system:config:list"))])
def list_configs(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, Config, page, page_size).model_dump(), request_id=get_request_id(request))


@router.get("/login-logs", dependencies=[Depends(require_permission("system:login-log:list"))])
def get_login_logs(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(list_login_logs(db, page, page_size).model_dump(), request_id=get_request_id(request))


@router.get(
    "/operation-logs",
    dependencies=[Depends(require_permission("system:operation-log:list"))],
)
def get_operation_logs(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(list_operation_logs(db, page, page_size).model_dump(), request_id=get_request_id(request))

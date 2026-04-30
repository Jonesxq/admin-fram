from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_request_id
from app.core.responses import success
from app.core.security import hash_password
from app.models.system import Config, Dept, DictItem, DictType, Menu, Post, Role, User
from app.schemas import system as system_schemas
from app.services.log_service import list_login_logs, list_operation_logs, log_operation
from app.services.rbac_service import require_permission
from app.services.system_service import create_item, page_query, soft_delete_item, to_safe_dict, update_item

router = APIRouter(prefix="/system", tags=["system"])


def _values(payload: BaseModel) -> dict[str, Any]:
    return payload.model_dump(exclude_unset=True)


def _create(
    request: Request,
    db: Session,
    current_user: User,
    model: type,
    values: dict[str, Any],
    permission: str,
    title: str,
) -> dict:
    try:
        item = create_item(db, model, values)
        log_operation(
            db,
            user=current_user,
            permission=permission,
            title=title,
            request=request,
            success=True,
        )
        db.commit()
        db.refresh(item)
    except Exception:
        db.rollback()
        raise
    return success(to_safe_dict(item), request_id=get_request_id(request))


def _update(
    request: Request,
    db: Session,
    current_user: User,
    model: type,
    item_id: int,
    values: dict[str, Any],
    permission: str,
    title: str,
) -> dict:
    try:
        item = update_item(db, model, item_id, values)
        log_operation(
            db,
            user=current_user,
            permission=permission,
            title=title,
            request=request,
            success=True,
        )
        db.commit()
        db.refresh(item)
    except Exception:
        db.rollback()
        raise
    return success(to_safe_dict(item), request_id=get_request_id(request))


def _delete(
    request: Request,
    db: Session,
    current_user: User,
    model: type,
    item_id: int,
    permission: str,
    title: str,
) -> dict:
    try:
        soft_delete_item(db, model, item_id)
        log_operation(
            db,
            user=current_user,
            permission=permission,
            title=title,
            request=request,
            success=True,
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    return success({"id": item_id}, request_id=get_request_id(request))


@router.get("/users", dependencies=[Depends(require_permission("system:user:list"))])
def list_users(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, User, page, page_size).model_dump(), request_id=get_request_id(request))


@router.post("/users")
def create_user(
    request: Request,
    payload: system_schemas.UserCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:user:create"))],
) -> dict:
    values = _values(payload)
    values["password_hash"] = hash_password(values.pop("password"))
    return _create(request, db, current_user, User, values, "system:user:create", "创建用户")


@router.put("/users/{item_id}")
def update_user(
    request: Request,
    item_id: int,
    payload: system_schemas.UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:user:update"))],
) -> dict:
    return _update(
        request,
        db,
        current_user,
        User,
        item_id,
        _values(payload),
        "system:user:update",
        "修改用户",
    )


@router.delete("/users/{item_id}")
def delete_user(
    request: Request,
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:user:delete"))],
) -> dict:
    return _delete(request, db, current_user, User, item_id, "system:user:delete", "删除用户")


@router.get("/roles", dependencies=[Depends(require_permission("system:role:list"))])
def list_roles(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, Role, page, page_size).model_dump(), request_id=get_request_id(request))


@router.post("/roles")
def create_role(
    request: Request,
    payload: system_schemas.RoleCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:role:create"))],
) -> dict:
    return _create(request, db, current_user, Role, _values(payload), "system:role:create", "创建角色")


@router.put("/roles/{item_id}")
def update_role(
    request: Request,
    item_id: int,
    payload: system_schemas.RoleUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:role:update"))],
) -> dict:
    return _update(
        request,
        db,
        current_user,
        Role,
        item_id,
        _values(payload),
        "system:role:update",
        "修改角色",
    )


@router.delete("/roles/{item_id}")
def delete_role(
    request: Request,
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:role:delete"))],
) -> dict:
    return _delete(request, db, current_user, Role, item_id, "system:role:delete", "删除角色")


@router.get("/menus", dependencies=[Depends(require_permission("system:menu:list"))])
def list_menus(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, Menu, page, page_size).model_dump(), request_id=get_request_id(request))


@router.post("/menus")
def create_menu(
    request: Request,
    payload: system_schemas.MenuCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:menu:create"))],
) -> dict:
    return _create(request, db, current_user, Menu, _values(payload), "system:menu:create", "创建菜单")


@router.put("/menus/{item_id}")
def update_menu(
    request: Request,
    item_id: int,
    payload: system_schemas.MenuUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:menu:update"))],
) -> dict:
    return _update(
        request,
        db,
        current_user,
        Menu,
        item_id,
        _values(payload),
        "system:menu:update",
        "修改菜单",
    )


@router.delete("/menus/{item_id}")
def delete_menu(
    request: Request,
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:menu:delete"))],
) -> dict:
    return _delete(request, db, current_user, Menu, item_id, "system:menu:delete", "删除菜单")


@router.get("/depts", dependencies=[Depends(require_permission("system:dept:list"))])
def list_depts(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, Dept, page, page_size).model_dump(), request_id=get_request_id(request))


@router.post("/depts")
def create_dept(
    request: Request,
    payload: system_schemas.DeptCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:dept:create"))],
) -> dict:
    return _create(request, db, current_user, Dept, _values(payload), "system:dept:create", "创建部门")


@router.put("/depts/{item_id}")
def update_dept(
    request: Request,
    item_id: int,
    payload: system_schemas.DeptUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:dept:update"))],
) -> dict:
    return _update(
        request,
        db,
        current_user,
        Dept,
        item_id,
        _values(payload),
        "system:dept:update",
        "修改部门",
    )


@router.delete("/depts/{item_id}")
def delete_dept(
    request: Request,
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:dept:delete"))],
) -> dict:
    return _delete(request, db, current_user, Dept, item_id, "system:dept:delete", "删除部门")


@router.get("/posts", dependencies=[Depends(require_permission("system:post:list"))])
def list_posts(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, Post, page, page_size).model_dump(), request_id=get_request_id(request))


@router.post("/posts")
def create_post(
    request: Request,
    payload: system_schemas.PostCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:post:create"))],
) -> dict:
    return _create(request, db, current_user, Post, _values(payload), "system:post:create", "创建岗位")


@router.put("/posts/{item_id}")
def update_post(
    request: Request,
    item_id: int,
    payload: system_schemas.PostUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:post:update"))],
) -> dict:
    return _update(
        request,
        db,
        current_user,
        Post,
        item_id,
        _values(payload),
        "system:post:update",
        "修改岗位",
    )


@router.delete("/posts/{item_id}")
def delete_post(
    request: Request,
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:post:delete"))],
) -> dict:
    return _delete(request, db, current_user, Post, item_id, "system:post:delete", "删除岗位")


@router.get("/dict-types", dependencies=[Depends(require_permission("system:dict:list"))])
def list_dict_types(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, DictType, page, page_size).model_dump(), request_id=get_request_id(request))


@router.post("/dict-types")
def create_dict_type(
    request: Request,
    payload: system_schemas.DictTypeCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:dict:create"))],
) -> dict:
    return _create(
        request,
        db,
        current_user,
        DictType,
        _values(payload),
        "system:dict:create",
        "创建字典类型",
    )


@router.put("/dict-types/{item_id}")
def update_dict_type(
    request: Request,
    item_id: int,
    payload: system_schemas.DictTypeUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:dict:update"))],
) -> dict:
    return _update(
        request,
        db,
        current_user,
        DictType,
        item_id,
        _values(payload),
        "system:dict:update",
        "修改字典类型",
    )


@router.delete("/dict-types/{item_id}")
def delete_dict_type(
    request: Request,
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:dict:delete"))],
) -> dict:
    return _delete(request, db, current_user, DictType, item_id, "system:dict:delete", "删除字典类型")


@router.get("/dict-items", dependencies=[Depends(require_permission("system:dict:list"))])
def list_dict_items(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, DictItem, page, page_size).model_dump(), request_id=get_request_id(request))


@router.post("/dict-items")
def create_dict_item(
    request: Request,
    payload: system_schemas.DictItemCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:dict:create"))],
) -> dict:
    return _create(
        request,
        db,
        current_user,
        DictItem,
        _values(payload),
        "system:dict:create",
        "创建字典项",
    )


@router.put("/dict-items/{item_id}")
def update_dict_item(
    request: Request,
    item_id: int,
    payload: system_schemas.DictItemUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:dict:update"))],
) -> dict:
    return _update(
        request,
        db,
        current_user,
        DictItem,
        item_id,
        _values(payload),
        "system:dict:update",
        "修改字典项",
    )


@router.delete("/dict-items/{item_id}")
def delete_dict_item(
    request: Request,
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:dict:delete"))],
) -> dict:
    return _delete(request, db, current_user, DictItem, item_id, "system:dict:delete", "删除字典项")


@router.get("/configs", dependencies=[Depends(require_permission("system:config:list"))])
def list_configs(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    page: int = 1,
    page_size: int = 20,
) -> dict:
    return success(page_query(db, Config, page, page_size).model_dump(), request_id=get_request_id(request))


@router.post("/configs")
def create_config(
    request: Request,
    payload: system_schemas.ConfigCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:config:create"))],
) -> dict:
    return _create(
        request,
        db,
        current_user,
        Config,
        _values(payload),
        "system:config:create",
        "创建配置",
    )


@router.put("/configs/{item_id}")
def update_config(
    request: Request,
    item_id: int,
    payload: system_schemas.ConfigUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:config:update"))],
) -> dict:
    return _update(
        request,
        db,
        current_user,
        Config,
        item_id,
        _values(payload),
        "system:config:update",
        "修改配置",
    )


@router.delete("/configs/{item_id}")
def delete_config(
    request: Request,
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_permission("system:config:delete"))],
) -> dict:
    return _delete(request, db, current_user, Config, item_id, "system:config:delete", "删除配置")


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

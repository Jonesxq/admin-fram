from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import create_access_token, verify_password
from app.models.system import Menu, User
from app.schemas.auth import TokenResponse


def authenticate(db: Session, username: str, password: str) -> User:
    user = db.scalar(select(User).where(User.username == username))
    if user is None or user.status != "enabled":
        raise invalid_credentials_error()

    if not verify_password(password, user.password_hash):
        raise invalid_credentials_error()

    return user


def build_token(user: User) -> TokenResponse:
    return TokenResponse(access_token=create_access_token(str(user.id)))


def build_current_user(user: User) -> dict:
    enabled_roles = [role for role in user.roles if role.status == "enabled"]
    permissions = {
        menu.permission
        for role in enabled_roles
        for menu in role.menus
        if menu.status == "enabled" and menu.permission
    }
    menus_by_id = {
        menu.id: serialize_menu(menu)
        for role in enabled_roles
        for menu in role.menus
        if menu.status == "enabled" and menu.type == "menu"
    }

    return {
        "user": {"id": user.id, "username": user.username, "nickname": user.nickname},
        "roles": sorted({role.code for role in enabled_roles}),
        "permissions": sorted(permissions),
        "menus": sorted(menus_by_id.values(), key=lambda item: (item["sort"], item["id"])),
    }


def invalid_credentials_error() -> AppError:
    return AppError(code=100401, message="账号或密码错误", status_code=401)


def serialize_menu(menu: Menu) -> dict:
    return {
        "id": menu.id,
        "parent_id": menu.parent_id,
        "type": menu.type,
        "title": menu.title,
        "path": menu.path,
        "component": menu.component,
        "permission": menu.permission,
        "icon": menu.icon,
        "sort": menu.sort,
    }

from app.core.deps import require_permission as require_permission
from app.models.system import User


def user_permissions(user: User) -> set[str]:
    return {
        menu.permission
        for role in enabled_roles(user)
        for menu in role.menus
        if menu.status == "enabled" and menu.deleted_at is None and menu.permission
    }


def enabled_roles(user: User):
    return [
        role
        for role in user.roles
        if role.status == "enabled" and role.deleted_at is None
    ]


def is_admin(user: User) -> bool:
    return any(role.code == "admin" for role in enabled_roles(user))

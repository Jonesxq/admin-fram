import os

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.system import Menu, Role, User


MENU_SEEDS = [
    {"title": "Dashboard", "path": "/dashboard", "component": "Dashboard", "permission": "dashboard"},
    {"title": "用户管理", "path": "/system/users", "component": "system/User", "permission": "system:user"},
    {"title": "角色管理", "path": "/system/roles", "component": "system/Role", "permission": "system:role"},
    {"title": "菜单管理", "path": "/system/menus", "component": "system/Menu", "permission": "system:menu"},
    {"title": "部门管理", "path": "/system/depts", "component": "system/Dept", "permission": "system:dept"},
    {"title": "岗位管理", "path": "/system/posts", "component": "system/Post", "permission": "system:post"},
    {
        "title": "字典管理",
        "path": "/system/dicts",
        "component": "system/Dict",
        "permission": "system:dict",
    },
    {
        "title": "参数配置",
        "path": "/system/configs",
        "component": "system/Config",
        "permission": "system:config",
    },
    {
        "title": "登录日志",
        "path": "/monitor/login-logs",
        "component": "monitor/LoginLog",
        "permission": "monitor:login-log",
    },
    {
        "title": "操作日志",
        "path": "/monitor/operation-logs",
        "component": "monitor/OperationLog",
        "permission": "monitor:operation-log",
    },
]

DEFAULT_INITIAL_ADMIN_PASSWORD = "Admin123!"
INITIAL_ADMIN_PASSWORD_ENV = "INITIAL_ADMIN_PASSWORD"
ALLOW_DEFAULT_ADMIN_PASSWORD_ENV = "ALLOW_DEFAULT_ADMIN_PASSWORD"
TRUTHY_ENV_VALUES = {"1", "true", "yes", "on"}


def get_initial_admin_password() -> str:
    password = os.getenv(INITIAL_ADMIN_PASSWORD_ENV, "").strip()
    if password and password != DEFAULT_INITIAL_ADMIN_PASSWORD:
        return password

    allow_default = os.getenv(ALLOW_DEFAULT_ADMIN_PASSWORD_ENV, "").strip().lower()
    if allow_default in TRUTHY_ENV_VALUES:
        print(
            "WARNING: using local-development-only default admin password. "
            f"Set a strong {INITIAL_ADMIN_PASSWORD_ENV} outside local development.",
        )
        return DEFAULT_INITIAL_ADMIN_PASSWORD

    raise RuntimeError(
        f"Refusing to seed admin with the public default password. Set a strong "
        f"{INITIAL_ADMIN_PASSWORD_ENV}, or set {ALLOW_DEFAULT_ADMIN_PASSWORD_ENV}=1 "
        "only for local development.",
    )


def get_or_create_admin_role(db: Session) -> Role:
    role = db.scalar(select(Role).where(Role.code == "admin"))
    if role is not None:
        return role

    role = Role(code="admin", name="管理员", data_scope="all", sort=0, status="enabled")
    db.add(role)
    db.flush()
    return role


def get_or_create_admin_user(db: Session, role: Role) -> User:
    user = db.scalar(select(User).where(User.username == "admin"))
    if user is None:
        user = User(
            username="admin",
            password_hash=hash_password(get_initial_admin_password()),
            nickname="管理员",
            status="enabled",
        )
        db.add(user)
        db.flush()

    if role not in user.roles:
        user.roles.append(role)
    return user


def seed_menus(db: Session, role: Role) -> None:
    for index, item in enumerate(MENU_SEEDS):
        menu = get_seed_menu(db, item)
        if menu is None:
            menu = Menu(
                type="menu",
                title=item["title"],
                path=item["path"],
                component=item["component"],
                permission=item["permission"],
                icon=None,
                sort=index,
                status="enabled",
            )
            db.add(menu)
            db.flush()

        if role not in menu.roles:
            menu.roles.append(role)


def get_seed_menu(db: Session, item: dict[str, str]) -> Menu | None:
    permission = item.get("permission")
    if permission:
        return db.scalar(select(Menu).where(Menu.permission == permission))

    return db.scalar(select(Menu).where(Menu.path == item["path"]))


def seed(db: Session) -> None:
    role = get_or_create_admin_role(db)
    get_or_create_admin_user(db, role)
    seed_menus(db, role)


def main() -> None:
    with SessionLocal() as db:
        seed(db)
        db.commit()


if __name__ == "__main__":
    main()

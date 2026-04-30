from datetime import datetime, timezone

import pytest

from app.core.errors import AppError
from app.models.system import Menu, Role, User
from app.services.rbac_service import require_permission, user_permissions


def test_user_permissions_includes_enabled_role_menu_permissions() -> None:
    user = User(
        username="admin",
        password_hash="hash",
        nickname="Administrator",
        roles=[
            Role(
                code="admin",
                name="Administrator",
                status="enabled",
                menus=[
                    Menu(
                        type="button",
                        title="用户查询",
                        permission="system:user:list",
                        status="enabled",
                    ),
                ],
            ),
        ],
    )

    assert user_permissions(user) == {"system:user:list"}


def test_user_permissions_ignores_disabled_and_soft_deleted_grants() -> None:
    user = User(
        username="user",
        password_hash="hash",
        nickname="User",
        roles=[
            Role(
                code="disabled",
                name="Disabled",
                status="disabled",
                menus=[
                    Menu(
                        type="button",
                        title="Disabled",
                        permission="disabled:permission",
                        status="enabled",
                    ),
                ],
            ),
            Role(
                code="deleted",
                name="Deleted",
                status="enabled",
                deleted_at=datetime.now(timezone.utc),
                menus=[
                    Menu(
                        type="button",
                        title="Deleted",
                        permission="deleted:permission",
                        status="enabled",
                    ),
                ],
            ),
            Role(
                code="viewer",
                name="Viewer",
                status="enabled",
                menus=[
                    Menu(
                        type="button",
                        title="Disabled menu",
                        permission="menu:disabled",
                        status="disabled",
                    ),
                    Menu(
                        type="button",
                        title="Deleted menu",
                        permission="menu:deleted",
                        status="enabled",
                        deleted_at=datetime.now(timezone.utc),
                    ),
                ],
            ),
        ],
    )

    assert user_permissions(user) == set()


def test_require_permission_allows_admin_role_without_specific_permission() -> None:
    user = User(
        username="admin",
        password_hash="hash",
        nickname="Administrator",
        roles=[Role(code="admin", name="Administrator", status="enabled", menus=[])],
    )

    assert require_permission("system:user:list")(user) is user


def test_require_permission_allows_user_with_permission() -> None:
    user = User(
        username="operator",
        password_hash="hash",
        nickname="Operator",
        roles=[
            Role(
                code="operator",
                name="Operator",
                status="enabled",
                menus=[
                    Menu(
                        type="button",
                        title="用户查询",
                        permission="system:user:list",
                        status="enabled",
                    ),
                ],
            ),
        ],
    )

    assert require_permission("system:user:list")(user) is user


def test_require_permission_rejects_user_without_permission() -> None:
    user = User(
        username="viewer",
        password_hash="hash",
        nickname="Viewer",
        roles=[Role(code="viewer", name="Viewer", status="enabled", menus=[])],
    )

    with pytest.raises(AppError) as exc_info:
        require_permission("system:user:list")(user)

    assert exc_info.value.code == 100403
    assert exc_info.value.message == "无权限"
    assert exc_info.value.status_code == 403

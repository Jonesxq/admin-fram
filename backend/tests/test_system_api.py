from collections.abc import Generator
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.core.security import hash_password
from app.main import app
from app.models.base import Base
from app.models.system import (
    Config,
    Dept,
    DictType,
    LoginLog,
    Menu,
    OperationLog,
    Post,
    Role,
    User,
)


@pytest.fixture()
def system_client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    with session_factory() as db:
        seed_system(db)
        db.commit()

    def override_get_db() -> Generator[Session, None, None]:
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_admin_with_system_user_list_can_access_protected_user_list(
    system_client: TestClient,
) -> None:
    response = system_client.get(
        "/api/v1/system/users",
        headers=auth_headers(system_client),
    )

    assert response.status_code == 200
    assert response.json()["code"] == 0


def test_system_users_returns_page_without_password_hash(system_client: TestClient) -> None:
    response = system_client.get(
        "/api/v1/system/users",
        headers=auth_headers(system_client),
    )

    data = response.json()["data"]
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total"] == 2
    assert [item["username"] for item in data["items"]] == ["admin", "operator"]
    assert all("password_hash" not in item for item in data["items"])


def test_system_roles_returns_admin_role(system_client: TestClient) -> None:
    response = system_client.get(
        "/api/v1/system/roles",
        headers=auth_headers(system_client),
    )

    data = response.json()["data"]
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total"] == 1
    assert data["items"][0]["code"] == "admin"


@pytest.mark.parametrize(
    "path",
    [
        "/api/v1/system/menus",
        "/api/v1/system/depts",
        "/api/v1/system/posts",
        "/api/v1/system/dict-types",
        "/api/v1/system/configs",
        "/api/v1/system/login-logs",
        "/api/v1/system/operation-logs",
    ],
)
def test_system_list_endpoints_return_page_shape(system_client: TestClient, path: str) -> None:
    response = system_client.get(path, headers=auth_headers(system_client))

    assert response.status_code == 200
    data = response.json()["data"]
    assert set(data) == {"items", "total", "page", "page_size"}
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert isinstance(data["items"], list)


def auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin123!"},
    )
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def seed_system(db: Session) -> None:
    permissions = [
        Menu(type="button", title=title, permission=permission, status="enabled")
        for title, permission in [
            ("用户查询", "system:user:list"),
            ("角色查询", "system:role:list"),
            ("菜单查询", "system:menu:list"),
            ("部门查询", "system:dept:list"),
            ("岗位查询", "system:post:list"),
            ("字典查询", "system:dict:list"),
            ("配置查询", "system:config:list"),
            ("登录日志查询", "system:login-log:list"),
            ("操作日志查询", "system:operation-log:list"),
        ]
    ]
    role = Role(
        code="admin",
        name="Administrator",
        status="enabled",
        menus=permissions,
    )
    admin = User(
        username="admin",
        password_hash=hash_password("Admin123!"),
        nickname="Administrator",
        status="enabled",
        roles=[role],
    )
    operator = User(
        username="operator",
        password_hash=hash_password("Operator123!"),
        nickname="Operator",
        status="enabled",
    )
    deleted_user = User(
        username="deleted",
        password_hash=hash_password("Deleted123!"),
        nickname="Deleted",
        status="enabled",
        deleted_at=datetime.now(timezone.utc),
    )
    db.add_all([
        admin,
        operator,
        deleted_user,
        Dept(name="研发部", status="enabled"),
        Post(code="dev", name="Developer", status="enabled"),
        DictType(code="sys_status", name="状态", status="enabled"),
        Config(key="site.name", value="Admin", name="站点名称"),
        LoginLog(username="admin", success=True),
        OperationLog(username="admin", title="用户查询", permission="system:user:list"),
    ])

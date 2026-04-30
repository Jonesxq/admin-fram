from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.core.security import hash_password
from app.main import app
from app.models.base import Base
from app.models.system import Menu, Role, User


@pytest.fixture()
def auth_client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    with session_factory() as db:
        seed_admin(db)
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


def test_login_with_correct_credentials_returns_access_token(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin123!"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 0
    assert body["data"]["access_token"]
    assert body["data"]["token_type"] == "bearer"


def test_me_without_token_returns_401(auth_client: TestClient) -> None:
    response = auth_client.get("/api/v1/auth/me")

    assert response.status_code == 401
    assert response.json()["code"] == 100401


def test_me_with_admin_token_returns_current_user_payload(auth_client: TestClient) -> None:
    login_response = auth_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin123!"},
    )
    token = login_response.json()["data"]["access_token"]

    response = auth_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["data"] == {
        "user": {"id": 1, "username": "admin", "nickname": "Administrator"},
        "roles": ["admin"],
        "permissions": ["system:user:list"],
        "menus": [],
    }


def seed_admin(db: Session) -> None:
    permission = Menu(
        type="button",
        title="用户查询",
        permission="system:user:list",
        sort=0,
        status="enabled",
    )
    role = Role(code="admin", name="Administrator", status="enabled", menus=[permission])
    user = User(
        username="admin",
        password_hash=hash_password("Admin123!"),
        nickname="Administrator",
        status="enabled",
        roles=[role],
    )
    db.add(user)

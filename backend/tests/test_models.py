import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import bcrypt
import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker

from app.core.security import hash_password
from app.models.base import Base
from app.models import system
from app.seed import MENU_SEEDS, seed

SYSTEM_LIST_PERMISSIONS = {
    "system:user:list",
    "system:role:list",
    "system:menu:list",
    "system:dept:list",
    "system:post:list",
    "system:dict:list",
    "system:config:list",
    "system:login-log:list",
    "system:operation-log:list",
}
SYSTEM_WRITE_PERMISSIONS = {
    f"system:{resource}:{action}"
    for resource in ("user", "role", "menu", "dept", "post", "dict", "config")
    for action in ("create", "update", "delete")
}
SYSTEM_PERMISSIONS = SYSTEM_LIST_PERMISSIONS | SYSTEM_WRITE_PERMISSIONS


@pytest.fixture(autouse=True)
def isolate_seed_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.seed.settings",
        SimpleNamespace(
            initial_admin_password="",
            allow_default_admin_password=False,
        ),
    )


def test_system_tables_are_registered() -> None:
    table_names = set(Base.metadata.tables.keys())

    assert "sys_user" in table_names
    assert "sys_role" in table_names
    assert "sys_menu" in table_names
    assert "sys_dept" in table_names
    assert "sys_post" in table_names
    assert "sys_dict_type" in table_names
    assert "sys_dict_item" in table_names
    assert "sys_config" in table_names
    assert "sys_login_log" in table_names
    assert "sys_operation_log" in table_names
    assert system.User.__tablename__ == "sys_user"


def test_hash_password_uses_bcrypt_hash() -> None:
    password_hash = hash_password("Admin123!")

    assert password_hash != "Admin123!"
    assert bcrypt.checkpw("Admin123!".encode("utf-8"), password_hash.encode("utf-8"))


def test_seed_is_idempotent_and_uses_stable_menu_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("INITIAL_ADMIN_PASSWORD", "Strong-Local-Only-Password-123!")
    monkeypatch.delenv("ALLOW_DEFAULT_ADMIN_PASSWORD", raising=False)

    with seed_session() as session:
        seed(session)
        menu = session.scalar(
            select(system.Menu).where(system.Menu.permission == "system:user:list"),
        )
        assert menu is not None
        menu.title = "用户管理-改名"
        session.commit()

        seed(session)
        session.commit()

        admin_user_count = session.scalar(
            select(func.count()).select_from(system.User).where(system.User.username == "admin"),
        )
        admin_role_count = session.scalar(
            select(func.count()).select_from(system.Role).where(system.Role.code == "admin"),
        )
        menu_count = session.scalar(select(func.count()).select_from(system.Menu))
        admin_role = session.scalar(select(system.Role).where(system.Role.code == "admin"))

        assert admin_user_count == 1
        assert admin_role_count == 1
        assert menu_count == 31
        assert admin_role is not None
        assert len(admin_role.menus) == 31


def test_seed_admin_role_has_system_permissions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("INITIAL_ADMIN_PASSWORD", "Strong-Local-Only-Password-123!")
    monkeypatch.delenv("ALLOW_DEFAULT_ADMIN_PASSWORD", raising=False)

    with seed_session() as session:
        seed(session)
        session.commit()

        admin_role = session.scalar(select(system.Role).where(system.Role.code == "admin"))
        assert admin_role is not None
        permissions = {menu.permission for menu in admin_role.menus}

        assert SYSTEM_PERMISSIONS <= permissions
        assert {item["permission"] for item in MENU_SEEDS} == {
            "dashboard:view",
            *SYSTEM_PERMISSIONS,
        }


def test_seed_uses_strong_env_password_without_allow_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("INITIAL_ADMIN_PASSWORD", "Strong-Local-Only-Password-123!")
    monkeypatch.delenv("ALLOW_DEFAULT_ADMIN_PASSWORD", raising=False)

    with seed_session() as session:
        seed(session)
        session.commit()

        admin_user = session.scalar(select(system.User).where(system.User.username == "admin"))

        assert admin_user is not None
        assert bcrypt.checkpw(
            "Strong-Local-Only-Password-123!".encode("utf-8"),
            admin_user.password_hash.encode("utf-8"),
        )


@pytest.mark.parametrize("password", [None, "", "Admin123!"])
def test_seed_rejects_missing_or_default_password_without_allow_flag(
    password: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if password is None:
        monkeypatch.delenv("INITIAL_ADMIN_PASSWORD", raising=False)
    else:
        monkeypatch.setenv("INITIAL_ADMIN_PASSWORD", password)
    monkeypatch.delenv("ALLOW_DEFAULT_ADMIN_PASSWORD", raising=False)

    with seed_session() as session:
        with pytest.raises(RuntimeError, match="INITIAL_ADMIN_PASSWORD"):
            seed(session)


@pytest.mark.parametrize("allow_value", ["1", "true", "yes", "on"])
def test_seed_allows_default_password_with_explicit_opt_in(
    allow_value: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("INITIAL_ADMIN_PASSWORD", "Admin123!")
    monkeypatch.setenv("ALLOW_DEFAULT_ADMIN_PASSWORD", allow_value)

    with seed_session() as session:
        seed(session)
        session.commit()
        seed(session)
        session.commit()

        admin_user_count = session.scalar(
            select(func.count()).select_from(system.User).where(system.User.username == "admin"),
        )
        admin_user = session.scalar(select(system.User).where(system.User.username == "admin"))
        menu_count = session.scalar(select(func.count()).select_from(system.Menu))

        assert admin_user_count == 1
        assert menu_count == 31
        assert admin_user is not None
        assert bcrypt.checkpw("Admin123!".encode("utf-8"), admin_user.password_hash.encode("utf-8"))


def test_alembic_upgrade_and_downgrade_against_file_sqlite(tmp_path: Path) -> None:
    database_path = tmp_path / "alembic_smoke.db"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite+pysqlite:///{database_path.as_posix()}"
    env.pop("ALLOW_IN_MEMORY_ALEMBIC", None)

    upgrade = run_alembic("upgrade", "head", env=env)
    downgrade = run_alembic("downgrade", "base", env=env)

    assert upgrade.returncode == 0, upgrade.stderr
    assert downgrade.returncode == 0, downgrade.stderr


def test_alembic_rejects_in_memory_sqlite_without_escape_hatch() -> None:
    env = os.environ.copy()
    env["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    env.pop("ALLOW_IN_MEMORY_ALEMBIC", None)

    result = run_alembic("upgrade", "head", env=env)

    assert result.returncode != 0
    assert "in-memory" in result.stderr


def run_alembic(*args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        check=False,
        text=True,
    )


def seed_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return session_factory()

import os
import subprocess
import sys
from pathlib import Path

import bcrypt
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker

from app.core.security import hash_password
from app.models.base import Base
from app.models import system
from app.seed import seed


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


def test_seed_is_idempotent_and_uses_stable_menu_identity() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    with session_factory() as session:
        seed(session)
        menu = session.scalar(
            select(system.Menu).where(system.Menu.permission == "system:user"),
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
        assert menu_count == 10
        assert admin_role is not None
        assert len(admin_role.menus) == 10


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

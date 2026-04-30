# Admin Framework MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a runnable open-source admin framework MVP with Vue 3 + Element Plus frontend, FastAPI backend, MySQL persistence, JWT authentication, RBAC, core system management modules, docs, and local quick start.

**Architecture:** Use a Monorepo with `frontend/`, `backend/`, `docs/`, and root infrastructure files. Backend owns authentication, RBAC, migrations, seed data, and REST APIs. Frontend owns the SaaS-style admin shell, auth flow, route guards, permission rendering, and system management screens.

**Tech Stack:** Vue 3, Vite, TypeScript, Element Plus, Pinia, Vue Router, Axios, Vitest, FastAPI, Pydantic, SQLAlchemy, Alembic, PyMySQL, Pytest, Ruff, MySQL, Docker Compose.

---

## Scope Check

The approved spec covers multiple subsystems. This plan intentionally implements a single coherent MVP release instead of one unbounded platform build. Complex data permission filtering, code generation, multi-tenancy, notification center, visual page builder, and full OAuth2/OIDC support are excluded from implementation tasks and documented as roadmap items.

## Target File Structure

```text
/
  .editorconfig
  .env.example
  .gitignore
  docker-compose.yml
  README.md
  LICENSE
  CONTRIBUTING.md
  CHANGELOG.md
  frontend/
    package.json
    index.html
    vite.config.ts
    tsconfig.json
    src/
      main.ts
      App.vue
      styles/
        element.scss
        layout.scss
      router/
        index.ts
        static-routes.ts
        dynamic-routes.ts
      stores/
        auth.ts
        tabs.ts
        app.ts
      api/
        client.ts
        auth.ts
        system.ts
      layouts/
        AdminLayout.vue
        components/
          SidebarMenu.vue
          TopBar.vue
          TagsView.vue
      components/
        PermissionButton.vue
        PageTable.vue
      views/
        login/LoginView.vue
        dashboard/DashboardView.vue
        errors/ForbiddenView.vue
        errors/NotFoundView.vue
        errors/ServerErrorView.vue
        system/UserView.vue
        system/RoleView.vue
        system/MenuView.vue
        system/DeptView.vue
        system/PostView.vue
        system/DictView.vue
        system/ConfigView.vue
        system/LoginLogView.vue
        system/OperationLogView.vue
        examples/ListView.vue
        examples/FormView.vue
        examples/DetailView.vue
      tests/
        permission.spec.ts
        auth-store.spec.ts
  backend/
    pyproject.toml
    alembic.ini
    .env.example
    app/
      main.py
      api/
        v1/
          router.py
          auth.py
          system.py
      core/
        config.py
        database.py
        errors.py
        responses.py
        security.py
        deps.py
        logging.py
      models/
        base.py
        system.py
      schemas/
        common.py
        auth.py
        system.py
      services/
        auth_service.py
        rbac_service.py
        system_service.py
        log_service.py
      seed.py
    migrations/
      env.py
      versions/
    tests/
      conftest.py
      test_health.py
      test_auth.py
      test_rbac.py
      test_system_api.py
  docs/
    guide/
      quick-start.md
      architecture.md
      permission-model.md
      add-module.md
      deployment.md
```

## Task 1: Repository Baseline and Local Infrastructure

**Files:**
- Create: `.editorconfig`
- Modify: `.gitignore`
- Create: `.env.example`
- Create: `docker-compose.yml`
- Create: `README.md`
- Create: `LICENSE`
- Create: `CONTRIBUTING.md`
- Create: `CHANGELOG.md`

- [ ] **Step 1: Write repository metadata files**

Create `.editorconfig`:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4
```

Create `.env.example`:

```env
APP_NAME=Open Admin
FRONTEND_PORT=5173
BACKEND_PORT=8000
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=open_admin
MYSQL_USER=open_admin
MYSQL_PASSWORD=open_admin_password
MYSQL_ROOT_PASSWORD=root_password
JWT_SECRET_KEY=change-me-in-local-env
```

Update `.gitignore` so it contains:

```gitignore
.superpowers/
.env
*.local
node_modules/
dist/
coverage/
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
*.pyc
```

- [ ] **Step 2: Add Docker Compose for MySQL**

Create `docker-compose.yml`:

```yaml
services:
  mysql:
    image: mysql:8.4
    container_name: open-admin-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: open_admin
      MYSQL_USER: open_admin
      MYSQL_PASSWORD: open_admin_password
      TZ: Asia/Shanghai
    ports:
      - "3306:3306"
    command:
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1", "-uopen_admin", "-popen_admin_password"]
      interval: 10s
      timeout: 5s
      retries: 10

volumes:
  mysql_data:
```

- [ ] **Step 3: Add initial open-source docs**

Create `README.md`:

```markdown
# Open Admin

Open Admin is a Vue 3 + FastAPI admin framework with JWT authentication, RBAC, MySQL persistence, and a modern SaaS-style management UI.

## Tech Stack

- Frontend: Vue 3, Vite, TypeScript, Element Plus, Pinia, Vue Router
- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic
- Database: MySQL

## Quick Start

```bash
docker compose up -d mysql
```

Backend and frontend setup steps are added as the MVP implementation lands.

## Default Admin Account

- Username: `admin`
- Password: `Admin123!`
```

Create `LICENSE`:

```text
MIT License

Copyright (c) 2026 Open Admin contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Create `CONTRIBUTING.md`:

```markdown
# Contributing

Run frontend type checks and tests before opening a pull request.
Run backend linting and tests before opening a pull request.
Keep feature changes scoped and include tests for authentication, authorization, and system management behavior.
```

Create `CHANGELOG.md`:

```markdown
# Changelog

## 0.1.0

- Initial MVP development.
```

- [ ] **Step 4: Verify and commit**

Run:

```bash
docker compose config
git status --short
```

Expected: Docker Compose validates and git shows only the files in this task.

Commit:

```bash
git add .editorconfig .env.example .gitignore docker-compose.yml README.md LICENSE CONTRIBUTING.md CHANGELOG.md
git commit -m "chore: add repository baseline"
```

## Task 2: Backend Scaffold, Health Check, and Test Harness

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/.env.example`
- Create: `backend/app/main.py`
- Create: `backend/app/api/v1/router.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/responses.py`
- Create: `backend/tests/conftest.py`
- Create: `backend/tests/test_health.py`

- [ ] **Step 1: Write failing health test**

Create `backend/tests/test_health.py`:

```python
from fastapi.testclient import TestClient


def test_health_returns_standard_response(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["message"] == "ok"
    assert response.json()["data"] == {"status": "ok"}
    assert "request_id" in response.json()
```

Create `backend/tests/conftest.py`:

```python
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client
```

- [ ] **Step 2: Add backend packaging**

Create `backend/pyproject.toml`:

```toml
[project]
name = "open-admin-backend"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "alembic",
  "bcrypt",
  "fastapi",
  "pydantic-settings",
  "pyjwt",
  "pymysql",
  "python-multipart",
  "sqlalchemy",
  "uvicorn[standard]",
]

[project.optional-dependencies]
dev = [
  "httpx",
  "pytest",
  "pytest-cov",
  "ruff",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

Create `backend/.env.example`:

```env
APP_NAME=Open Admin API
API_PREFIX=/api/v1
DATABASE_URL=mysql+pymysql://open_admin:open_admin_password@127.0.0.1:3306/open_admin
JWT_SECRET_KEY=change-me-in-local-env
JWT_EXPIRE_MINUTES=120
```

- [ ] **Step 3: Run test to verify it fails**

Run:

```bash
cd backend
python -m pytest tests/test_health.py -v
```

Expected: FAIL because `app.main` or `/api/v1/health` does not exist.

- [ ] **Step 4: Implement app, config, and standard response**

Create `backend/app/core/config.py`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Open Admin API"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite+pysqlite:///:memory:"
    jwt_secret_key: str = "test-secret"
    jwt_expire_minutes: int = 120

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
```

Create `backend/app/core/responses.py`:

```python
from typing import Any
from uuid import uuid4


def success(data: Any = None, message: str = "ok", request_id: str | None = None) -> dict[str, Any]:
    return {
        "code": 0,
        "message": message,
        "data": data,
        "request_id": request_id or str(uuid4()),
    }
```

Create `backend/app/api/v1/router.py`:

```python
from fastapi import APIRouter

from app.core.responses import success

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return success({"status": "ok"})
```

Create `backend/app/main.py`:

```python
from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(api_v1_router, prefix=settings.api_prefix)
```

- [ ] **Step 5: Run test and commit**

Run:

```bash
cd backend
python -m pytest tests/test_health.py -v
python -m ruff check .
```

Expected: PASS.

Commit:

```bash
git add backend
git commit -m "feat: scaffold backend health api"
```

## Task 3: Backend Error Handling, Request IDs, and Database Session

**Files:**
- Create: `backend/app/core/errors.py`
- Create: `backend/app/core/database.py`
- Create: `backend/app/core/logging.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/test_errors.py`

- [ ] **Step 1: Write failing error contract test**

Create `backend/tests/test_errors.py`:

```python
from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.core.errors import AppError
from app.main import app


def test_app_error_uses_standard_response(client: TestClient) -> None:
    router = APIRouter()

    @router.get("/test-error")
    def raise_error() -> None:
        raise AppError(code=100403, message="无权限", status_code=403)

    app.include_router(router, prefix="/api/v1")

    response = client.get("/api/v1/test-error")

    assert response.status_code == 403
    assert response.json()["code"] == 100403
    assert response.json()["message"] == "无权限"
    assert response.json()["data"] is None
    assert "request_id" in response.json()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
cd backend
python -m pytest tests/test_errors.py -v
```

Expected: FAIL because `AppError` and handler do not exist.

- [ ] **Step 3: Implement errors and handlers**

Create `backend/app/core/errors.py`:

```python
from typing import Any


class AppError(Exception):
    def __init__(
        self,
        code: int,
        message: str,
        status_code: int = 400,
        details: Any = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
```

Create `backend/app/core/database.py`:

```python
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Create `backend/app/core/logging.py`:

```python
from uuid import uuid4

from fastapi import Request


def get_request_id(request: Request) -> str:
    header_value = request.headers.get("x-request-id")
    return header_value or str(uuid4())
```

Modify `backend/app/main.py`:

```python
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.errors import AppError
from app.core.logging import get_request_id

app = FastAPI(title=settings.app_name)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": None,
            "details": exc.details,
            "request_id": get_request_id(request),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "code": 100422,
            "message": "参数校验失败",
            "data": None,
            "details": exc.errors(),
            "request_id": get_request_id(request),
        },
    )


app.include_router(api_v1_router, prefix=settings.api_prefix)
```

- [ ] **Step 4: Run tests and commit**

Run:

```bash
cd backend
python -m pytest tests/test_health.py tests/test_errors.py -v
python -m ruff check .
```

Expected: PASS.

Commit:

```bash
git add backend
git commit -m "feat: add backend error contract"
```

## Task 4: Backend Models, Alembic, and Seed Data

**Files:**
- Create: `backend/app/models/base.py`
- Create: `backend/app/models/system.py`
- Create: `backend/app/core/security.py`
- Create: `backend/alembic.ini`
- Create: `backend/migrations/env.py`
- Create: `backend/migrations/versions/0001_initial_system_tables.py`
- Create: `backend/app/seed.py`
- Create: `backend/tests/test_models.py`

- [ ] **Step 1: Write failing model metadata test**

Create `backend/tests/test_models.py`:

```python
from app.models.base import Base
from app.models import system


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
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
cd backend
python -m pytest tests/test_models.py -v
```

Expected: FAIL because models do not exist.

- [ ] **Step 3: Implement base and system models**

Create `backend/app/models/base.py`:

```python
from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    created_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
```

Create `backend/app/models/system.py` with SQLAlchemy classes for `User`, `Role`, `Menu`, `Dept`, `Post`, `DictType`, `DictItem`, `Config`, `LoginLog`, `OperationLog`, and association tables `sys_user_role`, `sys_role_menu`, `sys_user_post`. Use integer primary keys, unique codes where relevant, `status` strings, sort integers, and nullable `deleted_at`.

Required field names:

```python
User.username
User.password_hash
User.nickname
User.email
User.mobile
User.dept_id
User.status
Role.code
Role.name
Role.data_scope
Menu.parent_id
Menu.type
Menu.title
Menu.path
Menu.component
Menu.permission
Menu.icon
Dept.parent_id
Dept.ancestors
Dept.name
Post.code
Post.name
DictType.code
DictItem.value
Config.key
LoginLog.username
OperationLog.permission
```

Create `backend/app/models/__init__.py`:

```python
from app.models.base import Base
from app.models.system import (
    Config,
    Dept,
    DictItem,
    DictType,
    LoginLog,
    Menu,
    OperationLog,
    Post,
    Role,
    User,
)

__all__ = [
    "Base",
    "Config",
    "Dept",
    "DictItem",
    "DictType",
    "LoginLog",
    "Menu",
    "OperationLog",
    "Post",
    "Role",
    "User",
]
```

- [ ] **Step 4: Add Alembic migration**

Create `backend/alembic.ini`:

```ini
[alembic]
script_location = migrations
prepend_sys_path = .
sqlalchemy.url = mysql+pymysql://open_admin:open_admin_password@127.0.0.1:3306/open_admin

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
```

Create `backend/migrations/env.py`:

```python
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

Create `backend/migrations/versions/0001_initial_system_tables.py` using `op.create_table` for every core and relation table named in the spec. Match the model field names and create unique indexes for `sys_user.username`, `sys_role.code`, `sys_post.code`, `sys_dict_type.code`, and `sys_config.key`.

- [ ] **Step 5: Add password hashing and seed data**

Create `backend/app/core/security.py`:

```python
import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
```

Create `backend/app/seed.py`:

```python
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.system import Menu, Role, User


def seed(db: Session) -> None:
    admin = db.query(User).filter(User.username == "admin").first()
    if admin is None:
        admin = User(
            username="admin",
            password_hash=hash_password("Admin123!"),
            nickname="Administrator",
            status="enabled",
        )
        db.add(admin)

    role = db.query(Role).filter(Role.code == "admin").first()
    if role is None:
        role = Role(code="admin", name="超级管理员", status="enabled", sort=1, data_scope="all")
        db.add(role)
        admin.roles.append(role)

    if db.query(Menu).count() == 0:
        role.menus.extend(
            [
                Menu(title="Dashboard", path="/dashboard", component="dashboard/DashboardView", type="menu", permission="dashboard:view", sort=1, status="enabled"),
                Menu(title="用户管理", path="/system/users", component="system/UserView", type="menu", permission="system:user:list", sort=10, status="enabled"),
                Menu(title="角色管理", path="/system/roles", component="system/RoleView", type="menu", permission="system:role:list", sort=11, status="enabled"),
                Menu(title="菜单管理", path="/system/menus", component="system/MenuView", type="menu", permission="system:menu:list", sort=12, status="enabled"),
            ]
        )

    db.commit()


if __name__ == "__main__":
    with SessionLocal() as session:
        seed(session)
```

- [ ] **Step 6: Run tests and commit**

Run:

```bash
cd backend
python -m pytest tests/test_models.py -v
python -m ruff check .
```

Expected: PASS.

Commit:

```bash
git add backend
git commit -m "feat: add backend system models"
```

## Task 5: Backend Security, JWT Auth, and Current User API

**Files:**
- Modify: `backend/app/core/security.py`
- Create: `backend/app/schemas/auth.py`
- Create: `backend/app/services/auth_service.py`
- Create: `backend/app/api/v1/auth.py`
- Modify: `backend/app/api/v1/router.py`
- Modify: `backend/app/seed.py`
- Create: `backend/tests/test_auth.py`

- [ ] **Step 1: Write failing auth tests**

Create `backend/tests/test_auth.py`:

```python
from fastapi.testclient import TestClient


def test_login_returns_token(client: TestClient, seeded_db) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "Admin123!"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 0
    assert payload["data"]["access_token"]
    assert payload["data"]["token_type"] == "bearer"


def test_me_requires_token(client: TestClient) -> None:
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
    assert response.json()["code"] == 100401


def test_me_returns_permissions(client: TestClient, admin_token: str) -> None:
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {admin_token}"})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["user"]["username"] == "admin"
    assert "admin" in data["roles"]
    assert "system:user:list" in data["permissions"]
    assert any(menu["path"] == "/system/users" for menu in data["menus"])
```

Update `backend/tests/conftest.py` with fixtures `seeded_db` and `admin_token`. Use an in-memory SQLite engine for tests and call the same `seed` function after creating tables.

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
cd backend
python -m pytest tests/test_auth.py -v
```

Expected: FAIL because security, seed, and auth APIs are incomplete.

- [ ] **Step 3: Implement security helpers**

Replace `backend/app/core/security.py` with:

```python
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    expires_delta = timedelta(minutes=expires_minutes or settings.jwt_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
```

- [ ] **Step 4: Implement schemas, service, and auth router**

Create `backend/app/schemas/auth.py`:

```python
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

Create `backend/app/services/auth_service.py`:

```python
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import create_access_token, verify_password
from app.models.system import User


def authenticate(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username, User.deleted_at.is_(None)).first()
    if user is None or user.status != "enabled" or not verify_password(password, user.password_hash):
        raise AppError(code=100401, message="账号或密码错误", status_code=401)
    return user


def build_token(user: User) -> dict[str, str]:
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}


def build_current_user(user: User) -> dict:
    roles = [role.code for role in user.roles if role.status == "enabled"]
    permissions = sorted(
        {menu.permission for role in user.roles for menu in role.menus if menu.permission and menu.status == "enabled"}
    )
    menus = [
        {
            "id": menu.id,
            "parent_id": menu.parent_id,
            "title": menu.title,
            "path": menu.path,
            "component": menu.component,
            "permission": menu.permission,
            "icon": menu.icon,
            "sort": menu.sort,
        }
        for role in user.roles
        for menu in role.menus
        if menu.type == "menu" and menu.status == "enabled"
    ]
    return {
        "user": {"id": user.id, "username": user.username, "nickname": user.nickname},
        "roles": roles,
        "permissions": permissions,
        "menus": sorted(menus, key=lambda item: item["sort"]),
    }
```

Create `backend/app/api/v1/auth.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.responses import success
from app.models.system import User
from app.schemas.auth import LoginRequest
from app.services.auth_service import authenticate, build_current_user, build_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    user = authenticate(db, payload.username, payload.password)
    return success(build_token(user))


@router.get("/me")
def me(current_user: User = Depends(get_current_user)) -> dict:
    return success(build_current_user(current_user))
```

Create `backend/app/core/deps.py`:

```python
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.core.security import decode_access_token
from app.models.system import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise AppError(code=100401, message="未登录或登录已过期", status_code=401)
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, ValueError):
        raise AppError(code=100401, message="未登录或登录已过期", status_code=401)

    user = db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
    if user is None or user.status != "enabled":
        raise AppError(code=100401, message="未登录或登录已过期", status_code=401)
    return user
```

Modify `backend/app/api/v1/router.py`:

```python
from fastapi import APIRouter

from app.api.v1 import auth
from app.core.responses import success

router = APIRouter()
router.include_router(auth.router)


@router.get("/health")
def health() -> dict:
    return success({"status": "ok"})
```

- [ ] **Step 5: Run tests and commit**

Run:

```bash
cd backend
python -m pytest tests/test_auth.py tests/test_health.py -v
python -m ruff check .
```

Expected: PASS.

Commit:

```bash
git add backend
git commit -m "feat: add jwt authentication"
```

## Task 6: Backend RBAC and System APIs

**Files:**
- Modify: `backend/app/core/deps.py`
- Create: `backend/app/schemas/common.py`
- Create: `backend/app/schemas/system.py`
- Create: `backend/app/services/rbac_service.py`
- Create: `backend/app/services/system_service.py`
- Create: `backend/app/services/log_service.py`
- Create: `backend/app/api/v1/system.py`
- Modify: `backend/app/api/v1/router.py`
- Create: `backend/tests/test_rbac.py`
- Create: `backend/tests/test_system_api.py`

- [ ] **Step 1: Write failing RBAC tests**

Create `backend/tests/test_rbac.py`:

```python
from fastapi import Depends
from fastapi.testclient import TestClient

from app.core.deps import require_permission
from app.main import app


def test_require_permission_allows_admin(client: TestClient, admin_token: str) -> None:
    @app.get("/api/v1/test-rbac")
    def protected(_: None = Depends(require_permission("system:user:list"))) -> dict:
        return {"code": 0, "message": "ok", "data": True, "request_id": "test"}

    response = client.get("/api/v1/test-rbac", headers={"Authorization": f"Bearer {admin_token}"})

    assert response.status_code == 200
    assert response.json()["data"] is True
```

Create `backend/tests/test_system_api.py`:

```python
def test_users_list_returns_page(client, admin_token: str) -> None:
    response = client.get(
        "/api/v1/system/users?page=1&page_size=20",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] >= 1
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert any(item["username"] == "admin" for item in data["items"])


def test_roles_list_returns_admin_role(client, admin_token: str) -> None:
    response = client.get(
        "/api/v1/system/roles?page=1&page_size=20",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert any(item["code"] == "admin" for item in response.json()["data"]["items"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
cd backend
python -m pytest tests/test_rbac.py tests/test_system_api.py -v
```

Expected: FAIL because RBAC dependency and system API are not implemented.

- [ ] **Step 3: Implement RBAC dependency**

Create `backend/app/services/rbac_service.py`:

```python
from app.models.system import User


def user_permissions(user: User) -> set[str]:
    return {
        menu.permission
        for role in user.roles
        for menu in role.menus
        if role.status == "enabled" and menu.permission and menu.status == "enabled"
    }
```

Append to `backend/app/core/deps.py`:

```python
from collections.abc import Callable

from app.services.rbac_service import user_permissions


def require_permission(permission: str) -> Callable:
    def checker(current_user: User = Depends(get_current_user)) -> None:
        if any(role.code == "admin" for role in current_user.roles):
            return
        if permission not in user_permissions(current_user):
            raise AppError(code=100403, message="无权限", status_code=403)

    return checker
```

- [ ] **Step 4: Implement common and system schemas**

Create `backend/app/schemas/common.py`:

```python
from pydantic import BaseModel


class PageResponse(BaseModel):
    items: list[dict]
    total: int
    page: int
    page_size: int
```

Create `backend/app/schemas/system.py` with Pydantic models for user, role, menu, dept, post, dict, config, and log list items. Use `from_attributes = True` and expose only fields used by the frontend tables.

Required model names:

```python
UserListItem
UserCreate
UserUpdate
RoleListItem
RoleCreate
RoleUpdate
MenuListItem
DeptListItem
PostListItem
DictTypeListItem
DictItemListItem
ConfigListItem
LoginLogListItem
OperationLogListItem
```

- [ ] **Step 5: Implement system services and router**

Create `backend/app/services/system_service.py`:

```python
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session


def page_query(db: Session, model: type, page: int, page_size: int) -> dict[str, Any]:
    query = db.query(model).filter(model.deleted_at.is_(None))
    total = query.with_entities(func.count()).scalar() or 0
    items = query.order_by(model.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": [to_dict(item) for item in items], "total": total, "page": page, "page_size": page_size}


def to_dict(item: Any) -> dict[str, Any]:
    return {
        column.name: getattr(item, column.name)
        for column in item.__table__.columns
        if column.name not in {"password_hash", "deleted_at"}
    }
```

Create `backend/app/services/log_service.py`:

```python
from sqlalchemy.orm import Session

from app.models.system import LoginLog, OperationLog, User


def log_login(db: Session, username: str, success: bool, message: str) -> None:
    db.add(LoginLog(username=username, success=success, message=message))
    db.commit()


def log_operation(db: Session, user: User, permission: str, title: str) -> None:
    db.add(OperationLog(username=user.username, permission=permission, title=title))
    db.commit()
```

Create `backend/app/api/v1/system.py` exposing list endpoints for users, roles, menus, depts, posts, dict types, configs, login logs, and operation logs. Protect each endpoint with `require_permission("<permission>")` and return `success(page_query(...))`.

Required endpoints:

```text
GET /system/users
GET /system/roles
GET /system/menus
GET /system/depts
GET /system/posts
GET /system/dict-types
GET /system/configs
GET /system/login-logs
GET /system/operation-logs
```

Modify `backend/app/api/v1/router.py` to include `system.router`.

- [ ] **Step 6: Run tests and commit**

Run:

```bash
cd backend
python -m pytest tests/test_rbac.py tests/test_system_api.py -v
python -m ruff check .
```

Expected: PASS.

Commit:

```bash
git add backend
git commit -m "feat: add rbac system apis"
```

## Task 7: Frontend Scaffold, Routing, and Test Harness

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/index.html`
- Create: `frontend/vite.config.ts`
- Create: `frontend/tsconfig.json`
- Create: `frontend/src/main.ts`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/router/static-routes.ts`
- Create: `frontend/src/router/index.ts`
- Create: `frontend/src/views/login/LoginView.vue`
- Create: `frontend/src/views/dashboard/DashboardView.vue`
- Create: `frontend/src/views/errors/ForbiddenView.vue`
- Create: `frontend/src/views/errors/NotFoundView.vue`
- Create: `frontend/src/views/errors/ServerErrorView.vue`
- Create: `frontend/tests/permission.spec.ts`

- [ ] **Step 1: Create frontend package**

Create `frontend/package.json`:

```json
{
  "name": "open-admin-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite --host 0.0.0.0",
    "build": "vue-tsc --noEmit && vite build",
    "typecheck": "vue-tsc --noEmit",
    "test": "vitest run"
  },
  "dependencies": {
    "@element-plus/icons-vue": "^2.3.1",
    "axios": "^1.6.0",
    "element-plus": "^2.7.0",
    "pinia": "^2.1.0",
    "vue": "^3.4.0",
    "vue-router": "^4.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "typescript": "^5.4.0",
    "vite": "^5.2.0",
    "vitest": "^1.4.0",
    "vue-tsc": "^2.0.0"
  }
}
```

Create `frontend/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "jsx": "preserve",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "types": ["vitest/globals"],
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.vue", "tests/**/*.ts"]
}
```

Create `frontend/index.html`:

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Open Admin</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

Create `frontend/vite.config.ts`:

```ts
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  test: {
    environment: 'jsdom',
  },
})
```

- [ ] **Step 2: Write failing route test**

Create `frontend/tests/permission.spec.ts`:

```ts
import { describe, expect, it } from 'vitest'
import { staticRoutes } from '../src/router/static-routes'

describe('static routes', () => {
  it('contains login and dashboard routes', () => {
    expect(staticRoutes.some(route => route.path === '/login')).toBe(true)
    expect(staticRoutes.some(route => route.path === '/dashboard')).toBe(true)
  })
})
```

- [ ] **Step 3: Run test to verify it fails**

Run:

```bash
cd frontend
npm install
npm test -- tests/permission.spec.ts
```

Expected: FAIL because route files do not exist.

- [ ] **Step 4: Implement minimal frontend app and routes**

Create `frontend/src/router/static-routes.ts`:

```ts
import type { RouteRecordRaw } from 'vue-router'

export const staticRoutes: RouteRecordRaw[] = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: () => import('@/views/login/LoginView.vue') },
  { path: '/dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/DashboardView.vue') },
  { path: '/403', name: 'Forbidden', component: () => import('@/views/errors/ForbiddenView.vue') },
  { path: '/500', name: 'ServerError', component: () => import('@/views/errors/ServerErrorView.vue') },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/errors/NotFoundView.vue') },
]
```

Create `frontend/src/router/index.ts`:

```ts
import { createRouter, createWebHistory } from 'vue-router'
import { staticRoutes } from './static-routes'

export const router = createRouter({
  history: createWebHistory(),
  routes: staticRoutes,
})
```

Create `frontend/src/main.ts`:

```ts
import ElementPlus from 'element-plus'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import 'element-plus/dist/index.css'

createApp(App).use(createPinia()).use(router).use(ElementPlus).mount('#app')
```

Create `frontend/src/App.vue`:

```vue
<template>
  <router-view />
</template>
```

Create minimal view files with a single root element and visible page title for Login, Dashboard, Forbidden, NotFound, and ServerError.

- [ ] **Step 5: Run tests and commit**

Run:

```bash
cd frontend
npm test -- tests/permission.spec.ts
npm run typecheck
```

Expected: PASS.

Commit:

```bash
git add frontend
git commit -m "feat: scaffold frontend app"
```

## Task 8: Frontend API Client, Auth Store, and Route Guard

**Files:**
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/api/auth.ts`
- Create: `frontend/src/stores/auth.ts`
- Modify: `frontend/src/router/index.ts`
- Create: `frontend/tests/auth-store.spec.ts`

- [ ] **Step 1: Write failing auth store tests**

Create `frontend/tests/auth-store.spec.ts`:

```ts
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'
import { useAuthStore } from '../src/stores/auth'

describe('auth store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('stores token', () => {
    const store = useAuthStore()

    store.setToken('abc')

    expect(store.token).toBe('abc')
    expect(localStorage.getItem('access_token')).toBe('abc')
  })

  it('detects permission codes', () => {
    const store = useAuthStore()
    store.permissions = ['system:user:list']

    expect(store.hasPermission('system:user:list')).toBe(true)
    expect(store.hasPermission('system:user:delete')).toBe(false)
  })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
cd frontend
npm test -- tests/auth-store.spec.ts
```

Expected: FAIL because auth store does not exist.

- [ ] **Step 3: Implement API client and auth API**

Create `frontend/src/api/client.ts`:

```ts
import axios from 'axios'

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? '/api/v1',
  timeout: 15000,
})

http.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

Create `frontend/src/api/auth.ts`:

```ts
import { http } from './client'

export interface LoginPayload {
  username: string
  password: string
}

export interface LoginResult {
  access_token: string
  token_type: string
}

export async function loginApi(payload: LoginPayload): Promise<LoginResult> {
  const response = await http.post('/auth/login', payload)
  return response.data.data
}

export async function meApi() {
  const response = await http.get('/auth/me')
  return response.data.data
}
```

- [ ] **Step 4: Implement auth store and route guard**

Create `frontend/src/stores/auth.ts`:

```ts
import { defineStore } from 'pinia'
import { loginApi, meApi, type LoginPayload } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') ?? '',
    user: null as null | { id: number; username: string; nickname: string },
    roles: [] as string[],
    permissions: [] as string[],
    menus: [] as any[],
  }),
  actions: {
    setToken(token: string) {
      this.token = token
      localStorage.setItem('access_token', token)
    },
    async login(payload: LoginPayload) {
      const result = await loginApi(payload)
      this.setToken(result.access_token)
    },
    async fetchMe() {
      const data = await meApi()
      this.user = data.user
      this.roles = data.roles
      this.permissions = data.permissions
      this.menus = data.menus
    },
    logout() {
      this.token = ''
      this.user = null
      this.roles = []
      this.permissions = []
      this.menus = []
      localStorage.removeItem('access_token')
    },
    hasPermission(permission: string) {
      return this.roles.includes('admin') || this.permissions.includes(permission)
    },
  },
})
```

Modify `frontend/src/router/index.ts` to redirect unauthenticated users to `/login` and fetch current user before entering protected pages.

- [ ] **Step 5: Run tests and commit**

Run:

```bash
cd frontend
npm test -- tests/auth-store.spec.ts tests/permission.spec.ts
npm run typecheck
```

Expected: PASS.

Commit:

```bash
git add frontend
git commit -m "feat: add frontend auth flow"
```

## Task 9: Frontend Admin Layout and Permission Components

**Files:**
- Create: `frontend/src/styles/element.scss`
- Create: `frontend/src/styles/layout.scss`
- Create: `frontend/src/layouts/AdminLayout.vue`
- Create: `frontend/src/layouts/components/SidebarMenu.vue`
- Create: `frontend/src/layouts/components/TopBar.vue`
- Create: `frontend/src/layouts/components/TagsView.vue`
- Create: `frontend/src/stores/tabs.ts`
- Create: `frontend/src/stores/app.ts`
- Create: `frontend/src/components/PermissionButton.vue`
- Modify: `frontend/src/router/static-routes.ts`
- Modify: `frontend/src/main.ts`

- [ ] **Step 1: Write failing permission component test**

Extend `frontend/tests/permission.spec.ts`:

```ts
import { useAuthStore } from '../src/stores/auth'

it('admin role grants every permission', () => {
  const store = useAuthStore()
  store.roles = ['admin']

  expect(store.hasPermission('system:anything')).toBe(true)
})
```

Run:

```bash
cd frontend
npm test -- tests/permission.spec.ts
```

Expected: PASS. Keep this as a regression test for layout permission rendering.

- [ ] **Step 2: Implement layout styles**

Create `frontend/src/styles/layout.scss`:

```scss
:root {
  --oa-bg: #f6f8fb;
  --oa-panel: #ffffff;
  --oa-border: #dfe5ee;
  --oa-primary: #0f766e;
  --oa-text: #111827;
}

body {
  margin: 0;
  background: var(--oa-bg);
  color: var(--oa-text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.oa-shell {
  display: grid;
  grid-template-columns: 232px 1fr;
  min-height: 100vh;
}

.oa-main {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.oa-content {
  padding: 16px;
}
```

Create `frontend/src/styles/element.scss`:

```scss
@forward "element-plus/theme-chalk/src/common/var.scss" with (
  $colors: (
    "primary": (
      "base": #0f766e,
    ),
  )
);
```

- [ ] **Step 3: Implement layout components**

Create `AdminLayout.vue`, `SidebarMenu.vue`, `TopBar.vue`, and `TagsView.vue` so the screen uses classic sidebar + topbar + tags + content area. `SidebarMenu` renders `authStore.menus`. `TopBar` renders user nickname and logout. `TagsView` stores visited route tabs using `tabs.ts`.

Create `PermissionButton.vue`:

```vue
<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps<{
  permission: string
}>()

const auth = useAuthStore()
const visible = computed(() => auth.hasPermission(props.permission))
</script>

<template>
  <el-button v-if="visible">
    <slot />
  </el-button>
</template>
```

Modify `frontend/src/main.ts` to import `layout.scss` and `element.scss`.

- [ ] **Step 4: Wire protected routes under layout**

Modify `frontend/src/router/static-routes.ts` so `/dashboard`, `/system/*`, and `/examples/*` are children of `AdminLayout`. Keep `/login`, `/403`, `/500`, and `/:pathMatch(.*)*` outside the layout.

- [ ] **Step 5: Run checks and commit**

Run:

```bash
cd frontend
npm test
npm run typecheck
npm run build
```

Expected: PASS.

Commit:

```bash
git add frontend
git commit -m "feat: add admin layout shell"
```

## Task 10: Frontend Pages for System Management and Examples

**Files:**
- Create: `frontend/src/api/system.ts`
- Create: `frontend/src/components/PageTable.vue`
- Create: `frontend/src/views/system/UserView.vue`
- Create: `frontend/src/views/system/RoleView.vue`
- Create: `frontend/src/views/system/MenuView.vue`
- Create: `frontend/src/views/system/DeptView.vue`
- Create: `frontend/src/views/system/PostView.vue`
- Create: `frontend/src/views/system/DictView.vue`
- Create: `frontend/src/views/system/ConfigView.vue`
- Create: `frontend/src/views/system/LoginLogView.vue`
- Create: `frontend/src/views/system/OperationLogView.vue`
- Create: `frontend/src/views/examples/ListView.vue`
- Create: `frontend/src/views/examples/FormView.vue`
- Create: `frontend/src/views/examples/DetailView.vue`

- [ ] **Step 1: Implement system API wrappers**

Create `frontend/src/api/system.ts`:

```ts
import { http } from './client'

export interface PageParams {
  page: number
  page_size: number
  keyword?: string
}

export async function listUsers(params: PageParams) {
  const response = await http.get('/system/users', { params })
  return response.data.data
}

export async function listRoles(params: PageParams) {
  const response = await http.get('/system/roles', { params })
  return response.data.data
}

export async function listMenus(params: PageParams) {
  const response = await http.get('/system/menus', { params })
  return response.data.data
}

export async function listDepts(params: PageParams) {
  const response = await http.get('/system/depts', { params })
  return response.data.data
}

export async function listPosts(params: PageParams) {
  const response = await http.get('/system/posts', { params })
  return response.data.data
}

export async function listDictTypes(params: PageParams) {
  const response = await http.get('/system/dict-types', { params })
  return response.data.data
}

export async function listConfigs(params: PageParams) {
  const response = await http.get('/system/configs', { params })
  return response.data.data
}

export async function listLoginLogs(params: PageParams) {
  const response = await http.get('/system/login-logs', { params })
  return response.data.data
}

export async function listOperationLogs(params: PageParams) {
  const response = await http.get('/system/operation-logs', { params })
  return response.data.data
}
```

- [ ] **Step 2: Implement reusable page table**

Create `frontend/src/components/PageTable.vue` with props `columns`, `loader`, and `rowKey`. It should render an Element Plus table, keyword input, refresh button, and pagination. It must call `loader({ page, page_size, keyword })` and render `items` and `total`.

- [ ] **Step 3: Implement system views**

For each system view, import `PageTable` and the matching API wrapper. Define explicit columns matching backend fields. Add visible title and permission-coded action buttons:

```vue
<template>
  <section class="oa-page">
    <div class="oa-page__header">
      <h1>用户管理</h1>
      <PermissionButton permission="system:user:create">新增用户</PermissionButton>
    </div>
    <PageTable row-key="id" :columns="columns" :loader="listUsers" />
  </section>
</template>
```

Each view must use its own title and permission code:

```text
system:user:create
system:role:create
system:menu:create
system:dept:create
system:post:create
system:dict:create
system:config:create
system:login-log:list
system:operation-log:list
```

- [ ] **Step 4: Implement example views**

Create List, Form, and Detail example pages using Element Plus controls. They do not need backend writes. They demonstrate table filtering, form validation, and read-only detail sections.

- [ ] **Step 5: Run checks and commit**

Run:

```bash
cd frontend
npm run typecheck
npm run build
```

Expected: PASS.

Commit:

```bash
git add frontend
git commit -m "feat: add system management pages"
```

## Task 11: Backend CRUD Depth for Core System Modules

**Files:**
- Modify: `backend/app/api/v1/system.py`
- Modify: `backend/app/services/system_service.py`
- Modify: `backend/app/schemas/system.py`
- Modify: `backend/tests/test_system_api.py`

- [ ] **Step 1: Write failing user CRUD tests**

Append to `backend/tests/test_system_api.py`:

```python
def test_create_update_delete_user(client, admin_token: str) -> None:
    headers = {"Authorization": f"Bearer {admin_token}"}

    created = client.post(
        "/api/v1/system/users",
        headers=headers,
        json={"username": "demo", "password": "Demo123!", "nickname": "Demo User", "status": "enabled"},
    )
    assert created.status_code == 200
    user_id = created.json()["data"]["id"]

    updated = client.put(
        f"/api/v1/system/users/{user_id}",
        headers=headers,
        json={"nickname": "Demo Updated", "status": "disabled"},
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["nickname"] == "Demo Updated"

    deleted = client.delete(f"/api/v1/system/users/{user_id}", headers=headers)
    assert deleted.status_code == 200
    assert deleted.json()["data"]["deleted"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
cd backend
python -m pytest tests/test_system_api.py::test_create_update_delete_user -v
```

Expected: FAIL because write endpoints do not exist.

- [ ] **Step 3: Implement CRUD helpers and endpoints**

In `backend/app/services/system_service.py`, add functions:

```python
def create_item(db: Session, model: type, values: dict[str, Any]) -> Any
def update_item(db: Session, model: type, item_id: int, values: dict[str, Any]) -> Any
def soft_delete_item(db: Session, model: type, item_id: int) -> dict[str, bool]
```

Each function must filter `deleted_at.is_(None)`, raise `AppError(code=100404, message="资源不存在", status_code=404)` when missing, and commit changes.

In `backend/app/api/v1/system.py`, add create/update/delete endpoints for users, roles, menus, depts, posts, dict types, dict items, and configs. Log each write with `log_operation`.

- [ ] **Step 4: Run tests and commit**

Run:

```bash
cd backend
python -m pytest tests/test_system_api.py -v
python -m ruff check .
```

Expected: PASS.

Commit:

```bash
git add backend
git commit -m "feat: add system module crud"
```

## Task 12: End-to-End Local Run Documentation and Verification

**Files:**
- Modify: `README.md`
- Create: `docs/guide/quick-start.md`
- Create: `docs/guide/architecture.md`
- Create: `docs/guide/permission-model.md`
- Create: `docs/guide/add-module.md`
- Create: `docs/guide/deployment.md`
- Modify: `backend/.env.example`
- Create: `frontend/.env.example`

- [ ] **Step 1: Add frontend environment example**

Create `frontend/.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Ensure `backend/.env.example` contains the MySQL URL from root `.env.example`.

- [ ] **Step 2: Write quick start docs**

Create `docs/guide/quick-start.md` with exact commands:

```markdown
# Quick Start

## 1. Start MySQL

```bash
docker compose up -d mysql
```

## 2. Start Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

Default account:

- Username: `admin`
- Password: `Admin123!`
```

Create `docs/guide/architecture.md`:

```markdown
# Architecture

Open Admin is a Monorepo with `frontend/`, `backend/`, `docs/`, and root infrastructure files.

The frontend is a Vue 3 application with Element Plus, Pinia, Vue Router, and Axios. It renders the admin shell, handles token storage, loads current-user permissions, and protects routes.

The backend is a FastAPI service with routers, services, SQLAlchemy models, Pydantic schemas, Alembic migrations, and Pytest tests. It owns authentication, RBAC, system management APIs, logs, and seed data.
```

Create `docs/guide/permission-model.md`:

```markdown
# Permission Model

The MVP uses JWT authentication and RBAC authorization.

Menus decide visible routes. Permission codes decide visible buttons and backend API access.

Examples:

- `system:user:list`
- `system:user:create`
- `system:role:list`
- `system:menu:list`

Frontend checks permissions for rendering. Backend checks permissions again through API dependencies.
```

Create `docs/guide/add-module.md`:

```markdown
# Add a Module

1. Add SQLAlchemy model fields in `backend/app/models/system.py` or a new model file.
2. Add Alembic migration under `backend/migrations/versions`.
3. Add Pydantic request and response schemas under `backend/app/schemas`.
4. Add service functions under `backend/app/services`.
5. Add API routes under `backend/app/api/v1`.
6. Add frontend API wrapper under `frontend/src/api`.
7. Add Vue page under `frontend/src/views`.
8. Add menu seed data with a stable permission code.
9. Add backend tests and frontend type checks.
```

Create `docs/guide/deployment.md`:

```markdown
# Deployment

Build the frontend with `npm run build` inside `frontend/`.

Run the backend with an ASGI server such as Uvicorn or Gunicorn with Uvicorn workers.

Use environment variables for database URL and JWT secret. Use a managed MySQL instance or a production MySQL container with persistent volumes and backups.

Run `alembic upgrade head` before starting a new backend release.
```

- [ ] **Step 3: Update README**

Update `README.md` to include:

```markdown
## Quick Start

See `docs/guide/quick-start.md`.

## Features

- Vue 3 + Element Plus admin shell
- FastAPI REST API
- JWT authentication
- RBAC menus and permission codes
- MySQL migrations and seed data
- User, role, menu, department, post, dictionary, config, and log modules
```

- [ ] **Step 4: Run final verification**

Run:

```bash
docker compose config
cd backend
python -m pytest -v
python -m ruff check .
cd ../frontend
npm test
npm run typecheck
npm run build
```

Expected: PASS.

Commit:

```bash
git add README.md docs backend/.env.example frontend/.env.example
git commit -m "docs: add quick start guides"
```

## Task 13: Final MVP Smoke Test

**Files:**
- No required file changes unless smoke testing exposes defects.

- [ ] **Step 1: Start database**

Run:

```bash
docker compose up -d mysql
docker compose ps
```

Expected: `open-admin-mysql` is running and healthy.

- [ ] **Step 2: Run backend migration and seed**

Run:

```bash
cd backend
alembic upgrade head
python -m app.seed
```

Expected: migration completes, seed command exits without duplicate key errors.

- [ ] **Step 3: Start backend**

Run:

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Expected: FastAPI listens on `http://localhost:8000`.

- [ ] **Step 4: Start frontend**

Run in another shell:

```bash
cd frontend
npm run dev
```

Expected: Vite serves `http://localhost:5173`.

- [ ] **Step 5: Manual browser check**

Open `http://localhost:5173` and verify:

```text
1. Login with admin / Admin123!
2. Dashboard appears after login.
3. Sidebar shows Dashboard, 用户管理, 角色管理, 菜单管理.
4. 用户管理 table loads admin user.
5. 角色管理 table loads admin role.
6. Logout returns to login page.
```

- [ ] **Step 6: Commit smoke fixes**

If smoke testing required fixes, run relevant tests and commit:

```bash
git add frontend backend docs README.md
git commit -m "fix: pass mvp smoke test"
```

If no fixes were needed, do not create an empty commit.

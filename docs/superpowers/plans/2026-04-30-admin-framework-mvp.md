# 后台管理框架 MVP 实施计划

> **给执行代理的要求：** 实施本计划时必须使用 `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans`。每个步骤使用复选框（`- [ ]`）跟踪执行状态。

**目标：** 构建一个可本地运行、适合开源的后台管理框架 MVP，包含 Vue 3 + Element Plus 前端、FastAPI 后端、MySQL 持久化、JWT 登录、RBAC 权限、核心系统管理模块、文档和快速启动流程。

**架构：** 仓库采用 Monorepo，根目录包含 `frontend/`、`backend/`、`docs/` 和基础设施文件。后端负责认证、权限、迁移、种子数据和 REST API；前端负责现代 SaaS 风格的后台壳、登录流程、路由守卫、权限渲染和系统管理页面。

**技术栈：** Vue 3、Vite、TypeScript、Element Plus、Pinia、Vue Router、Axios、Vitest、FastAPI、Pydantic、SQLAlchemy、Alembic、PyMySQL、Pytest、Ruff、MySQL、Docker Compose。

---

## 范围控制

本计划只交付第一版可运行闭环。复杂数据权限过滤、代码生成器、多租户、通知中心、在线设计器、完整 OAuth2/OIDC 接入不进入实现任务，只在文档和扩展点中保留。

## 目标目录结构

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
        errors/
        system/
        examples/
      tests/
        permission.spec.ts
        auth-store.spec.ts
  backend/
    pyproject.toml
    alembic.ini
    .env.example
    app/
      main.py
      api/v1/
      core/
      models/
      schemas/
      services/
      seed.py
    migrations/
      env.py
      versions/
    tests/
  docs/
    guide/
```

## 任务 1：仓库基础与本地基础设施

**文件：**

- 创建：`.editorconfig`
- 修改：`.gitignore`
- 创建：`.env.example`
- 创建：`docker-compose.yml`
- 创建：`README.md`
- 创建：`LICENSE`
- 创建：`CONTRIBUTING.md`
- 创建：`CHANGELOG.md`

- [ ] **步骤 1：写入仓库基础配置**

`.editorconfig`：

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

`.env.example`：

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

`.gitignore` 至少包含：

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

- [ ] **步骤 2：添加 MySQL Docker Compose**

`docker-compose.yml`：

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

- [ ] **步骤 3：添加开源基础文档**

`README.md` 写明项目介绍、技术栈、默认账号和快速启动入口。

`LICENSE` 使用 MIT License。

`CONTRIBUTING.md` 写明提交前需要运行前端类型检查、前端测试、后端 lint 和后端测试。

`CHANGELOG.md` 初始化 `0.1.0` 版本记录。

- [ ] **步骤 4：验证并提交**

运行：

```bash
docker compose config
git status --short
```

预期：Docker Compose 配置有效，git 只显示本任务新增或修改的文件。

提交：

```bash
git add .editorconfig .env.example .gitignore docker-compose.yml README.md LICENSE CONTRIBUTING.md CHANGELOG.md
git commit -m "chore: add repository baseline"
```

## 任务 2：后端脚手架、健康检查和测试框架

**文件：**

- 创建：`backend/pyproject.toml`
- 创建：`backend/.env.example`
- 创建：`backend/app/main.py`
- 创建：`backend/app/api/v1/router.py`
- 创建：`backend/app/core/config.py`
- 创建：`backend/app/core/responses.py`
- 创建：`backend/tests/conftest.py`
- 创建：`backend/tests/test_health.py`

- [ ] **步骤 1：先写失败测试**

`backend/tests/test_health.py`：

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

`backend/tests/conftest.py`：

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

- [ ] **步骤 2：添加后端依赖配置**

`backend/pyproject.toml`：

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

`backend/.env.example`：

```env
APP_NAME=Open Admin API
API_PREFIX=/api/v1
DATABASE_URL=mysql+pymysql://open_admin:open_admin_password@127.0.0.1:3306/open_admin
JWT_SECRET_KEY=change-me-in-local-env
JWT_EXPIRE_MINUTES=120
```

- [ ] **步骤 3：运行失败测试**

```bash
cd backend
python -m pytest tests/test_health.py -v
```

预期：失败，原因是 `app.main` 或 `/api/v1/health` 尚未实现。

- [ ] **步骤 4：实现最小可用 FastAPI 应用**

`backend/app/core/config.py`：

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

`backend/app/core/responses.py`：

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

`backend/app/api/v1/router.py`：

```python
from fastapi import APIRouter

from app.core.responses import success

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return success({"status": "ok"})
```

`backend/app/main.py`：

```python
from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(api_v1_router, prefix=settings.api_prefix)
```

- [ ] **步骤 5：验证并提交**

```bash
cd backend
python -m pytest tests/test_health.py -v
python -m ruff check .
```

预期：通过。

提交：

```bash
git add backend
git commit -m "feat: scaffold backend health api"
```

## 任务 3：后端错误处理、请求 ID 和数据库会话

**文件：**

- 创建：`backend/app/core/errors.py`
- 创建：`backend/app/core/database.py`
- 创建：`backend/app/core/logging.py`
- 修改：`backend/app/main.py`
- 创建：`backend/tests/test_errors.py`

- [ ] **步骤 1：写错误响应契约测试**

`backend/tests/test_errors.py`：

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

- [ ] **步骤 2：运行失败测试**

```bash
cd backend
python -m pytest tests/test_errors.py -v
```

预期：失败，原因是 `AppError` 和异常处理器尚未实现。

- [ ] **步骤 3：实现异常、数据库会话和 request_id**

`backend/app/core/errors.py`：

```python
from typing import Any


class AppError(Exception):
    def __init__(self, code: int, message: str, status_code: int = 400, details: Any = None) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
```

`backend/app/core/database.py`：

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

`backend/app/core/logging.py`：

```python
from uuid import uuid4

from fastapi import Request


def get_request_id(request: Request) -> str:
    return request.headers.get("x-request-id") or str(uuid4())
```

修改 `backend/app/main.py`，加入 `AppError` 和 `RequestValidationError` 的统一响应处理。

- [ ] **步骤 4：验证并提交**

```bash
cd backend
python -m pytest tests/test_health.py tests/test_errors.py -v
python -m ruff check .
```

预期：通过。

提交：

```bash
git add backend
git commit -m "feat: add backend error contract"
```

## 任务 4：后端数据模型、Alembic 和种子数据

**文件：**

- 创建：`backend/app/models/base.py`
- 创建：`backend/app/models/system.py`
- 创建：`backend/app/models/__init__.py`
- 创建：`backend/app/core/security.py`
- 创建：`backend/alembic.ini`
- 创建：`backend/migrations/env.py`
- 创建：`backend/migrations/versions/0001_initial_system_tables.py`
- 创建：`backend/app/seed.py`
- 创建：`backend/tests/test_models.py`

- [ ] **步骤 1：写模型注册测试**

`backend/tests/test_models.py`：

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

- [ ] **步骤 2：运行失败测试**

```bash
cd backend
python -m pytest tests/test_models.py -v
```

预期：失败，原因是模型不存在。

- [ ] **步骤 3：实现 Base、通用字段和系统模型**

`backend/app/models/base.py`：

```python
from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
```

`backend/app/models/system.py` 必须实现这些表：

```text
sys_user
sys_role
sys_menu
sys_dept
sys_post
sys_dict_type
sys_dict_item
sys_config
sys_login_log
sys_operation_log
sys_user_role
sys_role_menu
sys_user_post
```

关键字段必须包含：

```text
User.username, User.password_hash, User.nickname, User.email, User.mobile, User.dept_id, User.status
Role.code, Role.name, Role.data_scope, Role.status
Menu.parent_id, Menu.type, Menu.title, Menu.path, Menu.component, Menu.permission, Menu.icon, Menu.sort, Menu.status
Dept.parent_id, Dept.ancestors, Dept.name, Dept.status
Post.code, Post.name, Post.status
DictType.code, DictType.name, DictType.status
DictItem.value, DictItem.label, DictItem.status
Config.key, Config.value, Config.name
LoginLog.username, LoginLog.success, LoginLog.message
OperationLog.username, OperationLog.permission, OperationLog.title
```

- [ ] **步骤 4：实现迁移和种子数据**

`backend/migrations/versions/0001_initial_system_tables.py` 使用 `op.create_table` 创建所有核心表和关系表，并为 `sys_user.username`、`sys_role.code`、`sys_post.code`、`sys_dict_type.code`、`sys_config.key` 创建唯一索引。

`backend/app/core/security.py` 先提供密码哈希：

```python
import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
```

`backend/app/seed.py` 创建默认管理员、管理员角色和基础菜单：

```text
账号：admin
密码：Admin123!
角色：admin
菜单：Dashboard、用户管理、角色管理、菜单管理、部门管理、岗位管理、字典管理、参数配置、登录日志、操作日志
```

- [ ] **步骤 5：验证并提交**

```bash
cd backend
python -m pytest tests/test_models.py -v
python -m ruff check .
```

预期：通过。

提交：

```bash
git add backend
git commit -m "feat: add backend system models"
```

## 任务 5：后端安全、JWT 登录和当前用户接口

**文件：**

- 修改：`backend/app/core/security.py`
- 创建：`backend/app/core/deps.py`
- 创建：`backend/app/schemas/auth.py`
- 创建：`backend/app/services/auth_service.py`
- 创建：`backend/app/api/v1/auth.py`
- 修改：`backend/app/api/v1/router.py`
- 创建：`backend/tests/test_auth.py`

- [ ] **步骤 1：写认证测试**

测试必须覆盖：

```text
POST /api/v1/auth/login 正确账号密码返回 access_token
GET /api/v1/auth/me 未带 token 返回 401 和 code=100401
GET /api/v1/auth/me 带管理员 token 返回 user、roles、permissions、menus
```

- [ ] **步骤 2：运行失败测试**

```bash
cd backend
python -m pytest tests/test_auth.py -v
```

预期：失败，原因是登录、JWT、依赖和当前用户接口尚未实现。

- [ ] **步骤 3：补全安全工具**

`backend/app/core/security.py` 最终必须包含：

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
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.jwt_expire_minutes)
    return jwt.encode({"sub": subject, "exp": expire}, settings.jwt_secret_key, algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
```

- [ ] **步骤 4：实现登录、当前用户和依赖**

实现：

```text
LoginRequest(username, password)
TokenResponse(access_token, token_type)
authenticate(db, username, password)
build_token(user)
build_current_user(user)
get_current_user(credentials, db)
POST /api/v1/auth/login
GET /api/v1/auth/me
```

`build_current_user` 返回结构：

```json
{
  "user": {"id": 1, "username": "admin", "nickname": "Administrator"},
  "roles": ["admin"],
  "permissions": ["system:user:list"],
  "menus": []
}
```

- [ ] **步骤 5：验证并提交**

```bash
cd backend
python -m pytest tests/test_auth.py tests/test_health.py -v
python -m ruff check .
```

预期：通过。

提交：

```bash
git add backend
git commit -m "feat: add jwt authentication"
```

## 任务 6：后端 RBAC 和系统管理 API

**文件：**

- 修改：`backend/app/core/deps.py`
- 创建：`backend/app/schemas/common.py`
- 创建：`backend/app/schemas/system.py`
- 创建：`backend/app/services/rbac_service.py`
- 创建：`backend/app/services/system_service.py`
- 创建：`backend/app/services/log_service.py`
- 创建：`backend/app/api/v1/system.py`
- 修改：`backend/app/api/v1/router.py`
- 创建：`backend/tests/test_rbac.py`
- 创建：`backend/tests/test_system_api.py`

- [ ] **步骤 1：写 RBAC 和系统接口测试**

测试必须覆盖：

```text
管理员拥有 system:user:list 时可访问受保护接口
GET /api/v1/system/users 返回分页结构
GET /api/v1/system/roles 返回 admin 角色
```

- [ ] **步骤 2：运行失败测试**

```bash
cd backend
python -m pytest tests/test_rbac.py tests/test_system_api.py -v
```

预期：失败，原因是权限依赖和系统接口尚未实现。

- [ ] **步骤 3：实现权限服务和依赖**

实现：

```text
user_permissions(user) -> set[str]
require_permission(permission)
```

规则：

```text
角色 code 为 admin 时放行
否则必须拥有指定 permission
无权限返回 AppError(code=100403, message="无权限", status_code=403)
```

- [ ] **步骤 4：实现分页和列表接口**

实现 `PageResponse`、系统列表 Item schema、`page_query`、`to_dict`。

必须提供接口：

```text
GET /api/v1/system/users
GET /api/v1/system/roles
GET /api/v1/system/menus
GET /api/v1/system/depts
GET /api/v1/system/posts
GET /api/v1/system/dict-types
GET /api/v1/system/configs
GET /api/v1/system/login-logs
GET /api/v1/system/operation-logs
```

每个接口返回：

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 20
}
```

- [ ] **步骤 5：验证并提交**

```bash
cd backend
python -m pytest tests/test_rbac.py tests/test_system_api.py -v
python -m ruff check .
```

预期：通过。

提交：

```bash
git add backend
git commit -m "feat: add rbac system apis"
```

## 任务 7：前端脚手架、路由和测试框架

**文件：**

- 创建：`frontend/package.json`
- 创建：`frontend/index.html`
- 创建：`frontend/vite.config.ts`
- 创建：`frontend/tsconfig.json`
- 创建：`frontend/src/main.ts`
- 创建：`frontend/src/App.vue`
- 创建：`frontend/src/router/static-routes.ts`
- 创建：`frontend/src/router/index.ts`
- 创建：`frontend/src/views/login/LoginView.vue`
- 创建：`frontend/src/views/dashboard/DashboardView.vue`
- 创建：`frontend/src/views/errors/ForbiddenView.vue`
- 创建：`frontend/src/views/errors/NotFoundView.vue`
- 创建：`frontend/src/views/errors/ServerErrorView.vue`
- 创建：`frontend/tests/permission.spec.ts`

- [ ] **步骤 1：创建前端工程配置**

`frontend/package.json`：

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
    "vue-tsc": "^2.0.0",
    "jsdom": "^24.0.0"
  }
}
```

`vite.config.ts` 配置 Vue 插件、`@` 别名和 Vitest `jsdom` 环境。

- [ ] **步骤 2：写路由测试**

`frontend/tests/permission.spec.ts`：

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

- [ ] **步骤 3：运行失败测试**

```bash
cd frontend
npm install
npm test -- tests/permission.spec.ts
```

预期：失败，原因是路由文件尚未实现。

- [ ] **步骤 4：实现最小前端应用**

实现：

```text
main.ts
App.vue
router/static-routes.ts
router/index.ts
LoginView.vue
DashboardView.vue
ForbiddenView.vue
NotFoundView.vue
ServerErrorView.vue
```

静态路由必须包含：

```text
/
/login
/dashboard
/403
/500
/:pathMatch(.*)*
```

- [ ] **步骤 5：验证并提交**

```bash
cd frontend
npm test -- tests/permission.spec.ts
npm run typecheck
```

预期：通过。

提交：

```bash
git add frontend
git commit -m "feat: scaffold frontend app"
```

## 任务 8：前端 API 客户端、登录状态和路由守卫

**文件：**

- 创建：`frontend/src/api/client.ts`
- 创建：`frontend/src/api/auth.ts`
- 创建：`frontend/src/stores/auth.ts`
- 修改：`frontend/src/router/index.ts`
- 创建：`frontend/tests/auth-store.spec.ts`

- [ ] **步骤 1：写 auth store 测试**

`frontend/tests/auth-store.spec.ts`：

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

- [ ] **步骤 2：运行失败测试**

```bash
cd frontend
npm test -- tests/auth-store.spec.ts
```

预期：失败，原因是 store 尚未实现。

- [ ] **步骤 3：实现请求封装和认证 API**

`client.ts` 必须创建 Axios 实例：

```text
baseURL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1"
timeout = 15000
请求拦截器从 localStorage.access_token 注入 Authorization: Bearer <token>
```

`auth.ts` 必须实现：

```text
loginApi({ username, password })
meApi()
```

- [ ] **步骤 4：实现 auth store 和路由守卫**

`auth.ts` store 必须包含：

```text
token
user
roles
permissions
menus
setToken(token)
login(payload)
fetchMe()
logout()
hasPermission(permission)
```

路由守卫规则：

```text
访问 /login 不需要 token
访问其他页面没有 token 时跳转 /login
有 token 但没有 user 时先调用 fetchMe()
```

- [ ] **步骤 5：验证并提交**

```bash
cd frontend
npm test -- tests/auth-store.spec.ts tests/permission.spec.ts
npm run typecheck
```

预期：通过。

提交：

```bash
git add frontend
git commit -m "feat: add frontend auth flow"
```

## 任务 9：前端后台主布局和权限组件

**文件：**

- 创建：`frontend/src/styles/element.scss`
- 创建：`frontend/src/styles/layout.scss`
- 创建：`frontend/src/layouts/AdminLayout.vue`
- 创建：`frontend/src/layouts/components/SidebarMenu.vue`
- 创建：`frontend/src/layouts/components/TopBar.vue`
- 创建：`frontend/src/layouts/components/TagsView.vue`
- 创建：`frontend/src/stores/tabs.ts`
- 创建：`frontend/src/stores/app.ts`
- 创建：`frontend/src/components/PermissionButton.vue`
- 修改：`frontend/src/router/static-routes.ts`
- 修改：`frontend/src/main.ts`

- [ ] **步骤 1：补充权限回归测试**

在 `permission.spec.ts` 中增加：

```ts
it('admin role grants every permission', () => {
  const store = useAuthStore()
  store.roles = ['admin']
  expect(store.hasPermission('system:anything')).toBe(true)
})
```

运行：

```bash
cd frontend
npm test -- tests/permission.spec.ts
```

预期：通过。

- [ ] **步骤 2：实现布局样式**

`layout.scss` 定义：

```text
--oa-bg: #f6f8fb
--oa-panel: #ffffff
--oa-border: #dfe5ee
--oa-primary: #0f766e
--oa-text: #111827
.oa-shell 使用 232px 左侧栏 + 主内容区
.oa-main 使用 flex column
.oa-content padding: 16px
```

- [ ] **步骤 3：实现布局组件**

实现：

```text
AdminLayout.vue：整体壳
SidebarMenu.vue：根据 authStore.menus 渲染菜单
TopBar.vue：折叠菜单、全屏、主题入口、用户信息、退出
TagsView.vue：记录和关闭访问标签
PermissionButton.vue：根据 permission 控制按钮显示
```

- [ ] **步骤 4：把受保护页面挂到布局下**

`/dashboard`、`/system/*`、`/examples/*` 挂到 `AdminLayout` 下。`/login`、`/403`、`/500`、`404` 不进入后台布局。

- [ ] **步骤 5：验证并提交**

```bash
cd frontend
npm test
npm run typecheck
npm run build
```

预期：通过。

提交：

```bash
git add frontend
git commit -m "feat: add admin layout shell"
```

## 任务 10：前端系统管理页面和示例页面

**文件：**

- 创建：`frontend/src/api/system.ts`
- 创建：`frontend/src/components/PageTable.vue`
- 创建：`frontend/src/views/system/UserView.vue`
- 创建：`frontend/src/views/system/RoleView.vue`
- 创建：`frontend/src/views/system/MenuView.vue`
- 创建：`frontend/src/views/system/DeptView.vue`
- 创建：`frontend/src/views/system/PostView.vue`
- 创建：`frontend/src/views/system/DictView.vue`
- 创建：`frontend/src/views/system/ConfigView.vue`
- 创建：`frontend/src/views/system/LoginLogView.vue`
- 创建：`frontend/src/views/system/OperationLogView.vue`
- 创建：`frontend/src/views/examples/ListView.vue`
- 创建：`frontend/src/views/examples/FormView.vue`
- 创建：`frontend/src/views/examples/DetailView.vue`

- [ ] **步骤 1：实现系统 API 封装**

`system.ts` 必须实现：

```text
listUsers
listRoles
listMenus
listDepts
listPosts
listDictTypes
listConfigs
listLoginLogs
listOperationLogs
```

统一参数：

```ts
export interface PageParams {
  page: number
  page_size: number
  keyword?: string
}
```

- [ ] **步骤 2：实现通用表格页面组件**

`PageTable.vue` 必须包含：

```text
keyword 输入框
刷新按钮
Element Plus 表格
分页器
columns / loader / rowKey props
调用 loader({ page, page_size, keyword })
渲染 items 和 total
```

- [ ] **步骤 3：实现系统管理页面**

每个系统页面使用 `PageTable` 和对应 API。页面必须有明确标题和权限按钮：

```text
用户管理：system:user:create
角色管理：system:role:create
菜单管理：system:menu:create
部门管理：system:dept:create
岗位管理：system:post:create
字典管理：system:dict:create
参数配置：system:config:create
登录日志：system:login-log:list
操作日志：system:operation-log:list
```

- [ ] **步骤 4：实现示例页面**

示例页必须覆盖：

```text
列表页：筛选、表格、分页、批量操作视觉
表单页：Element Plus 表单校验
详情页：只读详情分组
```

- [ ] **步骤 5：验证并提交**

```bash
cd frontend
npm run typecheck
npm run build
```

预期：通过。

提交：

```bash
git add frontend
git commit -m "feat: add system management pages"
```

## 任务 11：后端核心系统模块 CRUD

**文件：**

- 修改：`backend/app/api/v1/system.py`
- 修改：`backend/app/services/system_service.py`
- 修改：`backend/app/schemas/system.py`
- 修改：`backend/tests/test_system_api.py`

- [ ] **步骤 1：写用户 CRUD 测试**

测试必须覆盖：

```text
POST /api/v1/system/users 创建 demo 用户
PUT /api/v1/system/users/{id} 修改 nickname 和 status
DELETE /api/v1/system/users/{id} 软删除用户
```

- [ ] **步骤 2：运行失败测试**

```bash
cd backend
python -m pytest tests/test_system_api.py::test_create_update_delete_user -v
```

预期：失败，原因是写接口尚未实现。

- [ ] **步骤 3：实现 CRUD 服务**

`system_service.py` 增加：

```text
create_item(db, model, values)
update_item(db, model, item_id, values)
soft_delete_item(db, model, item_id)
```

规则：

```text
只操作 deleted_at is null 的数据
资源不存在时返回 AppError(code=100404, message="资源不存在", status_code=404)
删除使用软删除
写操作后 commit
```

- [ ] **步骤 4：实现写接口和操作日志**

为这些模块提供创建、更新、删除接口：

```text
users
roles
menus
depts
posts
dict-types
dict-items
configs
```

每个写接口必须调用 `log_operation` 记录操作人、权限码和标题。

- [ ] **步骤 5：验证并提交**

```bash
cd backend
python -m pytest tests/test_system_api.py -v
python -m ruff check .
```

预期：通过。

提交：

```bash
git add backend
git commit -m "feat: add system module crud"
```

## 任务 12：本地运行文档和发布文档

**文件：**

- 修改：`README.md`
- 创建：`docs/guide/quick-start.md`
- 创建：`docs/guide/architecture.md`
- 创建：`docs/guide/permission-model.md`
- 创建：`docs/guide/add-module.md`
- 创建：`docs/guide/deployment.md`
- 修改：`backend/.env.example`
- 创建：`frontend/.env.example`

- [ ] **步骤 1：添加前端环境变量示例**

`frontend/.env.example`：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

- [ ] **步骤 2：写快速开始文档**

`docs/guide/quick-start.md` 必须包含 Windows PowerShell 可执行命令：

```bash
docker compose up -d mysql
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

前端命令：

```bash
cd frontend
npm install
npm run dev
```

默认账号：

```text
admin / Admin123!
```

- [ ] **步骤 3：写架构、权限、新增模块和部署文档**

`architecture.md` 说明 Monorepo、前后端职责和运行链路。

`permission-model.md` 说明 JWT、RBAC、菜单权限、按钮权限和后端强校验。

`add-module.md` 按 9 步说明新增模块：模型、迁移、schema、service、API、前端 API、页面、菜单种子、测试。

`deployment.md` 说明前端 build、后端 ASGI 运行、环境变量、MySQL、迁移和生产部署注意事项。

- [ ] **步骤 4：更新 README**

README 必须包含：

```text
项目介绍
技术栈
功能清单
快速开始链接
默认账号
开发命令
文档入口
```

- [ ] **步骤 5：最终验证并提交**

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

预期：通过。

提交：

```bash
git add README.md docs backend/.env.example frontend/.env.example
git commit -m "docs: add quick start guides"
```

## 任务 13：MVP 本地冒烟测试

**文件：**

- 不固定修改文件；如冒烟测试暴露问题，只修改相关前后端或文档文件。

- [ ] **步骤 1：启动数据库**

```bash
docker compose up -d mysql
docker compose ps
```

预期：`open-admin-mysql` 运行且健康。

- [ ] **步骤 2：执行迁移和种子数据**

```bash
cd backend
alembic upgrade head
python -m app.seed
```

预期：迁移成功，重复执行种子数据不会产生唯一键错误。

- [ ] **步骤 3：启动后端**

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

预期：FastAPI 监听 `http://localhost:8000`。

- [ ] **步骤 4：启动前端**

```bash
cd frontend
npm run dev
```

预期：Vite 监听 `http://localhost:5173`。

- [ ] **步骤 5：浏览器手工验收**

检查：

```text
1. 使用 admin / Admin123! 登录成功
2. 登录后进入 Dashboard
3. 左侧菜单显示 Dashboard、用户管理、角色管理、菜单管理
4. 用户管理表格能加载 admin 用户
5. 角色管理表格能加载 admin 角色
6. 退出登录后回到登录页
```

- [ ] **步骤 6：提交冒烟修复**

如果冒烟测试发现问题，修复后运行相关测试并提交：

```bash
git add frontend backend docs README.md
git commit -m "fix: pass mvp smoke test"
```

如果没有改动，不创建空提交。

## 执行方式

计划完成后有两种执行方式：

1. **子代理驱动（推荐）：** 每个任务交给新的执行代理完成，主线程负责审查和集成。适合这个前后端并行的大工程。
2. **当前会话内执行：** 在当前会话按任务顺序推进，分批检查。节奏更集中，但并行度低。

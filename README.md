# Open Admin

Open Admin 是一个面向开源的通用后台管理框架 MVP。项目采用前后端分离的 Monorepo 结构，提供可本地运行、易扩展的企业后台基础能力，包括登录认证、RBAC 权限、系统管理、审计日志和模块扩展约定。

## 技术栈

- 前端：Vue 3、Vite、TypeScript、Element Plus、Pinia、Vue Router、Axios、Vitest
- 后端：FastAPI、Pydantic、SQLAlchemy、Alembic、PyMySQL、Pytest、Ruff
- 数据库与基础设施：MySQL 8.4、Docker Compose
- 认证权限：JWT 登录、RBAC 权限模型

## 功能清单

- JWT 登录、当前用户信息和路由守卫
- RBAC 角色、菜单权限和按钮权限
- 用户、角色、菜单、部门、岗位、字典、参数配置等系统管理页面
- 登录日志和操作日志基础能力
- 后端统一响应、异常处理、分页查询和软删除基础服务
- 本地 MySQL、Alembic 迁移和 seed 初始化流程

## 默认账号

本地 seed 可以创建默认管理员账号：

```text
admin / Admin123!
```

该账号仅用于本地开发。为了安全，seed 只有在 `INITIAL_ADMIN_PASSWORD=Admin123!` 且 `ALLOW_DEFAULT_ADMIN_PASSWORD=1` 同时设置时才允许使用这个公开默认密码。共享环境或非本地部署必须改用强密码，并设置 `ALLOW_DEFAULT_ADMIN_PASSWORD=0`。

## 快速启动

完整步骤见 [Quick Start](docs/guide/quick-start.md)。

常用入口：

- 前端默认端口：`5173`
- 后端默认端口：`8000`
- API 前缀：`/api/v1`
- MySQL 默认端口：`3306`
- 本地 CORS Origins：`http://localhost:5173,http://127.0.0.1:5173`

## 开发命令

启动 MySQL：

```powershell
docker compose up -d mysql
```

后端安装、迁移、seed 和开发服务，从仓库根目录执行：

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

前端开发服务，在另一个 PowerShell 窗口从仓库根目录执行：

```powershell
cd frontend
npm install
npm run dev
```

验证命令，从仓库根目录执行：

```powershell
docker compose config
cd backend
python -m pytest -v
python -m ruff check .
cd ..\frontend
npm test
npm run typecheck
npm run build
```

## 本地基础设施

当前仓库基础设施包含：

- `.editorconfig`：统一编辑器格式
- `.env.example`：本地环境变量示例
- `docker-compose.yml`：本地 MySQL 开发环境
- `.gitignore`：忽略本地环境、依赖、构建产物和缓存

## 文档入口

- [Quick Start](docs/guide/quick-start.md)
- [Architecture](docs/guide/architecture.md)
- [Permission Model](docs/guide/permission-model.md)
- [Add a Module](docs/guide/add-module.md)
- [Deployment](docs/guide/deployment.md)

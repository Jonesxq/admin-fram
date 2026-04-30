# Open Admin

Open Admin 是一个面向开源的通用后台管理框架 MVP。项目采用前后端分离的 Monorepo 结构，目标是提供可本地运行、易扩展的企业后台基础能力。

## 技术栈

- 前端：Vue 3、Vite、TypeScript、Element Plus、Pinia、Vue Router、Axios、Vitest
- 后端：FastAPI、Pydantic、SQLAlchemy、Alembic、PyMySQL、Pytest、Ruff
- 数据库与基础设施：MySQL 8.4、Docker Compose
- 认证权限：JWT 登录、RBAC 权限模型

## 默认账号

后续种子数据会创建默认管理员账号：

```text
账号：admin
密码：Admin123!
角色：admin
```

## 快速启动

1. 复制环境变量示例：

   ```bash
   cp .env.example .env
   ```

2. 启动本地 MySQL：

   ```bash
   docker compose up -d mysql
   ```

3. 后续前后端脚手架完成后，分别进入 `backend/` 和 `frontend/` 启动服务。

常用入口：

- 前端默认端口：`5173`
- 后端默认端口：`8000`
- MySQL 默认端口：`3306`

## 本地基础设施

当前仓库基础设施包含：

- `.editorconfig`：统一编辑器格式
- `.env.example`：本地环境变量示例
- `docker-compose.yml`：本地 MySQL 开发环境
- `.gitignore`：忽略本地环境、依赖、构建产物和缓存

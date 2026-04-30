# 通用后台管理框架设计

日期：2026-04-30

## 目标

构建一个准备开源的通用后台管理框架。项目采用前后端分离的 Monorepo 结构，提供美观、现代、可运行的企业后台基础能力。第一版强调功能面完整，但控制每个模块深度，避免过早做成沉重平台。

核心技术栈：

- 前端：Vue 3、Vite、TypeScript、Element Plus、Pinia、Vue Router
- 后端：FastAPI、Pydantic、SQLAlchemy、Alembic
- 数据库：MySQL
- 认证权限：JWT 登录 + RBAC
- 工程组织：`frontend/`、`backend/`、`docs/`、`docker-compose.yml`

## 非目标

第一版不实现复杂数据权限规则引擎、代码生成器、多租户、通知中心、在线设计器、OAuth2/OIDC 完整接入。这些能力只保留扩展点或路线图说明。

## 仓库组织

项目采用 Monorepo：

```text
/
  frontend/              Vue 3 管理后台
  backend/               FastAPI 接口服务
  docs/                  开源文档和设计文档
  docker-compose.yml     本地 MySQL 开发环境
  README.md              快速开始和项目介绍
  LICENSE
  CONTRIBUTING.md
  CHANGELOG.md
```

前后端通过 REST API 通信。后端提供迁移脚本和种子数据，保证开源用户可以在本地重复初始化环境。

## 前端设计

前端采用现代 SaaS 风格，但保留后台系统的效率和稳定感。主布局为经典左侧菜单 + 顶部工具栏 + 标签页导航 + 内容区。

框架级能力：

- 登录页、主布局、异常页
- 动态菜单和动态路由
- 标签页导航，支持关闭、刷新和右键操作
- 面包屑、菜单折叠、全屏、主题切换、用户下拉
- Axios 请求封装、Token 注入、错误拦截
- 权限指令或组件，用权限码控制按钮显示
- 常用页面范式：查询表格页、弹窗表单、详情页、分栏树表页、仪表盘

视觉原则：

- 白底、细边框、低饱和主色，整体偏清爽和专业
- 页面密度服务于后台操作，不做营销式大面积装饰
- 卡片用于具体信息块，不把页面结构层层包成卡片
- 桌面端优先，移动端保证登录页和基础页面可用

## 后端设计

后端按清晰分层组织：

- `api/v1`：FastAPI 路由、依赖注入、请求校验
- `services`：业务规则、事务、权限检查
- `models`：SQLAlchemy ORM 模型
- `schemas`：Pydantic 请求和响应模型
- `core`：配置、安全、数据库连接、异常、日志
- `migrations`：Alembic 数据库迁移
- `tests`：Pytest 测试

认证流程：

1. 用户提交账号密码。
2. 后端校验密码哈希、用户状态和角色状态。
3. 后端签发 JWT access token。
4. 前端调用当前用户接口，获取用户信息、角色、菜单和权限码。
5. 前端根据菜单动态挂载路由。
6. 后端接口通过依赖继续强制校验权限码。

## 数据模型

第一版核心表：

- `sys_user`：用户账号、密码哈希、昵称、邮箱、手机号、部门、状态
- `sys_role`：角色编码、角色名称、排序、状态、数据范围预留字段
- `sys_menu`：父级、类型、标题、路由路径、组件路径、权限码、图标、排序、状态
- `sys_dept`：部门树，包含父级、祖级路径、名称、排序、负责人、状态
- `sys_post`：岗位编码、岗位名称、排序、状态
- `sys_dict_type`：字典类型
- `sys_dict_item`：字典项
- `sys_config`：系统参数键值
- `sys_login_log`：登录日志
- `sys_operation_log`：操作日志

关系表：

- `sys_user_role`
- `sys_role_menu`
- `sys_user_post`

通用字段：

- `id`
- `created_at`
- `updated_at`
- `created_by`
- `updated_by`
- `deleted_at` 或软删除标记，具体实现时按 SQLAlchemy 约定统一

## 权限模型

第一版实现 JWT + RBAC。

菜单权限决定前端可见路由。按钮权限使用 `permission code`，例如 `system:user:create`、`system:user:update`。后端接口不能只依赖前端隐藏按钮，必须在依赖层校验当前用户是否拥有对应权限码。

超级管理员可以绕过普通权限校验，但仍记录关键操作日志。

数据权限只保留角色字段和服务层扩展点。第一版不实现按部门、本人、自定义范围过滤业务数据。

## 第一版功能范围

必须可用：

- 登录、退出、获取当前用户
- 用户管理
- 角色管理
- 菜单管理
- 部门管理
- 岗位管理
- 字典管理
- 参数配置
- 操作日志
- 登录日志
- 仪表盘
- 列表页、表单页、详情页示例
- 403、404、500 异常页

预留扩展：

- 数据权限字段和服务层扩展点
- 接口审计日志扩展点
- OAuth2/OIDC 接入点
- 代码生成器目录或文档位置
- 多租户字段预留说明

## API 约定

API 前缀为 `/api/v1`。

资源接口采用一致风格：

```text
POST   /api/v1/auth/login
GET    /api/v1/auth/me
GET    /api/v1/system/users
POST   /api/v1/system/users
PUT    /api/v1/system/users/{id}
DELETE /api/v1/system/users/{id}
```

成功响应：

```json
{
  "code": 0,
  "message": "ok",
  "data": {},
  "request_id": "..."
}
```

错误响应：

```json
{
  "code": 100401,
  "message": "未登录或登录已过期",
  "details": null,
  "request_id": "..."
}
```

列表响应的 `data` 使用：

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 20
}
```

错误处理规则：

- 401：未登录或 token 过期
- 403：无权限
- 422：参数校验错误，映射为统一响应
- 500：服务端错误，响应中包含 `request_id`，后端日志记录堆栈

## 测试策略

前端：

- `vue-tsc` 类型检查
- ESLint 和格式化检查
- Vitest 覆盖工具函数、状态管理、权限判断

后端：

- Ruff 格式和静态检查
- Pytest 覆盖认证、RBAC、系统管理核心接口
- Alembic 迁移 smoke test

验收：

- 本地可启动 MySQL、后端、前端
- 管理员可登录并看到权限菜单
- 用户、角色、菜单的核心 CRUD 可用
- 修改角色权限后，前端菜单和按钮权限能体现变化
- 日志、字典、参数接口可用
- 种子数据可重复初始化

## 开源交付标准

第一版需要包含：

- `README.md`：项目介绍、截图、快速开始、默认账号、常见问题
- `.env.example`：前后端环境变量示例
- `docker-compose.yml`：MySQL 开发环境
- `LICENSE`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `docs/guide`：目录结构、权限模型、新增模块指南、部署说明

推荐快速开始流程：

```text
git clone <repo>
copy .env.example files
docker compose up -d mysql
run backend migrations and seed data
start backend dev server
start frontend dev server
```

发布前质量门禁：

- 前端 lint、typecheck、test 通过
- 后端 ruff、pytest 通过
- 数据库迁移能从空库执行成功
- README 中的快速开始步骤经过人工验证

## 设计取舍

选择 Element Plus 是为了降低第一版成本并获得稳定的表格、表单、弹窗、日期等后台常用组件。界面通过主题、布局、间距、页面范式和少量封装组件做出现代 SaaS 风，而不是从零实现 UI 组件库。

选择 FastAPI 是因为它类型友好、接口开发效率高，适合前后端分离和开源学习。后端分层保持清晰，但不引入过重的领域架构。

选择 MySQL 是为了贴近国内后台系统常见部署习惯。后续如果需要 PostgreSQL，可以通过 SQLAlchemy 和 Alembic 的抽象降低迁移成本，但第一版不承诺多数据库适配。

第一版强调功能完整，但每个模块只做到可用、清晰、可扩展。复杂平台能力进入路线图，不进入第一版核心实现。

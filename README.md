# Open Admin

**Open Admin** 是一个面向开源的通用后台管理框架，采用前后端分离的 Monorepo 架构。项目提供可本地运行、易于扩展的企业级后台基础能力，涵盖登录认证、RBAC 权限管理、系统管理、审计日志和模块扩展约定，适合用作各类管理系统的开发起点。

---

## 目录

- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [功能特性](#功能特性)
- [数据库设计](#数据库设计)
- [权限模型](#权限模型)
- [API 接口](#api-接口)
- [前端页面](#前端页面)
- [快速启动](#快速启动)
- [环境变量配置](#环境变量配置)
- [开发命令](#开发命令)
- [新增业务模块指南](#新增业务模块指南)
- [生产部署](#生产部署)
- [常见问题](#常见问题)
- [参与贡献](#参与贡献)
- [开源协议](#开源协议)

---

## 技术栈

### 前端

| 技术 | 版本 | 说明 |
|---|---|---|
| Vue 3 | ^3.4.0 | 核心框架，Composition API |
| Vite | ^6.4.2 | 构建工具与开发服务器 |
| TypeScript | ^5.4.0 | 类型安全 |
| Element Plus | ^2.7.0 | UI 组件库 |
| Pinia | ^2.1.0 | 状态管理 |
| Vue Router | ^4.3.0 | 客户端路由 |
| Axios | ^1.6.0 | HTTP 请求 |
| Sass | ^1.99.0 | CSS 预处理器 |
| Vitest | ^3.2.4 | 单元测试 |
| Vue TSC | ^2.0.0 | TypeScript 类型检查 |

### 后端

| 技术 | 说明 |
|---|---|
| FastAPI | Web 框架，自动生成 OpenAPI 文档 |
| Pydantic | 数据校验与序列化 |
| SQLAlchemy | ORM 数据库工具 |
| Alembic | 数据库迁移管理 |
| PyMySQL | MySQL 数据库驱动 |
| bcrypt | 密码哈希 |
| PyJWT | JWT 令牌签发与验证 |
| Uvicorn | ASGI 服务器 |
| Pytest | 单元测试 |
| Ruff | 代码格式化与静态检查 |

### 基础设施

| 技术 | 说明 |
|---|---|
| MySQL 8.4 | 关系型数据库 |
| Docker Compose | 本地开发环境编排 |
| MIT License | 开源协议 |

---

## 项目结构

```
open-admin/
├── .editorconfig                  # 编辑器统一配置
├── .env.example                   # 根目录环境变量示例
├── .gitignore                     # Git 忽略规则
├── docker-compose.yml             # Docker 编排（MySQL）
├── README.md                      # 项目说明文档
├── LICENSE                        # MIT 开源协议
├── CONTRIBUTING.md                # 贡献指南
├── CHANGELOG.md                   # 版本变更记录
│
├── backend/                       # 后端服务
│   ├── pyproject.toml             # Python 项目配置与依赖
│   ├── alembic.ini                # Alembic 迁移配置
│   ├── .env.example               # 后端环境变量示例
│   ├── app/
│   │   ├── main.py                # FastAPI 应用入口（CORS、异常处理、中间件）
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── router.py      # 路由注册入口
│   │   │       ├── auth.py        # 认证接口（登录、当前用户）
│   │   │       └── system.py      # 系统管理接口（用户、角色、菜单等）
│   │   ├── core/
│   │   │   ├── config.py          # 配置管理（Pydantic Settings）
│   │   │   ├── database.py        # SQLAlchemy 会话工厂
│   │   │   ├── deps.py            # 依赖注入（认证、权限校验）
│   │   │   ├── errors.py          # 自定义异常类
│   │   │   ├── logging.py         # 请求 ID 生成
│   │   │   ├── responses.py       # 统一响应封装
│   │   │   └── security.py        # 密码哈希、JWT 签发与验证
│   │   ├── models/
│   │   │   ├── base.py            # ORM 基类与通用字段Mixin
│   │   │   └── system.py          # 系统管理数据模型（10 张表 + 3 张关联表）
│   │   ├── schemas/
│   │   │   ├── auth.py            # 认证相关请求/响应模型
│   │   │   ├── common.py          # 分页响应模型
│   │   │   └── system.py          # 系统管理请求/响应模型
│   │   ├── services/
│   │   │   ├── auth_service.py    # 认证业务逻辑
│   │   │   ├── rbac_service.py    # RBAC 权限服务
│   │   │   ├── system_service.py  # 通用 CRUD 服务
│   │   │   └── log_service.py     # 审计日志服务
│   │   └── seed.py                # 种子数据初始化
│   ├── migrations/
│   │   ├── env.py                 # Alembic 迁移环境
│   │   └── versions/
│   │       └── 0001_initial_system_tables.py
│   └── tests/                     # 后端单元测试
│       ├── conftest.py
│       ├── test_auth.py           # 认证接口测试
│       ├── test_config.py         # 配置测试
│       ├── test_errors.py         # 错误处理测试
│       ├── test_health.py         # 健康检查测试
│       ├── test_models.py         # 数据模型测试
│       ├── test_rbac.py           # RBAC 权限测试
│       └── test_system_api.py     # 系统管理接口测试
│
├── frontend/                      # 前端应用
│   ├── package.json               # Node.js 项目配置与依赖
│   ├── index.html                 # HTML 入口
│   ├── vite.config.ts             # Vite 构建配置
│   ├── tsconfig.json              # TypeScript 配置
│   ├── .env.example               # 前端环境变量示例
│   └── src/
│       ├── main.ts                # 应用入口
│       ├── App.vue                # 根组件
│       ├── api/
│       │   ├── client.ts          # Axios 实例（Token 注入、超时配置）
│       │   ├── auth.ts            # 认证 API（登录、获取用户信息）
│       │   └── system.ts          # 系统管理 API（全部 CRUD 封装）
│       ├── components/
│       │   ├── PageTable.vue      # 通用分页表格组件
│       │   ├── PermissionButton.vue  # 权限按钮组件
│       │   ├── StatusTag.vue      # 状态标签组件
│       │   └── SystemCrudPage.vue # 系统 CRUD 页面组件（表格+弹窗表单）
│       ├── layouts/
│       │   ├── AdminLayout.vue    # 后台主布局（侧边栏+顶栏+标签页+内容区）
│       │   └── components/
│       │       ├── SidebarMenu.vue    # 侧边菜单（动态渲染、折叠支持）
│       │       ├── SidebarMenuItem.vue # 菜单项递归组件
│       │       ├── TopBar.vue         # 顶栏（折叠、全屏、主题、用户信息、退出）
│       │       └── TagsView.vue       # 标签页导航（关闭、刷新、右键操作）
│       ├── router/
│       │   ├── index.ts           # 路由实例与全局守卫
│       │   └── static-routes.ts   # 静态路由定义
│       ├── stores/
│       │   ├── auth.ts            # 认证状态（Token、用户、权限、菜单）
│       │   ├── app.ts             # 应用状态（侧边栏折叠、主题面板）
│       │   └── tabs.ts            # 标签页状态
│       ├── styles/
│       │   ├── element.scss       # Element Plus 主题定制
│       │   └── layout.scss        # 布局样式变量与全局样式
│       ├── utils/
│       │   └── status.ts          # 状态工具函数
│       ├── views/
│       │   ├── login/LoginView.vue         # 登录页
│       │   ├── dashboard/DashboardView.vue # 仪表盘
│       │   ├── errors/
│       │   │   ├── ForbiddenView.vue       # 403 无权限
│       │   │   ├── NotFoundView.vue        # 404 页面不存在
│       │   │   └── ServerErrorView.vue     # 500 服务器错误
│       │   ├── system/
│       │   │   ├── UserView.vue            # 用户管理
│       │   │   ├── RoleView.vue            # 角色管理
│       │   │   ├── MenuView.vue            # 菜单管理
│       │   │   ├── DeptView.vue            # 部门管理
│       │   │   ├── PostView.vue            # 岗位管理
│       │   │   ├── DictView.vue            # 字典管理
│       │   │   ├── ConfigView.vue          # 参数配置
│       │   │   ├── LoginLogView.vue        # 登录日志
│       │   │   └── OperationLogView.vue    # 操作日志
│       │   └── examples/
│       │       ├── ListView.vue            # 列表页示例
│       │       ├── FormView.vue            # 表单页示例
│       │       └── DetailView.vue          # 详情页示例
│       └── tests/                 # 前端单元测试
│           ├── auth-store.spec.ts
│           ├── login-view.spec.ts
│           ├── page-table.spec.ts
│           ├── permission.spec.ts
│           ├── sidebar-menu.spec.ts
│           ├── status.spec.ts
│           ├── system-api.spec.ts
│           ├── top-bar.spec.ts
│           └── user-view-crud.spec.ts
│
└── docs/                          # 项目文档
    └── guide/
        ├── quick-start.md         # 快速启动指南
        ├── architecture.md        # 架构设计说明
        ├── permission-model.md    # 权限模型说明
        ├── add-module.md          # 新增模块指南
        └── deployment.md          # 生产部署指南
```

---

## 功能特性

### 认证与权限

- **JWT 登录认证**：用户名密码登录，后端签发 JWT Token，前端自动注入请求头
- **RBAC 权限模型**：用户 -> 角色 -> 菜单 -> 权限码，四级权限控制
- **菜单权限**：控制前端页面可见性和导航菜单显示
- **按钮权限**：控制页面内操作按钮的显示与隐藏（如新增、编辑、删除）
- **后端强校验**：所有写接口在后端依赖层强制校验权限码，不依赖前端隐藏
- **管理员角色**：admin 角色自动绕过所有权限校验（超级管理员）
- **路由守卫**：未登录自动跳转登录页，Token 过期自动清除状态

### 系统管理

- **用户管理**：用户账号的增删改查，支持分配角色和岗位
- **角色管理**：角色的增删改查，支持分配菜单权限
- **菜单管理**：菜单树管理，支持目录、菜单、按钮三种类型
- **部门管理**：部门树管理，支持多级组织架构
- **岗位管理**：岗位的增删改查
- **字典管理**：字典类型和字典项管理（如状态、性别等枚举值）
- **参数配置**：系统级键值对配置项管理

### 审计日志

- **登录日志**：记录每次登录的用户名、结果、IP 地址、浏览器信息
- **操作日志**：记录每次写操作的操作人、权限码、请求方法、路径、IP 地址

### 前端能力

- **动态菜单**：根据用户权限从后端获取菜单数据，动态渲染侧边栏
- **标签页导航**：多标签页切换，支持关闭、刷新，Dashboard 固定不可关闭
- **侧边栏折叠**：一键展开/收起侧边栏
- **全屏模式**：一键切换全屏
- **主题切换**：支持主题色预览与切换
- **通用表格组件**：`PageTable` 支持分页、搜索、列配置、操作插槽
- **通用 CRUD 组件**：`SystemCrudPage` 声明式配置列和表单字段，自动生成增删改查页面
- **权限按钮组件**：`PermissionButton` 根据权限码控制按钮渲染
- **响应式布局**：桌面端优先，768px 断点适配移动端
- **示例页面**：列表页、表单页、详情页三种常见页面范式

### 后端能力

- **统一响应格式**：所有接口返回 `{ code, message, data, request_id }` 结构
- **统一异常处理**：AppError 业务异常、参数校验异常、未知异常统一捕获
- **请求 ID 追踪**：每个请求自动生成或透传 `X-Request-Id`，便于日志追踪
- **分页查询**：通用分页查询服务，支持 `page` 和 `page_size` 参数
- **软删除**：数据不物理删除，通过 `deleted_at` 字段标记，唯一键自动释放
- **Alembic 迁移**：数据库版本管理，支持向前和回滚
- **种子数据**：幂等初始化管理员账号、角色、菜单和权限

---

## 数据库设计

### 核心表（10 张）

| 表名 | 说明 | 关键字段 |
|---|---|---|
| `sys_user` | 用户表 | username, password_hash, nickname, email, mobile, dept_id, status, last_login_at |
| `sys_role` | 角色表 | code, name, data_scope, sort, status |
| `sys_menu` | 菜单表 | parent_id, type, title, path, component, permission, icon, sort, status |
| `sys_dept` | 部门表 | parent_id, ancestors, name, sort, status |
| `sys_post` | 岗位表 | code, name, sort, status |
| `sys_dict_type` | 字典类型表 | code, name, status |
| `sys_dict_item` | 字典项表 | dict_type_id, value, label, sort, status |
| `sys_config` | 参数配置表 | key, value, name, remark |
| `sys_login_log` | 登录日志表 | username, success, message, ip_address, user_agent |
| `sys_operation_log` | 操作日志表 | username, permission, title, method, path, ip_address, success, message |

### 关联表（3 张）

| 表名 | 说明 |
|---|---|
| `sys_user_role` | 用户-角色关联（多对多） |
| `sys_role_menu` | 角色-菜单关联（多对多） |
| `sys_user_post` | 用户-岗位关联（多对多） |

### 通用字段

所有核心实体表均包含以下通用字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | Integer | 主键，自增 |
| `created_at` | DateTime | 创建时间 |
| `updated_at` | DateTime | 更新时间 |
| `created_by` | Integer | 创建人 ID |
| `updated_by` | Integer | 更新人 ID |
| `deleted_at` | DateTime | 软删除时间（NULL 表示未删除） |

### 实体关系

```
User ──┬── N:N ── Role ── N:N ── Menu
       ├── N:1 ── Dept (树形结构)
       └── N:N ── Post

DictType ── 1:N ── DictItem

Menu ── 树形结构（parent_id 自引用）
Dept ── 树形结构（parent_id + ancestors 祖级路径）
```

---

## 权限模型

### 认证流程

```
1. 用户提交用户名和密码
2. 后端校验密码哈希、用户状态、角色状态
3. 后端签发 JWT access_token（默认 120 分钟过期）
4. 前端存储 Token 到 localStorage
5. 前端每次请求自动携带 Authorization: Bearer <token>
6. 前端调用 /auth/me 获取用户信息、角色、菜单、权限码
7. 前端根据菜单动态渲染导航和路由
```

### RBAC 权限结构

```
用户（User）
  └── 角色（Role）── 可分配多个
        └── 菜单（Menu）── 可分配多个
              ├── 菜单权限（type=menu）── 控制页面可见性
              └── 按钮权限（type=button）── 控制操作按钮显示
```

### 权限码命名规范

```
{模块}:{资源}:{操作}

示例：
  system:user:list      查看用户列表
  system:user:create    创建用户
  system:user:update    编辑用户
  system:user:delete    删除用户
  system:role:list      查看角色列表
  dashboard:view        查看仪表盘
```

### 权限校验规则

- **菜单权限**：决定前端侧边栏显示哪些菜单项、哪些路由可访问
- **按钮权限**：决定页面内操作按钮是否渲染（纯前端控制，提升用户体验）
- **接口权限**：后端通过 `require_permission()` 依赖强制校验，不依赖前端隐藏
- **管理员绕过**：角色 code 为 `admin` 时自动放行所有权限校验
- **数据权限**：第一版保留 `data_scope` 字段扩展点，暂不实现按部门/本人过滤

### 种子数据默认权限

种子脚本会创建以下默认数据：

**管理员账号**：`admin / Admin123!`

**页面菜单**（10 个）：

| 菜单 | 路由 | 权限码 |
|---|---|---|
| 仪表盘 | /dashboard | dashboard:view |
| 用户管理 | /system/users | system:user:list |
| 角色管理 | /system/roles | system:role:list |
| 菜单管理 | /system/menus | system:menu:list |
| 部门管理 | /system/depts | system:dept:list |
| 岗位管理 | /system/posts | system:post:list |
| 字典管理 | /system/dicts | system:dict:list |
| 参数配置 | /system/configs | system:config:list |
| 登录日志 | /system/login-logs | system:login-log:list |
| 操作日志 | /system/operation-logs | system:operation-log:list |

**按钮权限**（21 个）：每个 CRUD 模块包含 create、update、delete 三个按钮权限。

---

## API 接口

### 接口规范

- **基础路径**：`/api/v1`
- **认证方式**：请求头 `Authorization: Bearer <token>`
- **响应格式**：

```json
{
  "code": 0,
  "message": "ok",
  "data": {},
  "request_id": "uuid"
}
```

- **列表响应**：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [],
    "total": 0,
    "page": 1,
    "page_size": 20
  },
  "request_id": "uuid"
}
```

- **错误码**：

| 错误码 | HTTP 状态码 | 说明 |
|---|---|---|
| 100401 | 401 | 未登录或 Token 已过期 |
| 100403 | 403 | 无权限访问 |
| 100404 | 404 | 资源不存在 |
| 100422 | 422 | 参数校验错误 |
| 100500 | 500 | 服务器内部错误 |

### 认证接口

| 方法 | 路径 | 说明 | 需要认证 |
|---|---|---|---|
| POST | `/api/v1/auth/login` | 用户登录 | 否 |
| GET | `/api/v1/auth/me` | 获取当前用户信息（含角色、权限、菜单） | 是 |

### 健康检查

| 方法 | 路径 | 说明 | 需要认证 |
|---|---|---|---|
| GET | `/api/v1/health` | 服务健康检查 | 否 |

### 系统管理接口

所有系统管理接口均需要认证，写接口自动记录操作日志。

#### 用户管理

| 方法 | 路径 | 权限码 | 说明 |
|---|---|---|---|
| GET | `/api/v1/system/users` | system:user:list | 用户列表（分页） |
| POST | `/api/v1/system/users` | system:user:create | 创建用户 |
| PUT | `/api/v1/system/users/{id}` | system:user:update | 更新用户 |
| DELETE | `/api/v1/system/users/{id}` | system:user:delete | 删除用户（软删除） |

#### 角色管理

| 方法 | 路径 | 权限码 | 说明 |
|---|---|---|---|
| GET | `/api/v1/system/roles` | system:role:list | 角色列表（分页） |
| POST | `/api/v1/system/roles` | system:role:create | 创建角色 |
| PUT | `/api/v1/system/roles/{id}` | system:role:update | 更新角色 |
| DELETE | `/api/v1/system/roles/{id}` | system:role:delete | 删除角色（软删除） |

#### 菜单管理

| 方法 | 路径 | 权限码 | 说明 |
|---|---|---|---|
| GET | `/api/v1/system/menus` | system:menu:list | 菜单列表（分页） |
| POST | `/api/v1/system/menus` | system:menu:create | 创建菜单 |
| PUT | `/api/v1/system/menus/{id}` | system:menu:update | 更新菜单 |
| DELETE | `/api/v1/system/menus/{id}` | system:menu:delete | 删除菜单（软删除） |

#### 部门管理

| 方法 | 路径 | 权限码 | 说明 |
|---|---|---|---|
| GET | `/api/v1/system/depts` | system:dept:list | 部门列表（分页） |
| POST | `/api/v1/system/depts` | system:dept:create | 创建部门 |
| PUT | `/api/v1/system/depts/{id}` | system:dept:update | 更新部门 |
| DELETE | `/api/v1/system/depts/{id}` | system:dept:delete | 删除部门（软删除） |

#### 岗位管理

| 方法 | 路径 | 权限码 | 说明 |
|---|---|---|---|
| GET | `/api/v1/system/posts` | system:post:list | 岗位列表（分页） |
| POST | `/api/v1/system/posts` | system:post:create | 创建岗位 |
| PUT | `/api/v1/system/posts/{id}` | system:post:update | 更新岗位 |
| DELETE | `/api/v1/system/posts/{id}` | system:post:delete | 删除岗位（软删除） |

#### 字典管理

| 方法 | 路径 | 权限码 | 说明 |
|---|---|---|---|
| GET | `/api/v1/system/dict-types` | system:dict:list | 字典类型列表（分页） |
| POST | `/api/v1/system/dict-types` | system:dict:create | 创建字典类型 |
| PUT | `/api/v1/system/dict-types/{id}` | system:dict:update | 更新字典类型 |
| DELETE | `/api/v1/system/dict-types/{id}` | system:dict:delete | 删除字典类型（软删除） |
| GET | `/api/v1/system/dict-items` | system:dict:list | 字典项列表（分页） |
| POST | `/api/v1/system/dict-items` | system:dict:create | 创建字典项 |
| PUT | `/api/v1/system/dict-items/{id}` | system:dict:update | 更新字典项 |
| DELETE | `/api/v1/system/dict-items/{id}` | system:dict:delete | 删除字典项（软删除） |

#### 参数配置

| 方法 | 路径 | 权限码 | 说明 |
|---|---|---|---|
| GET | `/api/v1/system/configs` | system:config:list | 配置列表（分页） |
| POST | `/api/v1/system/configs` | system:config:create | 创建配置 |
| PUT | `/api/v1/system/configs/{id}` | system:config:update | 更新配置 |
| DELETE | `/api/v1/system/configs/{id}` | system:config:delete | 删除配置（软删除） |

#### 审计日志

| 方法 | 路径 | 权限码 | 说明 |
|---|---|---|---|
| GET | `/api/v1/system/login-logs` | system:login-log:list | 登录日志列表（分页，只读） |
| GET | `/api/v1/system/operation-logs` | system:operation-log:list | 操作日志列表（分页，只读） |

### Swagger 文档

后端启动后，访问以下地址查看自动生成的 API 文档：

- Swagger UI：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`

---

## 前端页面

### 页面路由

| 路径 | 页面 | 说明 |
|---|---|---|
| `/login` | 登录页 | 用户名密码登录 |
| `/dashboard` | 仪表盘 | 登录后默认首页 |
| `/system/users` | 用户管理 | 用户 CRUD |
| `/system/roles` | 角色管理 | 角色 CRUD |
| `/system/menus` | 菜单管理 | 菜单树 CRUD |
| `/system/depts` | 部门管理 | 部门树 CRUD |
| `/system/posts` | 岗位管理 | 岗位 CRUD |
| `/system/dicts` | 字典管理 | 字典类型和字典项 CRUD |
| `/system/configs` | 参数配置 | 系统配置 CRUD |
| `/system/login-logs` | 登录日志 | 只读查看 |
| `/system/operation-logs` | 操作日志 | 只读查看 |
| `/examples/list` | 列表示例 | 标准列表页范式 |
| `/examples/form` | 表单示例 | 表单校验范式 |
| `/examples/detail` | 详情示例 | 只读详情范式 |
| `/403` | 无权限 | 403 错误页 |
| `/404` | 未找到 | 404 错误页 |
| `/500` | 服务器错误 | 500 错误页 |

### 布局结构

```
┌──────────────────────────────────────────────────┐
│                  TopBar 顶栏                      │
│  [折叠] 后台管理                    [全屏] [主题] [用户▼] │
├──────────┬───────────────────────────────────────┤
│          │           TagsView 标签页              │
│ Sidebar  │  [仪表盘] [用户管理] [角色管理] ...       │
│ 侧边栏    ├───────────────────────────────────────┤
│          │                                       │
│ ┌──────┐ │           内容区域                      │
│ │ OA   │ │                                       │
│ └──────┘ │      当前页面内容                       │
│          │                                       │
│ □ 仪表盘  │                                       │
│ □ 系统管理│                                       │
│   □ 用户 │                                       │
│   □ 角色 │                                       │
│   □ 菜单 │                                       │
│   ...    │                                       │
│          │                                       │
└──────────┴───────────────────────────────────────┘
```

### 前端状态管理

| Store | 说明 |
|---|---|
| `authStore` | Token 管理、用户信息、角色、权限码、菜单数据、登录/登出 |
| `appStore` | 侧边栏折叠状态、主题面板开关 |
| `tabsStore` | 标签页列表、添加/关闭/清空标签页 |

---

## 快速启动

### 环境要求

- **Docker Desktop**：用于运行 MySQL
- **Python 3.12+**：后端运行环境
- **Node.js 20+**：前端运行环境

### 第一步：克隆仓库

```bash
git clone https://github.com/Jonesxq/admin-fram.git
cd admin-fram
```

### 第二步：启动 MySQL

```bash
docker compose up -d mysql
```

等待 MySQL 就绪（首次启动需要拉取镜像）：

```bash
docker compose ps
# 确认 open-admin-mysql 状态为 healthy
```

### 第三步：启动后端

```bash
cd backend

# 创建并激活虚拟环境
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Linux / macOS
source .venv/bin/activate

# 创建环境变量文件
cp .env.example .env

# 安装依赖
pip install -e ".[dev]"

# 执行数据库迁移
alembic upgrade head

# 初始化种子数据（管理员账号、角色、菜单）
python -m app.seed

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端启动后访问：
- API 服务：`http://localhost:8000`
- Swagger 文档：`http://localhost:8000/docs`
- ReDoc 文档：`http://localhost:8000/redoc`

### 第四步：启动前端

在新的终端窗口中执行：

```bash
cd frontend

# 创建环境变量文件
cp .env.example .env

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端启动后访问：`http://localhost:5173`

### 第五步：登录系统

打开浏览器访问 `http://localhost:5173`，使用默认管理员账号登录：

```
用户名：admin
密码：Admin123!
```

> **安全提示**：默认密码仅用于本地开发。生产环境或共享环境必须修改密码，并在 `.env` 中设置 `ALLOW_DEFAULT_ADMIN_PASSWORD=0`。

---

## 环境变量配置

### 后端环境变量（backend/.env）

| 变量名 | 默认值 | 说明 |
|---|---|---|
| `APP_NAME` | Open Admin API | 应用名称 |
| `API_PREFIX` | /api/v1 | API 路由前缀 |
| `DATABASE_URL` | sqlite+pysqlite:///:memory: | 数据库连接字符串 |
| `JWT_SECRET_KEY` | test-secret | JWT 签名密钥（生产环境必须修改） |
| `JWT_EXPIRE_MINUTES` | 120 | Token 过期时间（分钟） |
| `INITIAL_ADMIN_PASSWORD` | （空） | 种子数据管理员密码 |
| `ALLOW_DEFAULT_ADMIN_PASSWORD` | false | 是否允许使用默认密码 Admin123! |
| `CORS_ORIGINS` | http://localhost:5173,... | CORS 允许的来源（逗号分隔或 JSON 数组） |

### 前端环境变量（frontend/.env）

| 变量名 | 默认值 | 说明 |
|---|---|---|
| `VITE_API_BASE_URL` | /api/v1 | 后端 API 基础地址 |

### Docker Compose 环境变量

| 变量名 | 默认值 | 说明 |
|---|---|---|
| `MYSQL_ROOT_PASSWORD` | root_password | MySQL root 密码 |
| `MYSQL_DATABASE` | open_admin | 数据库名称 |
| `MYSQL_USER` | open_admin | 数据库用户 |
| `MYSQL_PASSWORD` | open_admin_password | 数据库密码 |
| `MYSQL_PORT` | 3306 | 映射到宿主机的端口 |

---

## 开发命令

### 后端命令

```bash
cd backend

# 安装依赖（包含开发工具）
pip install -e ".[dev]"

# 数据库迁移
alembic upgrade head            # 执行迁移到最新版本
alembic revision --autogenerate -m "描述"  # 生成新迁移
alembic downgrade -1            # 回滚一个版本

# 种子数据
python -m app.seed              # 初始化管理员、角色、菜单

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 测试
python -m pytest -v             # 运行全部测试
python -m pytest tests/test_auth.py -v  # 运行指定测试

# 代码检查
python -m ruff check .          # 静态检查
python -m ruff check --fix .    # 自动修复
python -m ruff format .         # 格式化
```

### 前端命令

```bash
cd frontend

# 安装依赖
npm install

# 开发
npm run dev                     # 启动开发服务器（端口 5173）

# 构建
npm run build                   # TypeScript 检查 + 生产构建

# 测试
npm test                        # 运行全部测试
npm run typecheck               # TypeScript 类型检查
```

### Docker 命令

```bash
# 启动 MySQL
docker compose up -d mysql

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f mysql

# 停止
docker compose down

# 停止并删除数据卷（会丢失数据）
docker compose down -v
```

### 验证全部检查

```bash
# 后端
cd backend && python -m pytest -v && python -m ruff check .

# 前端
cd frontend && npm test && npm run typecheck && npm run build

# Docker
docker compose config
```

---

## 新增业务模块指南

以新增"公告管理"模块为例，完整步骤如下：

### 1. 创建数据模型

在 `backend/app/models/system.py` 中添加 `Notice` 模型，或创建新文件 `backend/app/models/notice.py`。

### 2. 生成数据库迁移

```bash
cd backend
alembic revision --autogenerate -m "add notice table"
alembic upgrade head
```

### 3. 创建请求/响应模型

在 `backend/app/schemas/` 下创建 `notice.py`，定义 `NoticeCreate`、`NoticeUpdate`、`NoticeItem` 等 Pydantic 模型。

### 4. 实现业务服务

在 `backend/app/services/` 下创建 `notice_service.py`，复用 `system_service.py` 中的通用 CRUD 函数。

### 5. 添加后端接口

在 `backend/app/api/v1/system.py` 或新建路由文件中添加接口，使用 `require_permission()` 依赖校验权限。

### 6. 添加前端 API

在 `frontend/src/api/system.ts` 中添加 `listNotices`、`createNotice` 等 API 函数。

### 7. 创建前端页面

在 `frontend/src/views/system/` 下创建 `NoticeView.vue`，使用 `SystemCrudPage` 组件声明式配置。

### 8. 注册路由和菜单

- 在 `frontend/src/router/static-routes.ts` 中添加路由
- 在 `backend/app/seed.py` 中添加菜单种子数据（或手动在菜单管理页面添加）

### 9. 添加测试

- 后端：在 `backend/tests/` 下添加接口测试
- 前端：在 `frontend/tests/` 下添加组件测试

---

## 生产部署

### 前端构建

```bash
cd frontend

# 设置后端 API 地址
echo "VITE_API_BASE_URL=https://your-api-domain.com/api/v1" > .env

# 构建
npm run build
# 产物在 dist/ 目录，部署到 Nginx 或其他静态文件服务器
```

### 后端部署

```bash
cd backend

# 设置环境变量
export DATABASE_URL=mysql+pymysql://user:password@host:3306/dbname
export JWT_SECRET_KEY=your-very-strong-secret-key
export CORS_ORIGINS=https://your-frontend-domain.com

# 执行迁移
alembic upgrade head

# 初始化种子数据（首次部署）
python -m app.seed

# 启动 ASGI 服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 生产注意事项

- **JWT 密钥**：必须使用强随机字符串，不能使用默认值
- **数据库密码**：必须修改默认密码
- **HTTPS**：生产环境建议使用 HTTPS
- **同源部署**：推荐前后端部署在同一域名下，避免 CORS 问题
- **MySQL 版本**：推荐 MySQL 8.0+
- **CI 检查**：发布前确保前端 lint、typecheck、test，后端 ruff、pytest 全部通过

---

## 常见问题

### Q: 种子数据重复执行会报错吗？

不会。种子脚本使用幂等逻辑（upsert by unique key），重复执行是安全的。

### Q: 如何修改默认管理员密码？

在 `backend/.env` 中设置 `INITIAL_ADMIN_PASSWORD=你的强密码`，然后重新执行 `python -m app.seed`。

### Q: 如何添加新的角色和权限？

1. 在角色管理页面创建新角色
2. 在菜单管理页面创建权限码（type=button）
3. 在角色管理页面为角色分配菜单权限
4. 在用户管理页面为用户分配角色

### Q: 前端如何控制按钮显示？

使用 `PermissionButton` 组件：

```vue
<PermissionButton
  type="primary"
  permission="system:user:create"
  @click="handleCreate"
>
  新增用户
</PermissionButton>
```

### Q: 如何重置数据库？

```bash
docker compose down -v       # 删除数据卷
docker compose up -d mysql   # 重新启动
alembic upgrade head         # 重新迁移
python -m app.seed           # 重新种子
```

### Q: 后端测试使用什么数据库？

测试默认使用 SQLite 内存数据库，无需启动 MySQL。测试配置在 `backend/tests/conftest.py` 中。

---

## 参与贡献

欢迎参与贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解提交规范和开发流程。

提交前请确保：

```bash
# 后端检查
cd backend && python -m pytest -v && python -m ruff check .

# 前端检查
cd frontend && npm test && npm run typecheck && npm run build
```

---

## 开源协议

本项目基于 [MIT License](LICENSE) 开源。

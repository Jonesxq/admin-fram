# Quick Start

This guide starts Open Admin locally on Windows PowerShell with MySQL, FastAPI, and Vite.

## Prerequisites

- Docker Desktop
- Python 3.12+
- Node.js 20+
- npm

## 1. Start MySQL

Run from the repository root:

```powershell
docker compose up -d mysql
```

## 2. Configure Backend

Create `backend/.env` from the example:

```powershell
Copy-Item backend\.env.example backend\.env
```

For the local demo account, temporarily edit `backend/.env` so it contains these values:

```env
DATABASE_URL=mysql+pymysql://open_admin:open_admin_password@127.0.0.1:3306/open_admin
JWT_SECRET_KEY=change-me-in-local-env
INITIAL_ADMIN_PASSWORD=Admin123!
ALLOW_DEFAULT_ADMIN_PASSWORD=1
```

`Admin123!` is only for local development. For any shared, staging, or production deployment, change `INITIAL_ADMIN_PASSWORD` and keep `ALLOW_DEFAULT_ADMIN_PASSWORD=0`.

## 3. Install and Run Backend

Run these commands in Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is available at `http://localhost:8000/api/v1`.

## 4. Configure Frontend

Open a second PowerShell window from the repository root:

```powershell
Copy-Item frontend\.env.example frontend\.env
```

The local frontend env should contain:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 5. Install and Run Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually `http://localhost:5173`.

## Default Local Account

```text
admin / Admin123!
```

This account is for local development only. Non-local deployments must use a different password before running the seed command.

## Re-running Setup

`alembic upgrade head` is safe to run repeatedly. If the database is already at the latest migration, Alembic leaves it unchanged.

`python -m app.seed` upserts the base admin role, menu records, button permission records, and role-permission bindings. If the `admin` user already exists, seed keeps that user and does not reset the admin password.

## Useful Checks

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

# Deployment

This guide summarizes the pieces required to deploy Open Admin outside local development.

## Frontend Build

Set the backend API base URL before building:

```env
VITE_API_BASE_URL=/api/v1
```

Build the static assets:

```powershell
cd frontend
npm install
npm run build
```

Deploy `frontend/dist/` to a static web server or CDN. Configure history fallback to `index.html` because the app uses Vue Router history mode.

The current recommended deployment is same-origin: serve the frontend and reverse proxy `/api/v1` to the backend ASGI service from the same public origin.

## Backend ASGI Runtime

Install backend dependencies in an isolated Python environment and run the FastAPI app with an ASGI server:

```powershell
cd backend
python -m pip install .
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For production, run Uvicorn behind a process manager or container orchestrator and terminate TLS at a reverse proxy or load balancer.

## Required Environment Variables

Configure at least:

```env
APP_NAME=Open Admin API
API_PREFIX=/api/v1
DATABASE_URL=mysql+pymysql://open_admin:<password>@<mysql-host>:3306/open_admin
JWT_SECRET_KEY=<long-random-secret>
JWT_EXPIRE_MINUTES=120
CORS_ORIGINS=https://admin.example.com
INITIAL_ADMIN_PASSWORD=<strong-initial-password>
ALLOW_DEFAULT_ADMIN_PASSWORD=0
```

Do not use `Admin123!` outside local development. The seed command only allows that public default when `ALLOW_DEFAULT_ADMIN_PASSWORD=1`, and that opt-in is for local demos only.

## MySQL

Use MySQL 8.x with `utf8mb4` character set and `utf8mb4_unicode_ci` collation. Create a dedicated database user with the minimum permissions needed by the application.

Back up the database before migrations and before upgrading deployed code.

## Migrations and Seed

Run migrations before starting the new application version:

```powershell
cd backend
alembic upgrade head
```

Run seed only when bootstrapping or intentionally refreshing base roles, menus, and permissions:

```powershell
python -m app.seed
```

For production bootstrap, set a strong `INITIAL_ADMIN_PASSWORD` before running seed, log in once, and rotate the password according to your operational policy.

## Production Notes

- Set a strong unique `JWT_SECRET_KEY`.
- Keep `.env` files out of source control and deployment artifacts.
- Restrict database network access to the backend runtime.
- Serve the frontend and backend over HTTPS.
- Prefer same-origin frontend and API access through a reverse proxy. If you deploy the frontend and API on different origins, set `CORS_ORIGINS` to the exact frontend origins as a comma-separated string or JSON list. Do not combine wildcard origins with credentialed requests.
- Run `python -m pytest -v`, `python -m ruff check .`, `npm test`, `npm run typecheck`, and `npm run build` in CI before release.

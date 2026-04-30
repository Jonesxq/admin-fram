# Architecture

Open Admin is a front-end and back-end separated Monorepo. The repository keeps the local infrastructure, API service, web application, and project documentation together so a developer can start the full MVP from one checkout.

## Repository Layout

- `backend/`: FastAPI application, SQLAlchemy models, Alembic migrations, schemas, services, API routers, seed data, and tests.
- `frontend/`: Vue 3 application built with Vite, TypeScript, Element Plus, Pinia, Vue Router, API clients, views, layout components, and tests.
- `docs/`: design notes, implementation plans, and guide documents.
- `docker-compose.yml`: local MySQL service used by the development workflow.

## Backend Responsibility

The backend owns business data, authentication, authorization, persistence, and audit logs. It exposes versioned API routes under `/api/v1`, validates request and response data with Pydantic schemas, uses SQLAlchemy for database access, and uses Alembic for schema migrations.

The backend also performs the final permission decision for protected operations. Frontend checks improve the user experience, but backend dependencies such as `require_permission(...)` are the source of truth.

## Frontend Responsibility

The frontend owns the admin user interface. It handles login, token storage, route guards, menu rendering, tab state, table and form views, and calls the backend through typed API modules.

The frontend reads `VITE_API_BASE_URL` at build and dev-server startup. For local development it points to `http://localhost:8000/api/v1`.

## Runtime Flow

1. MySQL runs from Docker Compose and stores application data.
2. Alembic applies database migrations from the backend.
3. `python -m app.seed` creates the local admin role, user, menus, and permissions.
4. FastAPI serves the API with Uvicorn.
5. Vite serves the Vue application.
6. The user logs in from the frontend.
7. The backend validates credentials and returns a JWT access token.
8. The frontend sends the token in the `Authorization: Bearer <token>` header.
9. Backend dependencies load the current user, roles, and permissions before protected handlers run.

## Request Path

```text
Browser -> Vue view -> frontend API module -> Axios client
  -> FastAPI router -> dependency checks -> service layer
  -> SQLAlchemy session -> MySQL
```

Responses follow the backend response wrapper, so frontend modules should consume the wrapped `data` payload rather than assuming raw model objects.

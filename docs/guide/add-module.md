# Add a Module

Use this checklist when adding a new admin module. Keep permission strings stable and name them with the same resource/action pattern used by existing system modules, for example `system:user:list`.

## 1. Add the Model

Create or extend a SQLAlchemy model in `backend/app/models/`. Include common fields used by the existing services when the module needs paging, soft delete, status, or sorting.

## 2. Add the Migration

Generate an Alembic migration in `backend/` and review the generated operations before applying it.

```powershell
alembic revision --autogenerate -m "add <module> table"
alembic upgrade head
```

## 3. Add Schemas

Create Pydantic schemas in `backend/app/schemas/` for create, update, query, and response payloads. Keep API schemas separate from database models.

## 4. Add Service Logic

Add service functions in `backend/app/services/` when the module needs logic beyond the shared CRUD helpers. Put transaction-sensitive work behind one service boundary so API handlers stay small.

## 5. Add Backend APIs

Register routes under the `/api/v1` router. Add `require_permission(...)` to every protected endpoint, including list, detail, create, update, delete, export, and any custom action.

## 6. Add Frontend API Methods

Create a frontend API module in `frontend/src/api/`. Keep URLs and request payload types close to the module so views do not hard-code endpoint paths.

## 7. Add Pages

Create the Vue page under `frontend/src/views/`. Use existing table, layout, and permission-button patterns. Read permissions from the auth store instead of duplicating role logic in the view.

## 8. Add Menu Seed Data

Update `backend/app/seed.py` with the module menu and button permissions. Include at least the list permission for the page and action permissions for create, update, and delete when those actions exist.

## 9. Add Tests

Add backend tests for service behavior, API success paths, and permission failures. Add frontend tests for API calls, view behavior, and permission-driven button visibility where the module adds meaningful UI logic.

Run the relevant checks before opening the change:

```powershell
cd backend
python -m pytest -v
python -m ruff check .
cd ../frontend
npm test
npm run typecheck
npm run build
```

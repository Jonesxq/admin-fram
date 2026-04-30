# Permission Model

Open Admin uses JWT authentication and RBAC authorization. Permissions are modeled as strings attached to menus and buttons, granted through roles, and enforced by the backend.

## JWT Authentication

Users log in with username and password. After successful authentication, the backend returns a JWT access token. The frontend stores the token in `localStorage` and sends it on API requests:

```text
Authorization: Bearer <access_token>
```

The backend decodes the token, reads the subject user id, loads the user from the database, and rejects missing, expired, invalid, disabled, or deleted users.

## RBAC

The core relationship is:

```text
User -> Roles -> Menus -> Permissions
```

A user can have multiple roles. Each enabled role can have multiple enabled menus or buttons. Permission strings such as `system:user:list` and `system:user:create` are collected from those menu records.

The built-in `admin` role is treated as a superuser role. Users with that role pass permission checks even when a specific permission string is not listed in the frontend state.

## Menu Permissions

Menu records represent navigable pages. They include fields such as title, path, component, status, sort order, and permission string. After login, the frontend receives the current user's menus and can render the sidebar based on those records.

Menu permissions control which pages are visible and which list endpoints a role can access. A page should still call protected backend APIs because visibility is not a security boundary.

## Button Permissions

Button records represent page-level actions such as create, update, and delete. The frontend can hide or show action buttons with `PermissionButton` by checking strings like `system:user:create`.

Button permissions are an interface affordance. They help users see only the actions they can perform, but they do not replace backend checks.

## Backend Strong Validation

Every protected backend handler must declare the required permission with `require_permission("...")`. The dependency checks the current user's roles and permissions before the handler runs.

Examples:

```python
Depends(require_permission("system:user:list"))
Depends(require_permission("system:user:create"))
```

This means a user cannot bypass authorization by manually calling an API endpoint that the frontend hid. New modules must add backend permission checks for every protected read and write operation.

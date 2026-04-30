from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.errors import AppError
from app.core.security import decode_access_token
from app.models.system import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    if credentials is None:
        raise unauthorized_error()

    try:
        payload = decode_access_token(credentials.credentials)
        subject = payload.get("sub")
    except jwt.PyJWTError as exc:
        raise unauthorized_error() from exc

    if not subject:
        raise unauthorized_error()

    user = (
        db.scalar(select(User).where(User.id == int(subject), User.deleted_at.is_(None)))
        if str(subject).isdigit()
        else None
    )
    if user is None or user.status != "enabled":
        raise unauthorized_error()

    return user


def unauthorized_error() -> AppError:
    return AppError(code=100401, message="未登录或登录已过期", status_code=401)

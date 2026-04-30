from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.logging import get_request_id
from app.core.responses import success
from app.models.system import User
from app.schemas.auth import LoginRequest
from app.services.auth_service import authenticate, build_current_user, build_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    payload: LoginRequest,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    user = authenticate(db, payload.username, payload.password)
    return success(build_token(user).model_dump(), request_id=get_request_id(request))


@router.get("/me")
def me(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    return success(build_current_user(current_user), request_id=get_request_id(request))

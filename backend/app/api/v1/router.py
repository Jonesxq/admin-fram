from fastapi import APIRouter, Request

from app.api.v1.auth import router as auth_router
from app.api.v1.system import router as system_router
from app.core.logging import get_request_id
from app.core.responses import success

router = APIRouter()
router.include_router(auth_router)
router.include_router(system_router)


@router.get("/health")
def health(request: Request) -> dict:
    return success({"status": "ok"}, request_id=get_request_id(request))

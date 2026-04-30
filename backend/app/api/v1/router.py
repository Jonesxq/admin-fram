from fastapi import APIRouter, Request

from app.core.logging import get_request_id
from app.core.responses import success

router = APIRouter()


@router.get("/health")
def health(request: Request) -> dict:
    return success({"status": "ok"}, request_id=get_request_id(request))

from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.core.errors import AppError
from app.main import app


def test_app_error_uses_standard_response(client: TestClient) -> None:
    router = APIRouter()

    @router.get("/test-error")
    def raise_error() -> None:
        raise AppError(code=100403, message="无权限", status_code=403)

    app.include_router(router, prefix="/api/v1")
    response = client.get("/api/v1/test-error")

    assert response.status_code == 403
    assert response.json()["code"] == 100403
    assert response.json()["message"] == "无权限"
    assert response.json()["data"] is None
    assert "request_id" in response.json()

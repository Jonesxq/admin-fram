from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.core.errors import AppError
from app.main import app


def _has_input_field(value: object) -> bool:
    if isinstance(value, dict):
        return "input" in value or any(_has_input_field(item) for item in value.values())
    if isinstance(value, list):
        return any(_has_input_field(item) for item in value)
    return False


def _get_with_temporary_router(client: TestClient, router: APIRouter, path: str, **kwargs: object):
    routes = list(app.router.routes)
    try:
        app.include_router(router, prefix="/api/v1")
        return client.get(path, **kwargs)
    finally:
        app.router.routes = routes


def test_app_error_uses_standard_response(client: TestClient) -> None:
    router = APIRouter()

    @router.get("/test-error")
    def raise_error() -> None:
        raise AppError(code=100403, message="无权限", status_code=403)

    response = _get_with_temporary_router(client, router, "/api/v1/test-error")

    assert response.status_code == 403
    assert response.json()["code"] == 100403
    assert response.json()["message"] == "无权限"
    assert response.json()["data"] is None
    assert "request_id" in response.json()


def test_app_error_echoes_request_id_in_body_and_header(client: TestClient) -> None:
    router = APIRouter()

    @router.get("/test-error-request-id")
    def raise_error() -> None:
        raise AppError(code=100403, message="无权限", status_code=403)

    response = _get_with_temporary_router(
        client,
        router,
        "/api/v1/test-error-request-id",
        headers={"x-request-id": "request-123"},
    )

    assert response.status_code == 403
    assert response.json()["request_id"] == "request-123"
    assert response.headers["X-Request-ID"] == "request-123"


def test_validation_error_details_strip_input_fields(client: TestClient) -> None:
    router = APIRouter()

    @router.get("/test-validation/{item_id}")
    def validate_item_id(item_id: int) -> dict[str, int]:
        return {"item_id": item_id}

    response = _get_with_temporary_router(client, router, "/api/v1/test-validation/not-an-int")

    assert response.status_code == 422
    assert response.json()["code"] == 100422
    assert response.json()["message"] == "参数校验失败"
    assert response.json()["data"] is None
    assert response.json()["details"]
    assert not _has_input_field(response.json()["details"])
    assert response.json()["request_id"] == response.headers["X-Request-ID"]

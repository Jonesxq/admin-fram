import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.errors import AppError
from app.core.logging import get_request_id

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


def _strip_validation_input(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: _strip_validation_input(item)
            for key, item in value.items()
            if key != "input"
        }
    if isinstance(value, list):
        return [_strip_validation_input(item) for item in value]
    return value


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request.state.request_id = get_request_id(request)
    try:
        response = await call_next(request)
    except Exception as exc:
        response = unhandled_error_handler(request, exc)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


@app.exception_handler(AppError)
def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "code": exc.code,
            "message": exc.message,
            "data": None,
            "details": exc.details,
            "request_id": get_request_id(request),
        }),
    )


@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "code": 100422,
            "message": "参数校验失败",
            "data": None,
            "details": _strip_validation_input(exc.errors()),
            "request_id": get_request_id(request),
        }),
    )


@app.exception_handler(Exception)
def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = get_request_id(request)
    logger.exception(
        "Unhandled request error",
        extra={"request_id": request_id},
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({
            "code": 100500,
            "message": "服务端错误",
            "data": None,
            "details": None,
            "request_id": request_id,
        }),
        headers={"X-Request-ID": request_id},
    )


app.include_router(api_v1_router, prefix=settings.api_prefix)

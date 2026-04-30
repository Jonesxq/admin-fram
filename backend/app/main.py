from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.errors import AppError
from app.core.logging import get_request_id

app = FastAPI(title=settings.app_name)


@app.exception_handler(AppError)
def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": None,
            "details": exc.details,
            "request_id": get_request_id(request),
        },
    )


@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "code": 100422,
            "message": "参数校验失败",
            "data": None,
            "details": exc.errors(),
            "request_id": get_request_id(request),
        },
    )


app.include_router(api_v1_router, prefix=settings.api_prefix)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ServiceError(Exception):
    status_code = 500
    code = "service_error"

    def __init__(self, message: str) -> None:
        self.message = message


class ForbiddenError(ServiceError):
    status_code = 403
    code = "forbidden"


class BadRequestError(ServiceError):
    status_code = 400
    code = "bad_request"


class NotFoundError(ServiceError):
    status_code = 404
    code = "not_found"


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ServiceError)
    async def handle_service_error(_: Request, exc: ServiceError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
        )

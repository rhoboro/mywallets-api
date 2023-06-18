from fastapi import FastAPI, Request, responses

class AppException(Exception):
    status_code: int = 500
    message: str = "Internal Server Error"
    details: dict | None = None

class NotFound(AppException):
    status_code: int = 404
    message: str = "Not Found"

    def __init__(
        self, resource: str, resource_id: int
    ) -> None:
        self.details = {resource: resource_id}

def init_exception_handler(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(
        req: Request, exc: AppException
    ):
        content = {"message": exc.message}
        if exc.details:
            content["details"] = exc.details
        return responses.JSONResponse(
            status_code=exc.status_code,
            content=content,
        )

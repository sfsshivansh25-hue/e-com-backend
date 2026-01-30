import traceback
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.logger import get_logger

logger = get_logger("errors")


class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except Exception as exc:
            request_id = getattr(request.state, "request_id", "unknown")

            logger.error(
                f"unhandled_exception request_id={request_id} "
                f"path={request.url.path} error={str(exc)}\n"
                f"{traceback.format_exc()}"
            )

            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "request_id": request_id,
                },
            )

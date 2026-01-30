import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import get_logger

logger = get_logger("request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.time()

        logger.info(
            f"request_start id={request_id} method={request.method} path={request.url.path}"
        )

        try:
            response: Response = await call_next(request)
        except Exception as exc:
            duration = round((time.time() - start_time) * 1000, 2)

            logger.error(
                f"request_error id={request_id} duration_ms={duration} error={str(exc)}"
            )
            raise

        duration = round((time.time() - start_time) * 1000, 2)

        logger.info(
            f"request_end id={request_id} status={response.status_code} duration_ms={duration}"
        )

        response.headers["X-Request-ID"] = request_id
        return response

from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.logger import setup_logger
from app.core.middleware import RequestLoggingMiddleware
from app.core.error_handler import ErrorLoggingMiddleware


app = FastAPI(title=settings.APP_NAME)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorLoggingMiddleware)
app.include_router(api_router)
setup_logger("INFO")



@app.get("/health")
async def health_check():
    return {"status": "ok"}



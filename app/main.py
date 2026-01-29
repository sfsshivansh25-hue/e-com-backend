from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router


app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
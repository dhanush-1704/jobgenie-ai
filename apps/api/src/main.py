from fastapi import FastAPI

from src.api.router import router
from src.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(
    router,
    prefix=settings.API_PREFIX,
)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} 🚀"
    }
from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to StockPilot API 🚀"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
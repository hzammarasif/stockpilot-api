from fastapi import FastAPI
from app.api.router import api_router

from app.core.config import settings
from app.core.exception_handler import (
    register_exception_handlers,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
)

register_exception_handlers(app)

app.include_router(
    api_router,
    prefix="/api/v1",
)
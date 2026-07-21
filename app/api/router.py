from fastapi import APIRouter

from app.api.v1 import auth
from app.api.v1.company import router as company_router

api_router = APIRouter()

api_router.include_router(auth.router)

api_router.include_router(company_router)
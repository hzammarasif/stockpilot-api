from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies.auth import get_auth_service
from app.schemas.auth import Token, UserLogin, UserRegister
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: UserRegister,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return await auth_service.register_user(data)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    return await auth_service.login(data)
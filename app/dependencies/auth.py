from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)


def get_auth_service(
    session: AsyncSession = Depends(get_session),
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        session=session,
    )

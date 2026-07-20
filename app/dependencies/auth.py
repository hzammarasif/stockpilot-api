from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession




from app.auth.jwt import decode_token
from app.core.exceptions import UnauthorizedException
from app.db.database import get_session
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService



oauth2_scheme = OAuth2PasswordBearer(           # Think of it as a token extractor
    tokenUrl="/api/v1/auth/login",
)

def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)


def get_role_repository(
    session: AsyncSession = Depends(get_session),
) -> RoleRepository:
    return RoleRepository(session)

def get_auth_service(
    session: AsyncSession = Depends(get_session),
    user_repository: UserRepository = Depends(get_user_repository),
    role_repository: RoleRepository = Depends(get_role_repository),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        role_repository=role_repository,
        session=session,
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository) 
) -> User:
    payload = decode_token(token)
    if payload.type != "access":
        raise UnauthorizedException()
    user = await user_repository.get_by_id(payload.sub)

    if not user:
        raise UnauthorizedException()

    return user
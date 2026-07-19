from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token
from app.core.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token, UserLogin, UserRegister
from app.schemas.user import UserResponse


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        session: AsyncSession,
    ) -> None:
        self.user_repository = user_repository
        self.session = session

    async def register_user(
        self,
        data: UserRegister,
    ) -> UserResponse:

        if await self.user_repository.exists_by_email(data.email):
            raise EmailAlreadyExistsException()

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
        )

        try:
            await self.user_repository.create(user)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return UserResponse.model_validate(user)

    async def login(
        self,
        data: UserLogin,
    ) -> Token:

        user = await self.user_repository.get_by_email(data.email)

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(
            data.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            subject=str(user.id),
        )

        refresh_token = create_refresh_token(
            subject=str(user.id),
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )
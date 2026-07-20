from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token
from app.core.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token, UserLogin, UserRegister
from app.schemas.user import UserResponse


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        session: AsyncSession,
    ) -> None:
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.session = session

    async def register_user(
        self,
        data: UserRegister,
    ) -> UserResponse:

        if await self.user_repository.exists_by_email(data.email):
            raise EmailAlreadyExistsException()

        default_role = await self.role_repository.get_by_name("employee")

        print("=" * 50)
        print("DEFAULT ROLE:", default_role)
        print("ROLE ID:", default_role.id if default_role else None)
        print("=" * 50)

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            role_id=default_role.id,
        )

        print("USER ROLE ID:", user.role_id)
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            role_id=default_role.id,
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
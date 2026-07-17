from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.auth.hashing import hash_password
from app.models.user import User
from app.schemas.auth import UserRegister
from app.schemas.user import UserResponse


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        session: AsyncSession,
    ) -> None:
        self.user_repository = user_repository
        self.session = session
    

    async def register_user(self,data: UserRegister) -> UserResponse:

        existing_user = await self.user_repository.get_by_email(data.email)

        if existing_user:
            raise ValueError("Email already exists")

        hashed_password = hash_password(data.password)

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password,
        )

        await self.user_repository.create(user)

        await self.session.commit()

        return UserResponse.model_validate(user)    
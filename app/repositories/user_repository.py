from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        return await self.exists(User.email == email)

    async def exists_by_username(self, username: str) -> bool:
        return await self.exists(User.username == username)
    
    async def get_by_id_with_role(self, user_id: int) -> User | None:
        stmt = (
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
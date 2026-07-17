from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository



async def exists_by_email(self, email: str) -> bool:
    return await self.exists(User.email == email)


async def exists_by_username(self, username: str) -> bool:
    return await self.exists(User.username == username)
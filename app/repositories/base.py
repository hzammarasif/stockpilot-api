from typing import Generic, TypeVar

from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)



FilterType = ColumnElement[bool]

class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelType],
    ):
        self.session = session
        self.model = model

    async def create(self, obj: ModelType)-> ModelType:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj;

    async def get_by_id(self, id: object)-> ModelType | None:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt);
        return result.scalar_one_or_none()
    

    async def get_one(
        self,
        *filters: ColumnElement[bool],
    ) -> ModelType | None:
        stmt = select(self.model).where(*filters)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
    

    from sqlalchemy import select

    async def get_all(self) -> list[ModelType]:
        stmt = select(self.model)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
    

    async def update(self, obj: ModelType) -> ModelType:
        await self.session.flush()
        await self.session.refresh(obj)
        return obj
    
    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)
        await self.session.flush()

    async def exists(self,*filters: FilterType) -> bool:


        stmt = select(
            exists().where(*filters)
        )

        result = await self.session.execute(stmt)

        return bool(result.scalar())

from app.models.company import Company
from app.repositories.base import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, session):
        super().__init__(session, Company)

    async def get_by_name(self, name: str) -> Company | None:
        return await self.get_one(Company.name == name)

    async def exists_by_name(self, name: str) -> bool:
        return await self.exists(Company.name == name)
    from pydantic import BaseModel, ConfigDict, Field


    
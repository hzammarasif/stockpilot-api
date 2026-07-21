from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CompanyAlreadyExistsException
from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate


class CompanyService:
    def __init__(
        self,
        company_repository: CompanyRepository,
        session: AsyncSession,
    ):
        self.company_repository = company_repository
        self.session = session

    async def create_company(
        self,
        data: CompanyCreate,
    ) -> Company:

        if await self.company_repository.exists_by_name(data.name):
            raise CompanyAlreadyExistsException("Company already exists.")

        company = Company(
            name=data.name,
        )

        await self.company_repository.create(company)

        await self.session.commit()

        return company
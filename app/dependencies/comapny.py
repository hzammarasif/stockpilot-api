from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.repositories.company_repository import CompanyRepository
from app.services.company_service import CompanyService


def get_company_repository(
    session: AsyncSession = Depends(get_session),
) -> CompanyRepository:
    return CompanyRepository(session)


def get_company_service(
    session: AsyncSession = Depends(get_session),
    company_repository: CompanyRepository = Depends(get_company_repository),
) -> CompanyService:
    return CompanyService(
        company_repository=company_repository,
        session=session,
    )
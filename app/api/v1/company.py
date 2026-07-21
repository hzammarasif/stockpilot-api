from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies.comapny import get_company_service
from app.schemas.company import CompanyCreate, CompanyResponse
from app.services.company_service import CompanyService

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_company(
    data: CompanyCreate,
    company_service: CompanyService = Depends(get_company_service),
) -> CompanyResponse:
    company = await company_service.create_company(data)
    return CompanyResponse.model_validate(company)
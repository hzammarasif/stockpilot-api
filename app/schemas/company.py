from pydantic import BaseModel, ConfigDict, Field


class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class CompanyUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class CompanyResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
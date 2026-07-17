from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    int: UUID
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True) 
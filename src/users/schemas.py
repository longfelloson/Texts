from datetime import datetime
import uuid
from pydantic import UUID4, BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    email: EmailStr
    hashed_password: str
    id: UUID4 = Field(..., default_factory=uuid.uuid4)
    created_at: datetime = Field(..., default_factory=datetime.now)


class User(BaseModel):
    id: UUID4
    email: EmailStr
    hashed_password: str
    created_at: datetime
    is_admin: bool = Field(default=False)


class UserCredentials(BaseModel):
    email: EmailStr
    password: str
    
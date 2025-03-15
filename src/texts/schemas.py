from datetime import datetime
from typing import Optional
import uuid
from pydantic import UUID4, BaseModel, Field, field_validator


class CreateText(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    body: str = Field(
        ..., min_length=1, description="Text body cannot be empty"
    )
    header: str = Field(
        ..., min_length=1, description="Header cannot be empty"
    )
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: Optional[datetime]

    @field_validator("expires_at")
    @classmethod
    def validate_expires_at(cls, value):
        if value and value <= datetime.now():
            raise ValueError("The date has to be in the future")
        return value


class Text(BaseModel):
    id: UUID4
    body: str
    created_at: datetime
    header: str
    expires_at: Optional[datetime]
    created_by: UUID4
    
from typing import Optional

from pydantic import BaseModel, field_validator

from python_fastapi.constants import VALID_EMAIL_DOMAIN, GenderEnum
from python_fastapi.utils import validate_password


class BaseReadSchema(BaseModel):
    id: int
    created_at: str
    updated_at: str

class BaseUserSchema(BaseModel):
    email: str
    username: str

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, email: str) -> str:
        if not email.endswith(VALID_EMAIL_DOMAIN):
            raise ValueError(f"Email must end with {VALID_EMAIL_DOMAIN}")
        return email

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if len(value) < 4:
            raise ValueError("Name must be at least 3 characters long")
        return value


class CreateUserSchema(BaseUserSchema):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        try:
            _ = validate_password(password)
        except ValueError as e:
            raise e
        return password


class ReadUserSchema(BaseReadSchema, BaseUserSchema):
    is_active: bool


class UpdateUserSchema(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if len(value) < 4:
            raise ValueError("Name must be at least 3 characters long")
        return value


class ResponseSchema(BaseModel):
    success: bool
    message: str
    data: any
    extras: Optional[dict] = None

    class Config:
        arbitrary_types_allowed=True
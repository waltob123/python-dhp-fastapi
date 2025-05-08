from pydantic import BaseModel, EmailStr

from email_validator import validate_email, EmailNotValidError


class CreateUserSchema(BaseModel):
    name: str
    email: EmailStr

    @classmethod
    def validate_email(cls, email: str) -> str:
        try:
            valid = validate_email(email)
            return email if valid else None
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {e}")

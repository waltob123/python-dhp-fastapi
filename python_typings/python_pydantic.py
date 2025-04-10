from typing import Optional

from pydantic import BaseModel, field_validator


class User(BaseModel):
    first_name: str
    last_name: str
    other_names: Optional[str] = None
    age: int
    hobbies: list[str]

    @field_validator("other_names", "last_name", "first_name")
    @classmethod
    def validate_other_names(cls, value: str) -> None:
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        if not value.isalpha():
            raise ValueError("Name must contain only letters")


new_user = User(first_name="John", last_name="Doe", age=23, hobbies=["reading", "gaming"])
print(new_user)
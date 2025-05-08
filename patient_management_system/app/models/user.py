import random
from app.dummy_data import users


class User:
    def __init__(self, name: str, email: str) -> None:
        self.id = random.randint(1, 1000000)
        self.name = name
        self.email = email
        users.append(self.to_dict())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    def __repr__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

    def __str__(self) -> str:
        return f"<User {self.email}>"

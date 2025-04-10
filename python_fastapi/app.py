from enum import Enum
from typing import Annotated, Optional

from fastapi import FastAPI, Body, Path
from pydantic import BaseModel, field_validator


app = FastAPI()


VALID_EMAIL_DOMAIN = "ghs.gov.gh"


class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"


class CreateUserSchema(BaseModel):
    email: str
    first_name: str
    last_name: str
    other_names: Optional[str] = None
    age: int
    gender: str

    @field_validator("other_names", "last_name", "first_name")
    @classmethod
    def validate_other_names(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        if not value.isalpha():
            raise ValueError("Name must contain only letters")
        return value

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, email: str) -> str:
        if not email.endswith(VALID_EMAIL_DOMAIN):
            raise ValueError(f"Email must end with {VALID_EMAIL_DOMAIN}")
        return email

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, gender: str) -> str:
        if not GenderEnum.__contains__(gender.lower()):
            raise ValueError("Gender must be one of these: {gender_list}".format(
                gender_list=[value.value for key, value in GenderEnum.__members__.items()])
            )
        return gender.lower()

    @field_validator("age")
    @classmethod
    def validate_age(cls, age: int) -> int:
        if age < 0:
            raise ValueError("Age must be a positive number")
        return age

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "other_names": self.other_names,
            "age": self.age,
            "gender": self.gender
        }



def check_email_uniqueness(email: str, list_of_users: list[dict]) -> bool:
    """
    Check if email is unique

    :param email: str
    :param list_of_users: list[dict]
    :return: bool
    """
    for user in list_of_users:
        if user.get("email") == email:
            return False
    return True


def get_user_from_list(user_id: int, users_list: list[dict]) -> dict | None:
    """
    Get user from list of users

    :param user_id: the id of the user to get
    :param users_list: the list of users to search from
    :return: dict
    """
    for user in users_list:
        if user.get("id") == user_id:
            return user
    return None

users = [
    {
        "id": 1,
        "name": "John Doe",
        "gender": "Male",
        "email": "john.doe@gmail.com"
    },
    {
        "id": 2,
        "name": "Kwame Atta",
        "gender": "Male",
        "email": "kwame.atta@gmail.com"
    },
    {
        "id": 3,
        "name": "Mary Jane",
        "gender": "Female",
        "email": "mary.jane@gmail.com"
    }
]


@app.get(path="/api/v1/users", status_code=200)
def get_all_users() -> list[dict]:
    """
    Get all users

    :return: dict
    """
    return users


@app.get(path="/api/v1/users/{user_id}", status_code=200)
def get_user(user_id: Annotated[int, Path(description="The id of the user to get")]) -> dict:
    """
    Get user by id

    :param user_id: int
    :return: dict
    """
    user = get_user_from_list(user_id, users)
    if not user:
        return {"error": "Not Found"}
    return user


@app.post(path="/api/v1/users", status_code=201)
def create_user(user: CreateUserSchema = Body()) -> dict:
    """
    Create a new user

    :param user: dictionary containing user data
    :return: dict
    """
    # check if email is unique
    if not check_email_uniqueness(user.email, users):
        return {"error": "Email already exists"}

    user_dict = user.to_dict()

    user_dict["id"] = len(users) + 1
    users.append(user_dict)

    return user_dict


@app.put(path="/api/v1/users/{user_id}", status_code=200)
def update_user(user_id: int = Path(), user_update_data: dict = Body()) -> dict:
    """
    Update user by id

    :param user_id: the id of the user to update
    :param user_update_data: the new data to update the user with
    :return: dict
    """
    user_to_update = get_user_from_list(user_id, users)

    if not user_to_update:
        return {"error": "Not Found"}

    # user_to_update.update(user_update_data)
    for key, value in user_update_data.items():
        if key in user_to_update.keys():
            user_to_update[key] = value
        else:
            print("skip")

    return user_to_update


@app.patch(path="/api/v1/users/{user_id}", status_code=200)
def update_user(user_id: int = Path(), user_update_data: dict = Body()) -> dict:
    """
    Update user by id

    :param user_id: the id of the user to update
    :param user_update_data: the new data to update the user with
    :return: dict
    """
    user_to_update = get_user_from_list(user_id, users)

    if not user_to_update:
        return {"error": "Not Found"}

    # user_to_update.update(user_update_data)
    for key, value in user_update_data.items():
        if key in user_to_update.keys():
            user_to_update[key] = value
        else:
            print("skip")

    return user_to_update


@app.delete(path="/api/v1/users/{user_id}", status_code=204)
def delete_user(user_id: int = Path()) -> None:
    """
    Delete user by id

    :param user_id: the id of the user to delete
    :return: dict
    """
    user_to_delete = get_user_from_list(user_id, users)

    if not user_to_delete:
        raise Exception("User not found")
        # return {"error": "Not Found"}

    # Alternate method to delete user
    # del users[users.index(user_to_delete)]
    users.remove(user_to_delete)

    # return {"message": "User deleted successfully"}
    return None

from datetime import datetime, timezone
from typing import Annotated

from fastapi import FastAPI, Body, Path, Query, status, HTTPException

from python_fastapi.helper_functions import get_user_from_list, check_email_uniqueness
from python_fastapi.models import User
from python_fastapi.schemas import ResponseSchema, ReadUserSchema, CreateUserSchema, UpdateUserSchema
from python_fastapi.users_data import users
from python_fastapi.utils import offset_calculator

app = FastAPI()


@app.get(path="/api/v1/users", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
def get_all_users(
    page: Annotated[int, Query(description="The page number to get", ge=1)] = None,
    page_size: Annotated[int, Query(description="The number of items to get per page", ge=1)] = None,
    is_active: Annotated[bool, Query(description="Filter by active status")] = None,
) -> ResponseSchema:
    """
    Get all users

    :return: dict
    """
    response = []

    if is_active is not None:
        for user in users:
            if user["is_active"] == is_active:
                response.append(user)

    if page and page_size:
        offset = offset_calculator(page, page_size)
        response = response[offset:offset + page_size]
        return ResponseSchema(
            success=True,
            message="Users retrieved successfully",
            data=[ReadUserSchema(**user).model_dump() for user in response],
            extras={
                "page": page,
                "page_size": page_size,
                "total_users": len(users)
            }
        )
    return ResponseSchema(
        success=True,
        message="Users retrieved successfully",
        data=[ReadUserSchema(**user).model_dump() for user in users],
    )




@app.get(path="/api/v1/users/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
def get_user(user_id: Annotated[int, Path(description="The id of the user to get")]) -> ResponseSchema:
    """
    Get user by id

    :param user_id: int
    :return: dict
    """
    user = get_user_from_list(user_id, users)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return ResponseSchema(
            success=True,
            message="Users retrieved successfully",
            data=ReadUserSchema(**user).model_dump()
        )


@app.post(path="/api/v1/users", status_code=status.HTTP_201_CREATED, response_model=ResponseSchema)
def create_user(user: CreateUserSchema = Body()) -> ResponseSchema:
    """
    Create a new user

    :param user: dictionary containing user data
    :return: dict
    """
    # check if email is unique
    if not check_email_uniqueness(user.email, users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists.")

    new_user = User(**user.model_dump())
    User.save(new_user.to_dict(), users)

    return ResponseSchema(
            success=True,
            message="User created successfully",
            data=ReadUserSchema(**new_user.to_dict()).model_dump()
    )


@app.put(path="/api/v1/users/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
def update_user(user_id: int = Path(), user_update_data: UpdateUserSchema = Body()) -> ResponseSchema:
    """
    Update user by id

    :param user_id: the id of the user to update
    :param user_update_data: the new data to update the user with
    :return: dict
    """
    user_to_update = get_user_from_list(user_id, users)

    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # user_to_update.update(user_update_data)
    for key, value in user_update_data.model_dump().items():
        if key in user_to_update.keys():
            user_to_update[key] = value
    user_to_update["updated_at"] = str(datetime.now(tz=timezone.utc))

    return ResponseSchema(
            success=True,
            message="User created successfully",
            data=ReadUserSchema(**user_to_update).model_dump()
    )


@app.patch(path="/api/v1/users/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
def update_user(user_id: int = Path(), user_update_data: UpdateUserSchema = Body()) -> ResponseSchema:
    """
    Update user by id

    :param user_id: the id of the user to update
    :param user_update_data: the new data to update the user with
    :return: dict
    """
    user_to_update = get_user_from_list(user_id, users)

    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # user_to_update.update(user_update_data)
    for key, value in user_update_data.model_dump().items():
        if key in user_to_update.keys():
            user_to_update[key] = value
    user_to_update["updated_at"] = str(datetime.now(tz=timezone.utc))

    return ResponseSchema(
        success=True,
        message="User created successfully",
        data=ReadUserSchema(**user_to_update).model_dump()
    )


@app.delete(path="/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int = Path()) -> None:
    """
    Delete user by id

    :param user_id: the id of the user to delete
    :return: dict
    """
    user_to_delete = get_user_from_list(user_id, users)

    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        # return {"error": "Not Found"}

    # Alternate method to delete user
    # del users[users.index(user_to_delete)]
    # users.remove(user_to_delete)
    user_to_delete["deleted_at"] = str(datetime.now(tz=timezone.utc))

    # return {"message": "User deleted successfully"}
    return None

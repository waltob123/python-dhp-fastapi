from datetime import datetime, timezone
from typing import Annotated

from fastapi import FastAPI, Body, Path, Query, status, HTTPException, Request

from python_fastapi.helper_functions import get_user_from_list
from python_fastapi.schemas import ResponseSchema, ReadUserSchema, CreateUserSchema, UpdateUserSchema
from python_fastapi.services import get_all_users_from_list, get_user_by_id, create_new_user, update_a_user
from python_fastapi.users_data import users
from python_fastapi.utils import generate_id

app = FastAPI()


@app.middleware("http")
async def process_request_and_response(request: Request, call_next):
    """
    Middleware to process request and response

    :param request: Request
    :param call_next: Callable
    :return: Response
    """
    response = await call_next(request)
    response.headers["X-Response-ID"] = str(generate_id())
    return response

@app.get(path="/api/v1/users", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
def get_all_users(
    request: Request,
    page: Annotated[int, Query(description="The page number to get", ge=1)] = None,
    page_size: Annotated[int, Query(description="The number of items to get per page", ge=1)] = None,
    is_active: Annotated[bool, Query(description="Filter by active status")] = None,
    is_deleted: Annotated[bool, Query(description="Filter by deleted status")] = None,
) -> ResponseSchema:
    """
    Get all users

    :return: dict
    """
    response = get_all_users_from_list(
        users=users, page=page, page_size=page_size, is_active=is_active, is_deleted=is_deleted)

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


@app.get(path="/api/v1/users/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
def get_user(user_id: Annotated[int, Path(description="The id of the user to get")]) -> ResponseSchema:
    """
    Get user by id

    :param user_id: int
    :return: dict
    """
    user = get_user_by_id(user_id, users)
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
    new_user = create_new_user(user, users)

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
    updated_user = update_a_user(user_id, user_update_data, users)

    return ResponseSchema(
            success=True,
            message="User created successfully",
            data=ReadUserSchema(**updated_user.to_dict()).model_dump()
    )


@app.patch(path="/api/v1/users/{user_id}", status_code=status.HTTP_200_OK, response_model=ResponseSchema)
def update_user(user_id: int = Path(), user_update_data: UpdateUserSchema = Body()) -> ResponseSchema:
    """
    Update user by id

    :param user_id: the id of the user to update
    :param user_update_data: the new data to update the user with
    :return: dict
    """
    updated_user = update_a_user(user_id, user_update_data, users)

    return ResponseSchema(
            success=True,
            message="User created successfully",
            data=ReadUserSchema(**updated_user.to_dict()).model_dump()
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

from datetime import datetime, timezone
from typing import Optional
from fastapi import HTTPException, status

from python_fastapi.helper_functions import get_user_from_list, check_email_uniqueness
from python_fastapi.models import User
from python_fastapi.schemas import CreateUserSchema, UpdateUserSchema


def offset_calculator(page: int, page_size: int) -> int:
    return (page - 1) * page_size


def get_all_users_from_list(
        users: list[dict],
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        is_active: Optional[bool] = None,
        is_deleted: Optional[bool] = None
) -> list[dict]:
    """
    Get all users

    :param users: The list of users to get
    :param page: The page number to get
    :param page_size: The number of items to get per page
    :param is_active: The active status to filter by
    :param is_deleted: The deleted status to filter by
    :return: A filtered and optionally paginated list of users
    """
    def user_matches(user: dict) -> bool:
        # TODO: fix is_deleted bug
        if is_active is not None and user["is_active"] != is_active:
            return False
        if is_deleted is True and user["deleted_at"] is None:
            return False
        if is_deleted is False and user["deleted_at"] is not None:
            return False
        return True

    filtered_users = [user for user in users if user_matches(user)]

    if page is not None and page_size is not None:
        offset = offset_calculator(page, page_size)
        return filtered_users[offset:offset + page_size]

    return filtered_users


def get_user_by_id(user_id: int, users_list: list[dict]) -> dict | None:
    """
    Get user from list of users

    :param user_id: the id of the user to get
    :param users_list: the list of users to search from
    :return: dict
    """
    user = get_user_from_list(user_id, users_list)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


def create_new_user(
    user: CreateUserSchema,
    users_list: list[dict]
) -> User:
    """
    Create a new user

    :param user: The user to create
    :param users_list: The list of users to add the new user to
    :return: The created user
    """
    if not check_email_uniqueness(user.model_dump()["email"], users_list):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")

    user = User(**user.model_dump())

    User.save(user.to_dict(), users_list)

    return user


def update_a_user(
    user_id: int,
    user_update_data: UpdateUserSchema,
    users_list: list[dict]
) -> User:
    """
    Update a user

    :param user_id: The id of the user to update
    :param user_update_data: The data to update the user with
    :param users_list: The list of users to update the user in
    :return: The updated user
    """
    user = get_user_from_list(user_id, users_list)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    user_obj = User.create_instance(**user)

    for key, value in user_update_data.model_dump().items():
        if hasattr(user_obj, key):
            setattr(user_obj, key, value)

    user_obj.updated_at = str(datetime.now(tz=timezone.utc))

    return user_obj

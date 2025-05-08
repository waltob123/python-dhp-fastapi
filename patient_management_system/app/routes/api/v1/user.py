from fastapi import APIRouter, Depends, Request, HTTPException, status

from app.custom_exceptions.custom_http_exception import CustomHTTPException
from app.dummy_data import users
from app.helpers.users import get_users_list, check_email_uniqueness
from app.models.user import User
from app.schemas.users_schema import CreateUserSchema

users_router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    redirect_slashes=True
)


@users_router.get(path="")
def get_all_users(request: Request) -> list[dict]:
    return users


@users_router.get(path="/{user_id}")
def get_user_by_id(request: Request, user_id: int) -> dict:
    for user in users:
        if user["id"] == user_id:
            return user
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    raise CustomHTTPException(status_code=404, message="User not found", success=False)

@users_router.post("")
def create_user(request: Request, user_data: CreateUserSchema, users_list: list = Depends(get_users_list)) -> dict:
    if not check_email_uniqueness(users_list, str(user_data.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    new_user = User(**user_data.model_dump())

    return new_user.to_dict()


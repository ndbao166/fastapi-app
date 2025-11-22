from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from loguru import logger
from rich.pretty import pretty_repr

from app.models.user import CreateUserRequest, UpdateUserRequest, User, UserSearchParams
from app.services.user import UserService
from app.utils import load_example_json

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[User], summary="Api feature search users")
async def get_users(
    user_service: Annotated[UserService, Depends()],
    user_search_params: Annotated[UserSearchParams, Depends()],
) -> list[User]:
    """
    ### Api feature search users
    This api is used to search users.
    ### Query parameters
    - page: int (default: 1)
    - page_size: int (default: 10)
    - sort_by: email, username, created_at, updated_at
    - sort_order: asc, desc (default: desc)
    - email: EmailStr (default: None) - email of the user
    - username: str (default: None) - username of the user
    - created_from: datetime (default: None) - created from of the user
    - created_to: datetime (default: None) - created to of the user
    - search: str (default: None) - search of the user
    - email: find users by email
    - username: find users by username
    - search: find users by email or username
    """
    logger.debug(f"🪲[Debug User Router] User search params: {pretty_repr(user_search_params)}")
    users, _ = await user_service.get_users(params=user_search_params)
    return users


@router.get("/{email_or_user_id}", response_model=User, summary="Api feature get user by email or user id")
async def get_user_by_email_or_user_id(
    email_or_user_id: Annotated[str, Path(description="The email or user id of the user")],
    user_service: Annotated[UserService, Depends()],
) -> User:
    """
    ### Api feature get user by email or user id
    This api is used to get a user by email or user id.
    ### Path parameters
    - email_or_user_id: str - email or user id of the user
    """
    logger.debug(f"🪲[Debug User Router] User email or user id: {email_or_user_id}")
    user = await user_service.get_user(email_or_user_id=email_or_user_id)
    return user


@router.delete("/{email_or_user_id}", response_model=bool, summary="Api feature delete user by email or user id")
async def delete_user(
    email_or_user_id: Annotated[str, Path(description="The email or user id of the user")],
    user_service: Annotated[UserService, Depends()],
) -> bool:
    """
    ### Api feature delete user by email or user id
    This api is used to delete a user by email or user id.
    ### Path parameters
    - email_or_user_id: str - email or user id of the user
    """
    logger.debug(f"🪲[Debug User Router] User email or user id: {email_or_user_id}")
    return await user_service.delete_user(email_or_user_id=email_or_user_id)


@router.post("/", response_model=User)
async def create_user(
    user: Annotated[CreateUserRequest, Body(openapi_examples=load_example_json("data/example/user_example.json"))],
    user_service: Annotated[UserService, Depends()],
) -> User:
    """
    ### Api feature create user
    This api is used to create a new user.
    ### Request body
    - username: str - username of the user
    - email: EmailStr - email of the user
    - password: str - password of the user
    - confirm_password: str - confirm password of the user
    """
    logger.debug(f"🪲[Debug User Router] User create request: {pretty_repr(user)}")
    return await user_service.create_user(user=user)


@router.put("/{email_or_user_id}", response_model=User, summary="Api feature update user by email or user id")
async def update_user(
    email_or_user_id: Annotated[str, Path(description="The email or user id of the user")],
    user: Annotated[UpdateUserRequest, Body(openapi_examples=load_example_json("data/example/user_example.json"))],
    user_service: Annotated[UserService, Depends()],
) -> User:
    """
    ### Api feature update user by email or user id
    This api is used to update a user by email or user id.
    ### Path parameters
    - email_or_user_id: str - email or user id of the user
    ### Request body
    - username: str - username of the user
    """
    logger.debug(f"🪲[Debug User Router] User email or user id: {email_or_user_id}")
    logger.debug(f"🪲[Debug User Router] User update request: {pretty_repr(user)}")
    return await user_service.update_user(email_or_user_id=email_or_user_id, user=user)

from datetime import datetime
from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from strenum import StrEnum


class User(BaseModel):
    id: Annotated[str | None, Field(description="The id of the user")] = None
    username: Annotated[str, Field(min_length=3, max_length=20, description="The username of the user")]
    email: Annotated[EmailStr, Field(description="The email of the user")]

    @model_validator(mode="before")
    @classmethod
    def convert_oid_to_str(cls, values: dict[str, Any]) -> dict[str, Any]:
        if "_id" in values and isinstance(values["_id"], ObjectId):
            values["id"] = str(values["_id"])
        return values


class CreateUserRequest(User):
    password: Annotated[str, Field(min_length=8, max_length=20, description="The password of the user")]
    confirm_password: Annotated[str, Field(min_length=8, max_length=20, description="The confirm password of the user")]


class UpdateUserRequest(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20, description="The username of the user")]


class UserInDB(User):
    hashed_password: Annotated[str, Field(description="The hashed password of the user")]
    created_at: Annotated[datetime, Field(description="The creation date of the user", default_factory=datetime.now)]
    updated_at: Annotated[datetime, Field(description="The last update date of the user", default_factory=datetime.now)]


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class UserSortField(StrEnum):
    EMAIL = "email"
    USERNAME = "username"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class UserSearchParams(BaseModel):
    """search/filter/sort/pagination"""

    # Pagination
    page: Annotated[int, Field(default=1, ge=1, description="Page number")]
    page_size: Annotated[int, Field(default=10, ge=1, le=100, description="Items per page")]

    # Sort
    sort_by: Annotated[UserSortField, Field(default=UserSortField.CREATED_AT)]
    sort_order: Annotated[SortOrder, Field(default=SortOrder.DESC)]

    # Filter
    email: Annotated[EmailStr | None, Field(description="The email of the user")] = None
    username: Annotated[str | None, Field(description="The username of the user")] = None
    created_from: Annotated[datetime | None, Field(description="The creation date from of the user")] = None
    created_to: Annotated[datetime | None, Field(description="The creation date to of the user")] = None
    search: Annotated[str | None, Field(description="The search of the user")] = None

    @field_validator("created_from", "created_to", mode="before")
    @classmethod
    def validate_date_range(cls, value: Any) -> datetime | None:
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

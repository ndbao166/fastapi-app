import re

from bson import ObjectId
from fastapi import HTTPException
from loguru import logger
from pydantic import EmailStr
from pymongo import IndexModel
from rich.pretty import pretty_repr

from app.core.settings import settings
from app.db.mongodb import get_collection
from app.models.user import CreateUserRequest, SortOrder, UpdateUserRequest, User, UserInDB, UserSearchParams
from app.utils import get_password_hash


class UserRepository:
    def __init__(self):
        self.collection = get_collection(settings.MONGO_DATABASE, "users")
        self.email_index = IndexModel("email", unique=True)
        self.username_index = IndexModel("username", unique=True)
        self.created_at_index = IndexModel("created_at")
        self.updated_at_index = IndexModel("updated_at")

    async def build_filter_query(self, params: UserSearchParams) -> dict:
        """Build MongoDB filter query từ search params"""
        query = {}

        # Exact match filters
        if params.email:
            query["email"] = params.email

        if params.username:
            query["username"] = params.username

        # Date range filters
        if params.created_from or params.created_to:
            query["created_at"] = {}
            if params.created_from:
                query["created_at"]["$gte"] = params.created_from
            if params.created_to:
                query["created_at"]["$lte"] = params.created_to

        # Full-text search (search trong email hoặc username)
        if params.search:
            # Escape special regex characters
            escaped_search = re.escape(params.search)
            query["$or"] = [{"email": {"$regex": escaped_search, "$options": "i"}}, {"username": {"$regex": escaped_search, "$options": "i"}}]
        logger.debug(f"🪲[Debug User Repository] Query: {pretty_repr(query)}")
        return query

    async def find_with_pagination(self, params: UserSearchParams) -> tuple[list[dict], int]:
        """
        Tìm users với pagination, filter, sort
        Returns: (list_users, total_count)
        """
        # Build filter query
        filter_query = await self.build_filter_query(params)

        # Build sort
        sort_direction = 1 if params.sort_order == SortOrder.ASC else -1
        sort_query = [(params.sort_by.value, sort_direction)]

        # Calculate skip
        skip = (params.page - 1) * params.page_size

        # Execute queries
        cursor = self.collection.find(filter_query)
        cursor.sort(sort_query)
        cursor.skip(skip)
        cursor.limit(params.page_size)

        users = await cursor.to_list(length=params.page_size)
        total = await self.collection.count_documents(filter_query)

        return users, total


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def get_users(self, params: UserSearchParams) -> tuple[list[User], int]:
        users, total = await self.repository.find_with_pagination(params)
        return [User(**user) for user in users], total

    async def get_user(self, email: EmailStr) -> User:
        user = await self.repository.collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return User(**user)

    async def update_user(self, email: EmailStr, user: UpdateUserRequest) -> User:
        result = await self.repository.collection.update_one(
            {"email": email},
            {
                "$set": user.model_dump(exclude_none=True),
            },
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        user_in_db = await self.repository.collection.find_one({"email": email})
        return User(**user_in_db)

    async def delete_user(self, email: EmailStr) -> bool:
        result = await self.repository.collection.delete_one({"email": email})
        if result.deleted_count <= 0:
            raise HTTPException(status_code=404, detail="User not found")

        return True

    async def create_user(self, user: CreateUserRequest) -> User:
        if user.password != user.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        if await self.repository.collection.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already exists")

        query_result = await self.repository.collection.insert_one(
            UserInDB(
                **user.model_dump(),
                hashed_password=get_password_hash(user.password),
            ).model_dump(exclude_none=True)
        )

        user_in_db = await self.repository.collection.find_one({"_id": ObjectId(query_result.inserted_id)})

        return User(**user_in_db)

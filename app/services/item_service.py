from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection

from app.models.item import Item


class ItemService:
    def __init__(self, col_item: AsyncIOMotorCollection[Any]):
        self.col_item = col_item

    async def create_item(self, item: Item) -> Item:
        await self.col_item.insert_one(item.model_dump())
        return item

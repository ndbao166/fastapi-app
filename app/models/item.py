from pydantic import BaseModel
from strenum import StrEnum


class Category(StrEnum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    OTHER = "other"


class Item(BaseModel):
    name: str
    description: str
    price: float
    category: list[Category]

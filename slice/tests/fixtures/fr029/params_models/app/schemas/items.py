from typing import Optional

from pydantic import BaseModel, Field


class Tag(BaseModel):
    name: str
    color: Optional[str] = None


class ItemCreate(BaseModel):
    name: str
    price: float
    quantity: Optional[int]
    description: str | None = None
    sku: str = Field(alias="stockKeepingUnit")
    main_tag: Tag
    tags: list[Tag] = []


class ItemPublic(BaseModel):
    id: int
    name: str
    tags: list[Tag]


class Item(BaseModel):
    id: int
    name: str
    secret_cost: float

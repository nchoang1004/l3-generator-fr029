from pydantic import BaseModel


class Tag(BaseModel):
    label: str


class ItemIn(BaseModel):
    name: str
    price: float | None = None


class ItemOut(BaseModel):
    id: int
    name: str
    tags: list[Tag]

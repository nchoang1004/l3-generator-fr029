from pydantic import BaseModel


class OrderIn(BaseModel):
    product: str
    quantity: int


class OrderOut(BaseModel):
    id: int
    product: str
    quantity: int

from pydantic import BaseModel


class Item(BaseModel):
    code: str
    active: bool = True

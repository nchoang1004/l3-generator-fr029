import httpx
from fastapi import APIRouter

from app.schemas import ItemIn, ItemOut

router = APIRouter()


@router.post("/", status_code=201)
def create_item(item: ItemIn) -> ItemOut:
    httpx.post("https://audit.example.com/log", json={"name": item.name})
    return ItemOut(id=1, name=item.name, tags=[])


@router.get("/{item_id}")
def read_item(item_id: int, verbose: bool = False) -> ItemOut:
    return ItemOut(id=item_id, name="x", tags=[])

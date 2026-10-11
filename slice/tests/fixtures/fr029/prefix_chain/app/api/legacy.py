from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.get("/items/{item_id}")
def legacy_get_item(item_id: int):
    return {"id": item_id, "legacy": True}

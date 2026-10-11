from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
def list_items():
    return []


@router.get("/{item_id}")
def get_item(item_id: int):
    return {"id": item_id}


@router.api_route("/{item_id}/sync", methods=["GET", "POST"])
def sync_item(item_id: int):
    return {"id": item_id, "synced": True}

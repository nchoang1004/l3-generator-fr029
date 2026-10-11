from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, Form, Header, Query, UploadFile, status
from fastapi.responses import RedirectResponse

from app.deps import search_filter, tenant
from app.schemas.items import Item, ItemCreate, ItemPublic, Tag
from app.schemas.legacy import Item as LegacyItem

router = APIRouter()


@router.get("/items", response_model=list[ItemPublic])
def list_items(filters: Annotated[dict, Depends(search_filter)]):
    return []


@router.get("/items/{item_id}", response_model=ItemPublic)
def get_item(
    item_id: int,
    verbose: Annotated[int, Query()],
    x_token: Annotated[str | None, Header()] = None,
) -> Item:
    return Item(id=item_id, name="x", secret_cost=1.0)


@router.get("/items/{item_id}/full")
def get_item_full(item_id: int) -> Item:
    return Item(id=item_id, name="x", secret_cost=1.0)


@router.post("/items", response_model=ItemPublic, status_code=201)
def create_item(item: ItemCreate, tenant_id: Annotated[str, Depends(tenant)]):
    return ItemPublic(id=1, name=item.name, tags=item.tags)


@router.put("/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, item: ItemCreate, tag: Tag):
    return ItemPublic(id=item_id, name=item.name, tags=[tag])


@router.patch("/items/{item_id}/tag")
def set_main_tag(item_id: int, tag: Annotated[Tag, Body(embed=True)]):
    return {"id": item_id, "tag": tag.name}


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return None


@router.post("/uploads")
def upload(title: Annotated[str, Form()], file: Annotated[UploadFile, File()]):
    return {"title": title, "filename": file.filename}


@router.post("/login")
def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"user": username}


@router.get("/legacy/items/{code}", response_model=LegacyItem)
def legacy_item(code: str):
    return LegacyItem(code=code)


@router.get("/go", response_class=RedirectResponse)
def go():
    return "/items"

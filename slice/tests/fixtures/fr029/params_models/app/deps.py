from typing import Annotated

from fastapi import Depends, Header, Query


def pagination(skip: int = 0, limit: Annotated[int, Query(le=100)] = 10):
    return {"skip": skip, "limit": limit}


def search_filter(
    q: str | None = None,
    page: Annotated[dict, Depends(pagination)] = None,
):
    return {"q": q, "page": page}


def tenant(x_tenant_id: Annotated[str, Header()]):
    return x_tenant_id

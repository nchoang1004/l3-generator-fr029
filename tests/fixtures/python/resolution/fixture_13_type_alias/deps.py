from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from repo import OrderRepository


def get_repo() -> OrderRepository:
    return OrderRepository()


def get_session() -> Session:
    return Session()


RepoDep = Annotated[OrderRepository, Depends(get_repo)]
SessionDep = Annotated[Session, Depends(get_session)]

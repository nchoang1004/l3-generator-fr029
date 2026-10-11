from fastapi import APIRouter, Depends
from sqlalchemy import func, select

from app.db import get_db
from app.models import Order

router = APIRouter(prefix="/reports")


@router.get("/daily")
def daily_report(db=Depends(get_db)):
    total = db.scalar(select(func.count(Order.id)))
    return {"orders": total}

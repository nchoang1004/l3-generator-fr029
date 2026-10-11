from app import repository
from app.config import settings


def place_order(db, product: str, quantity: int):
    capped = min(quantity, settings.MAX_ORDER_QUANTITY)
    return repository.save_order(db, product, capped)


def get_order(db, order_id: int):
    return repository.find_order(db, order_id)

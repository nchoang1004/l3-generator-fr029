import os

from service import OrderService


def handle(payload):
    svc = OrderService()
    os.getenv("REGION")
    return svc.create(payload)

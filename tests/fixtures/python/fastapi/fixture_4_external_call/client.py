import httpx
import requests

import settings


def charge(order_id: int):
    requests.get("https://api.payment.com/charge")
    httpx.post(f"{settings.PAYMENT_URL}/charge", json={"id": order_id})


def notify():
    client = httpx.Client()
    client.put("https://hooks.internal/notify")


def flexible(method: str):
    requests.request(method, "https://api.payment.com/any")

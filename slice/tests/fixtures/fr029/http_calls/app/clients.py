import urllib.request

import aiohttp
import httpx
import httpx as hx
import requests

from app.config import settings
from app.inventory_client import InventoryClient


def fetch_rates():
    return httpx.get("https://rates.example.com/v1/latest")


def notify_shipping(order_id: int):
    with httpx.Client() as c:
        c.post("https://ship.example.com/orders", json={"id": order_id})


async def reserve_stock(sku: str):
    async with InventoryClient() as client:
        return await client.put(settings.INVENTORY_URL, json={"sku": sku})


def patch_profile(user_id: int):
    with httpx.Client() as client:
        return client.request("PATCH", "https://users.example.com/profile", json={"id": user_id})


def call_dynamic(method: str, url: str):
    with httpx.Client() as client:
        return client.request(method, url)


def download_report():
    with httpx.stream("GET", "https://reports.example.com/daily.csv") as response:
        return b"".join(response.iter_bytes())


def audit_ping():
    return requests.Session().get("https://audit.example.com/ping")


def charge(amount: int):
    return requests.post(settings.PAYMENT_URL, json={"amount": amount})


async def fetch_weather():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://weather.example.com/today") as resp:
            return await resp.json()


def fetch_user(base: str, user_id: int):
    return httpx.get(f"{base}/users/{user_id}")


def purge_cache():
    return hx.delete("https://cache.example.com/purge")


def read_legacy_feed():
    with urllib.request.urlopen("https://legacy.example.com/feed") as resp:
        return resp.read()

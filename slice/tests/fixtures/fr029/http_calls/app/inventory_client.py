import httpx


class InventoryClient(httpx.AsyncClient):
    def __init__(self):
        super().__init__(timeout=5.0)

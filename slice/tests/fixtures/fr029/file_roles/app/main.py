from fastapi import FastAPI

from app.api import orders, reports

app = FastAPI(title="File roles")
app.include_router(orders.router)
app.include_router(reports.router)

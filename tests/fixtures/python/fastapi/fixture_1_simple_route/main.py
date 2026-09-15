from fastapi import FastAPI

app = FastAPI()


@app.get("/orders")
def list_orders():
    return []


@app.post("/orders")
def create_order():
    return {}

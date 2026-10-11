from fastapi import FastAPI

from db.models import load_items

app = FastAPI()


@app.get("/items", status_code=200)
def list_items():
    return load_items()

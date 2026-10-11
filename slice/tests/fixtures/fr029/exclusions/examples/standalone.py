from fastapi import FastAPI

demo = FastAPI(title="Standalone example")


@demo.get("/example")
def example():
    return {"example": True}

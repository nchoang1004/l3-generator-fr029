from fastapi import FastAPI

app = FastAPI()


@app.get("/only-in-test")
def only_in_test():
    return {}

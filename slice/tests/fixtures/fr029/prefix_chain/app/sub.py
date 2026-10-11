from fastapi import FastAPI

sub_app = FastAPI(title="Sub app")


@sub_app.get("/hello")
def sub_hello():
    return {"hello": "sub"}

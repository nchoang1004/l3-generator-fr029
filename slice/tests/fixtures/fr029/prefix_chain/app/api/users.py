from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.get("/me")
def read_me():
    return {"name": "me"}

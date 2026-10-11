from fastapi import APIRouter

router = APIRouter(prefix="/status")


@router.get("/ping")
def ping():
    return {"pong": True}

from fastapi import APIRouter

router = APIRouter()


@router.get("/selfcheck")
def selfcheck():
    return {"ok": True}

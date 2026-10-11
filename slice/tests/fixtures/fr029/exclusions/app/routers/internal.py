from fastapi import APIRouter

router = APIRouter()


@router.get("/debug/state")
def debug_state():
    return {"state": "ok"}

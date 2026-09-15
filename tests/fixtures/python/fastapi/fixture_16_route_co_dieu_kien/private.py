from fastapi import APIRouter

router = APIRouter(prefix="/private")


@router.post("/reset")
def reset():
    return "done"

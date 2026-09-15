from fastapi import APIRouter

router = APIRouter(prefix="/public")


@router.get("/health")
def health():
    return "ok"

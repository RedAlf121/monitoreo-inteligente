from fastapi import APIRouter

router = APIRouter()

@router.post("/items/{item_id}")
def create_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
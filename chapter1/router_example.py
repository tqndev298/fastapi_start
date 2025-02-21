from fastapi import APIRouter

router = APIRouter()


@router.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

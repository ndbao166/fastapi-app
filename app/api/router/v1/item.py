from fastapi import APIRouter, Depends, HTTPException

from app.dependency import get_token_header

router = APIRouter(
    prefix="/v1/items",
    tags=["items-v1"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items() -> dict[str, dict[str, str]]:
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str) -> dict[str, str]:
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str) -> dict[str, str]:
    if item_id != "plumbus":
        raise HTTPException(status_code=403, detail="You can only update the item: plumbus")
    return {"item_id": item_id, "name": "The great Plumbus"}

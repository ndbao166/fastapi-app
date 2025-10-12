from fastapi import APIRouter, Depends

from app.dependency import get_token_header

router = APIRouter(
    prefix="/v1/users",
    tags=["users-v1"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users() -> list[dict[str, str]]:
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me")
async def read_user_me() -> dict[str, str]:
    return {"username": "fakecurrentuser"}


@router.get("/{username}")
async def read_user_v1(username: str) -> dict[str, str]:
    return {"username": username}

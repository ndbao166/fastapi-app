from fastapi import APIRouter

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users() -> list[dict[str, str]]:
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/")
async def create_user(username: str) -> dict[str, str]:
    return {"username": username}


@router.get("/me")
async def read_user_me() -> dict[str, str]:
    return {"username": "baond"}


@router.get("/{username}")
async def read_user_v1(username: str) -> dict[str, str]:
    return {"username": username}


@router.put("/{username}")
async def update_user(username: str) -> dict[str, str]:
    return {"username": username}


@router.delete("/{username}")
async def delete_user(username: str) -> dict[str, str]:
    return {"username": username}

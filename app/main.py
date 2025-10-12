from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from loguru import logger

from app.api import item_router_v1, item_router_v2, user_router_v1, user_router_v2
from app.core.settings import settings
from app.dependency import get_query_token


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    from app.settings import clean_app, setup_app

    await setup_app()
    logger.info(f"🚀 App has been started: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"🚀 OpenAPI docs: http://{settings.HOST}:{settings.PORT}/docs")
    yield
    clean_app()


app = FastAPI(
    title="Learn FastAPI",
    description="### Learn FastAPI",
    version="0.1.0",
    lifespan=lifespan,
    dependencies=[Depends(get_query_token)],
)


app.include_router(item_router_v1)
app.include_router(user_router_v1)
app.include_router(item_router_v2)
app.include_router(user_router_v2)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

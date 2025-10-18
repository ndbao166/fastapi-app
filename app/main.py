from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api import user_router_v1
from app.core.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    from loguru import logger

    from app.setup import clean_app, setup_app

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
    dependencies=[],
)


app.include_router(user_router_v1)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

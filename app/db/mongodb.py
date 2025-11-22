from typing import Any

from loguru import logger
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)


class _Setting:
    client: AsyncIOMotorClient[Any]


async def setup_mongodb(host: str, port: int, username: str | None, password: str | None, database_name: str) -> None:
    _Setting.client = AsyncIOMotorClient(
        host=host,
        port=port,
        username=username,
        password=password,
        directConnection=True,
    )
    try:
        await _Setting.client.admin.command("ping")
        logger.info("✅ MongoDB client has been connected.")
        await get_db(database_name)
        logger.info(f"✅ MongoDB database {database_name} has been connected.")
    except Exception as e:
        logger.exception(f"🆘 Error connecting to MongoDB: {e}")
        raise


def close_mongodb() -> None:
    _Setting.client.close()
    logger.info("✅ MongoDB client has been closed.")


async def get_db(db_name: str) -> AsyncIOMotorDatabase[Any]:
    if not _Setting.client:
        raise Exception("MongoDB client has not been setup.")

    dbs = await _Setting.client.list_database_names()
    if db_name not in dbs:
        raise Exception(f"Database '{db_name}' does not exist.")

    return _Setting.client[db_name]


def get_collection(db_name: str, collection_name: str) -> AsyncIOMotorCollection[Any]:
    return _Setting.client[db_name][collection_name]

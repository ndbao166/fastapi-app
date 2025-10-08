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


async def is_mongodb_connected() -> bool:
    return _Setting.client is not None


async def get_db(db_name: str) -> AsyncIOMotorDatabase[Any]:
    if not _Setting.client:
        raise Exception("MongoDB client has not been setup.")

    dbs = await _Setting.client.list_database_names()
    if db_name not in dbs:
        raise Exception(f"Database '{db_name}' does not exist.")

    return _Setting.client[db_name]


async def get_collection(db_name: str, collection_name: str) -> AsyncIOMotorCollection[Any]:
    db = await get_db(db_name)

    cols = await db.list_collection_names()
    if collection_name not in cols:
        raise Exception(f"Collection '{collection_name}' does not exist in database '{db_name}'.")

    return db[collection_name]

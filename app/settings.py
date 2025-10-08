from app.core.logging import Logger
from app.core.settings import settings
from app.db.mongodb import close_mongodb, setup_mongodb


async def setup_app() -> None:

    # 1. Logger
    Logger.setup(settings.LOG_FOLDER_PATH, settings.LOG_FOLDER_BACKUP_PATH)

    # 2. MongoDB
    await setup_mongodb(
        settings.MONGO_HOST,
        settings.MONGO_PORT,
        settings.MONGO_USER,
        settings.MONGO_PASSWORD,
        settings.MONGO_DATABASE,
    )

    # 3. App config
    from app.core.config import app_config
    _ = app_config


def clean_app() -> None:
    close_mongodb()


__all__ = ["setup_app", "clean_app"]

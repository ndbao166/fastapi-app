from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    LOG_FOLDER_PATH: str
    LOG_FOLDER_BACKUP_PATH: str
    CONFIG_PATH: str

    PORT: int
    HOST: str

    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DATABASE: str

    class Config:
        env_file = ".env"


settings = Settings()

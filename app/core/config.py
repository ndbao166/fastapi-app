from functools import lru_cache

from loguru import logger
from pydantic import BaseModel
from rich.pretty import pretty_repr

from app.core.settings import settings


class GoogleConfig(BaseModel):
    model_name: str
    base_url: str


class OpenAIConfig(BaseModel):
    model_name: str
    base_url: str


class AnthropicConfig(BaseModel):
    model_name: str
    base_url: str


class LLMConfig(BaseModel):
    google: GoogleConfig
    openai: OpenAIConfig
    anthropic: AnthropicConfig


class AppConfig(BaseModel):
    llm: LLMConfig

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "AppConfig":
        import yaml
        try:
            with open(yaml_path, encoding="utf-8") as file:
                yaml_data = yaml.safe_load(file)
                logger.info(f"✅ Config from {yaml_path} loaded successfully: \n{pretty_repr(yaml_data)}")
                return cls(**yaml_data)
        except Exception as e:
            logger.exception(f"🆘 Error loading app config from {yaml_path}: {e}")
            raise


@lru_cache
def get_app_config() -> AppConfig:
    return AppConfig.from_yaml(settings.CONFIG_PATH)


app_config = get_app_config()

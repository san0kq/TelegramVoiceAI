from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', override=True)


class Settings(BaseSettings):
    app_host: str
    app_port: int
    tg_token: str
    webhook_url: str
    openai_api_key: str
    assistant_id: str
    redis_password: str
    redis_user: str = 'default'
    redis_host: str
    redis_port: str
    redis_external_port: str = '6379'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


def get_settings() -> Settings:
    return Settings()


settings = get_settings()

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
    value_identifier_assistant_id: str
    redis_password: str
    redis_user: str = 'default'
    redis_host: str
    redis_port: str
    redis_external_port: str = '6379'
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: str
    postgres_external_port: str
    amplitude_api_key: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


def get_settings() -> Settings:
    return Settings()


settings = get_settings()

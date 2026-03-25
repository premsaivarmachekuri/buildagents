from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "my-base-app"
    debug: bool = False
    openai_api_key: str = ""
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
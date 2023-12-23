from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Security
    API_KEY: str = "default-api-key"
    EXCHANGE: str = "binance"  # binance as default

    class Config:
        env_file = ".env"


settings = Settings()
from pydantic import AmqpDsn, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Security
    API_KEY: str = "default-api-key"
    EXCHANGE: str = "binance"  # binance as default

    PIKA_URL: AmqpDsn = Field("amqp://cryptostream:bullionbear@localhost:5672/")
    PIKA_EXCHANGE: str = "market"

    class Config:
        env_file = ".env"


settings = Settings()
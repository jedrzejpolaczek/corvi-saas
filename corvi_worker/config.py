from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field("postgresql+psycopg2://corvi:corvi@postgres:5432/corvi", env="DATABASE_URL")
    QUEUE_BACKEND: str = Field("rabbitmq", env="QUEUE_BACKEND")
    RABBITMQ_URL: str = Field("amqp://guest:guest@rabbitmq:5672/", env="RABBITMQ_URL")
    REDIS_URL: str = Field("redis://redis:6379/0", env="REDIS_URL")

settings = Settings()

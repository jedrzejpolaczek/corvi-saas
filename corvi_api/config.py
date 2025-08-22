from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    ENV: str = Field("dev", env="ENV")
    API_ROOT_PATH: str = ""
    DATABASE_URL: str = Field("postgresql+psycopg2://corvi:corvi@postgres:5432/corvi", env="DATABASE_URL")
    JWT_SECRET: str = Field("devsecret", env="JWT_SECRET")
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60*24*7
    SESSION_SECRET: str = Field("sessionsecret", env="SESSION_SECRET")
    CORS_ORIGINS: List[str] = ["*"]

    # S3/MinIO
    S3_ENDPOINT_URL: str = Field("http://minio:9000", env="S3_ENDPOINT_URL")
    S3_ACCESS_KEY: str = Field("minio", env="S3_ACCESS_KEY")
    S3_SECRET_KEY: str = Field("minio123", env="S3_SECRET_KEY")
    S3_BUCKET: str = Field("corvi", env="S3_BUCKET")
    S3_SECURE: bool = False

    # Queue
    QUEUE_BACKEND: str = Field("rabbitmq", env="QUEUE_BACKEND")
    RABBITMQ_URL: str = Field("amqp://guest:guest@rabbitmq:5672//", env="RABBITMQ_URL")
    REDIS_URL: str = Field("redis://redis:6379/0", env="REDIS_URL")

    # MLflow
    MLFLOW_TRACKING_URI: str = Field("http://mlflow:5000", env="MLFLOW_TRACKING_URI")

    # Enterprise
    ENTERPRISE_MODE: bool = Field(False, env="ENTERPRISE_MODE")

    # Rate limiting
    RATE_LIMIT_PER_MIN: int = 120

    class Config:
        case_sensitive = False
        env_file = ".env"

settings = Settings()

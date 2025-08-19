from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Core infra
    DATABASE_URL: str = Field("sqlite:///./corvi.db")
    REDIS_URL: str = Field("redis://localhost:6379/0")
    # Auth
    JWT_SECRET: str = Field("change-me-in-prod")
    JWT_ALGORITHM: str = Field("HS256")
    JWT_EXPIRES_MIN: int = Field(60 * 24)  # 24h

    # S3/MinIO
    S3_ENDPOINT_URL: str | None = None
    S3_REGION: str | None = None
    S3_ACCESS_KEY: str | None = None
    S3_SECRET_KEY: str | None = None
    S3_BUCKET: str = "corvi-datasets"

    # Upload
    UPLOAD_MAX_MB: int = 100

    # HPO Heuristics (MVP)
    PRUNING_LAST_K: int = 5
    PRUNING_MIN_DELTA: float = 0.005
    CLASSIFICATION_MIN_USEFUL: float = 0.60
    REGRESSION_MIN_USEFUL: float = 0.30

    # Testing toggles
    CELERY_TASK_ALWAYS_EAGER: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

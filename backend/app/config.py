from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@postgres:5432/clipgen"
    redis_url: str = "redis://redis:6379/0"
    storage_path: str = "/data/storage"

    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-5-20250929"

    highlight_clip_count: int = 4
    highlight_clip_seconds: int = 45
    whisper_model_size: str = "base"

    class Config:
        env_file = ".env"


settings = Settings()

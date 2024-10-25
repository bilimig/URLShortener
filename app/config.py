from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db/url_shortener"
    REDIS_URL: str = "redis://localhost:6379/0"
    BROKER_URL: str = "redis://redis:6379/0"
    BACKEND_URL: str = "redis://redis:6379/0"

settings = Settings()
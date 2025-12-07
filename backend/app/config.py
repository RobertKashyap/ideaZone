"""Application configuration."""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings loaded from environment variables."""
    
    app_name: str = "Idea Tracker API"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./idea_tracker.db"
    
    # API Keys (placeholders - to be set via env)
    gemini_api_key: str = ""
    google_search_api_key: str = ""
    google_search_cx: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

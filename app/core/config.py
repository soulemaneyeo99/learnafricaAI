from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "LearnAfrica AI API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "changethis-generate-a-secure-random-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Gemini API Key (User provided)
    GEMINI_API_KEY: str
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

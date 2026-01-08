from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings"""
    
    # App configuration
    APP_NAME: str = "Excel Translation Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Translation API"
    VERSION: str = "1.0.0"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".xlsx", ".xls"]
    UPLOAD_DIR: str = "uploads"
    
    # Translation API settings
    TRANSLATION_API_KEY: str = ""  # Set in .env file for real API
    TRANSLATION_API_URL: str = "https://translation.googleapis.com/language/translate/v2"
    USE_MOCK_TRANSLATION: bool = True  # Set to False when using real API
    
    # Supported languages
    SUPPORTED_LANGUAGES: List[str] = ["en", "ko", "ja", "zh", "es", "fr", "de"]
    DEFAULT_SOURCE_LANG: str = "ko"
    DEFAULT_TARGET_LANG: str = "en"
    
    # Rate limiting
    MAX_BATCH_SIZE: int = 100  # Max texts to translate in one batch
    REQUEST_TIMEOUT: int = 30  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

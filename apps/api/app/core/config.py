"""Application configuration"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_TITLE: str = "SkyLaneAI API"
    API_VERSION: str = "2.0.0"
    API_DESCRIPTION: str = "Sky Hazard Detection API for Flying Taxis"

    # CORS Settings
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]

    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".mp4", ".avi"}

    # Model Settings
    MODEL_PATH: str = "yolo11n.pt"  # Will be downloaded automatically
    CONFIDENCE_THRESHOLD: float = 0.25
    IOU_THRESHOLD: float = 0.45

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()

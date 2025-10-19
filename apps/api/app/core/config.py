"""Application configuration"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_TITLE: str = "SkyLaneAI API"
    API_VERSION: str = "2.0.0"
    API_DESCRIPTION: str = "Sky Hazard Detection API for Flying Taxis"

    # CORS Settings
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001", "https://00ddcee62d4f.ngrok-free.app"]

    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".mp4", ".avi"}

    # Model Settings
    MODELS_DIR: str = "models"  # Directory to store model files
    MODEL_NAME: str = "yolo11n.pt"  # Model filename
    MODEL_CACHE_ENABLED: bool = True  # Cache models to avoid re-downloading
    MODEL_DEVICE: str = "cpu"  # Device to run model on: "cpu", "cuda", or "cuda:0"
    CONFIDENCE_THRESHOLD: float = 0.25
    IOU_THRESHOLD: float = 0.45

    # Video Streaming Settings
    DEFAULT_PROCESS_FPS: int = 10  # Process 10 frames per second
    MAX_FRAME_QUEUE_SIZE: int = 30  # Maximum frames in processing queue
    ENABLE_FRAME_SKIPPING: bool = True  # Skip frames if processing is slow

    # Video Upload Settings
    VIDEO_UPLOAD_DIR: str = "temp/uploads"  # Directory for uploaded videos
    VIDEO_MAX_SIZE_MB: int = 100  # Maximum video file size in MB
    VIDEO_ALLOWED_FORMATS: list[str] = [".mp4", ".avi", ".mov", ".mkv"]  # Allowed video formats
    VIDEO_CLEANUP_HOURS: int = 24  # Auto-delete videos after N hours

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()

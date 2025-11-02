"""Application configuration"""
import json
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_TITLE: str = "SkyLaneAI API"
    API_VERSION: str = "2.0.0"
    API_DESCRIPTION: str = "Sky Hazard Detection API for Flying Taxis"

    # CORS Settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://sky-lane-ai-web.vercel.app"
    ]

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from JSON string or return list as-is"""
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                return parsed if isinstance(parsed, list) else [parsed]
            except json.JSONDecodeError:
                # If it's a comma-separated string
                return [origin.strip() for origin in v.split(',')]
        return v

    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".mp4", ".avi"}

    # Model Settings
    MODELS_DIR: str = "models"  # Directory to store model files
    MODEL_NAME: str = "yolo11l.pt"  # Model filename (large model for better accuracy)
    MODEL_CACHE_ENABLED: bool = True  # Cache models to avoid re-downloading
    MODEL_DEVICE: str = "cpu"  # Device to run model on: "cpu", "cuda", or "cuda:0"
    CONFIDENCE_THRESHOLD: float = 0.25
    IOU_THRESHOLD: float = 0.45

    # Sky Hazard Detection Settings
    # Only detect these classes (sky hazards). Set to empty list to detect all classes.
    # COCO classes that might appear in sky: bird, kite, airplane (aircraft)
    # Note: COCO doesn't have "drone" or "balloon" as separate classes, but:
    # - Drones may be detected as "airplane" or "kite"
    # - Balloons may be detected as "kite" or "sports ball"
    SKY_HAZARD_CLASSES: list[str] = [
        "bird",
        "kite",
        "airplane",
        "sports ball"  # May detect balloons
    ]

    # Video Streaming Settings
    DEFAULT_PROCESS_FPS: int = 10  # Process 10 frames per second
    MAX_FRAME_QUEUE_SIZE: int = 30  # Maximum frames in processing queue
    ENABLE_FRAME_SKIPPING: bool = True  # Skip frames if processing is slow

    # Video Upload Settings
    VIDEO_UPLOAD_DIR: str = "temp/uploads"  # Directory for uploaded videos
    VIDEO_MAX_SIZE_MB: int = 100  # Maximum video file size in MB
    VIDEO_ALLOWED_FORMATS: list[str] = [".mp4", ".avi", ".mov", ".mkv"]  # Allowed video formats
    VIDEO_CLEANUP_HOURS: int = 24  # Auto-delete videos after N hours

    # OpenAI API Settings
    OPENAI_API_KEY: str = ""  # OpenAI API key for advanced features
    OPENAI_MODEL: str = "gpt-5-nano"  # Model for alert generation
    ALERT_GENERATION_TIMEOUT: int = 5  # Timeout in seconds

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()

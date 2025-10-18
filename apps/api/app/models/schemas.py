"""Pydantic schemas for API requests and responses"""
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str
    message: str


class DetectionBox(BaseModel):
    """Bounding box for detected object"""
    x1: float = Field(..., description="Top-left x coordinate")
    y1: float = Field(..., description="Top-left y coordinate")
    x2: float = Field(..., description="Bottom-right x coordinate")
    y2: float = Field(..., description="Bottom-right y coordinate")


class Detection(BaseModel):
    """Detected object information"""
    class_name: str = Field(..., description="Name of detected class")
    class_id: int = Field(..., description="Class ID")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    bbox: DetectionBox = Field(..., description="Bounding box coordinates")


class ImageDetectionResponse(BaseModel):
    """Response from image detection endpoint"""
    success: bool
    detections: list[Detection]
    detection_count: int
    processing_time_ms: float
    image_size: tuple[int, int]

"""Pydantic schemas for API requests and responses"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


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
    frame_number: Optional[int] = Field(None, description="Frame number in video")
    timestamp: Optional[float] = Field(None, description="Timestamp in seconds")


class ImageDetectionResponse(BaseModel):
    """Response from image detection endpoint"""
    success: bool
    detections: list[Detection]
    detection_count: int
    processing_time_ms: float
    image_size: tuple[int, int]


# Natural Language Alert Models

class EnrichedContext(BaseModel):
    """Enriched context from detection analysis"""
    estimated_size: str = Field(..., description="Size category: small, medium, large")
    bbox_area_pixels: int = Field(..., description="Bounding box area in pixels")
    screen_position: str = Field(..., description="Position on screen (e.g., upper-left, center)")
    threat_level_raw: str = Field(..., description="Initial threat assessment")


class CraftedMessage(BaseModel):
    """Human-readable alert message"""
    title: str = Field(..., description="Alert title")
    emoji: str = Field(..., description="Alert emoji")
    body: str = Field(..., description="Full message body in markdown")
    sections: dict = Field(default_factory=dict, description="Parsed message sections")


class ActionRecommendation(BaseModel):
    """Recommended actions for pilot"""
    immediate_actions: list[str] = Field(default_factory=list, description="Actions to take immediately")
    monitoring_actions: list[str] = Field(default_factory=list, description="What to monitor")
    contingency_actions: list[str] = Field(default_factory=list, description="Actions if situation worsens")


class PriorityScore(BaseModel):
    """Priority level and scoring"""
    level: str = Field(..., description="Priority level: green, yellow, orange, red")
    score: int = Field(..., ge=1, le=10, description="Numeric priority score 1-10")
    reasoning: str = Field(..., description="Justification for priority level")


class NaturalLanguageAlert(BaseModel):
    """Complete natural language alert"""
    alert_id: str = Field(..., description="Unique alert identifier")
    detection: Detection = Field(..., description="Original detection data")
    context: EnrichedContext = Field(..., description="Enriched context")
    message: CraftedMessage = Field(..., description="Crafted message")
    actions: ActionRecommendation = Field(..., description="Recommended actions")
    priority: PriorityScore = Field(..., description="Priority assessment")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Alert generation timestamp")

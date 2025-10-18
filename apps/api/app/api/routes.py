"""API routes"""
from fastapi import APIRouter
from app.core.config import settings
from app.models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        message="SkyLaneAI API is running"
    )

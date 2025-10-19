"""FastAPI main application"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router
from app.api.stream_routes import router as stream_router
from app.api.video_routes import router as video_router, _recover_uploaded_videos


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print(f"🚀 {settings.API_TITLE} v{settings.API_VERSION} starting...")
    print(f"📚 API Documentation: http://localhost:8000/docs")

    # Recover uploaded videos from disk
    print("🔄 Recovering uploaded videos...")
    await _recover_uploaded_videos()
    print("✅ Video recovery complete")

    yield

    # Shutdown
    print("👋 Shutting down SkyLaneAI API...")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["api"])
app.include_router(stream_router, prefix="/api/v1/stream", tags=["stream"])
app.include_router(video_router, prefix="/api/v1/video", tags=["video"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SkyLaneAI API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }

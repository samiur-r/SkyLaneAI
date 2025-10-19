"""Video upload and management routes"""
import os
import uuid
import logging
from pathlib import Path
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import json
from app.services.video_file_processor import VideoFileProcessor
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Store active video processors (in production, use Redis or similar)
active_processors: Dict[str, VideoFileProcessor] = {}

# Store uploaded video metadata
uploaded_videos: Dict[str, Dict[str, Any]] = {}


def _get_upload_dir() -> Path:
    """Get or create upload directory"""
    upload_dir = Path(settings.VIDEO_UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def _validate_video_file(filename: str) -> bool:
    """Validate video file extension"""
    ext = Path(filename).suffix.lower()
    return ext in settings.VIDEO_ALLOWED_FORMATS


def _get_file_size_mb(file_path: Path) -> float:
    """Get file size in MB"""
    return file_path.stat().st_size / (1024 * 1024)


@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a video file for processing

    Args:
        file: Video file (multipart/form-data)

    Returns:
        Video ID and metadata
    """
    try:
        # Validate file type
        if not _validate_video_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Allowed: {settings.VIDEO_ALLOWED_FORMATS}"
            )

        # Generate unique video ID
        video_id = str(uuid.uuid4())

        # Get upload directory
        upload_dir = _get_upload_dir()

        # Save file with original extension
        file_ext = Path(file.filename).suffix
        file_path = upload_dir / f"{video_id}{file_ext}"

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(f"Video uploaded: {file_path}")

        # Check file size
        file_size_mb = _get_file_size_mb(file_path)
        if file_size_mb > settings.VIDEO_MAX_SIZE_MB:
            file_path.unlink()  # Delete file
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.VIDEO_MAX_SIZE_MB}MB"
            )

        # Initialize video processor to extract metadata
        processor = VideoFileProcessor(str(file_path))
        try:
            metadata = await processor.initialize()
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            file_path.unlink()  # Delete file
            raise HTTPException(
                status_code=400,
                detail=f"Invalid video file: {str(e)}"
            )
        finally:
            await processor.close()

        # Store metadata
        video_data = {
            "video_id": video_id,
            "filename": file.filename,
            "file_path": str(file_path),
            "size_mb": file_size_mb,
            "metadata": metadata,
            "uploaded_at": None  # Will be set by proper datetime
        }

        uploaded_videos[video_id] = video_data

        logger.info(f"Video metadata extracted: {video_id}")

        return {
            "video_id": video_id,
            "filename": file.filename,
            "duration": metadata["duration"],
            "fps": metadata["fps"],
            "total_frames": metadata["total_frames"],
            "width": metadata["width"],
            "height": metadata["height"],
            "size_mb": round(file_size_mb, 2),
            "codec": metadata["codec"]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading video: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{video_id}/metadata")
async def get_video_metadata(video_id: str):
    """
    Get metadata for uploaded video

    Args:
        video_id: Video ID

    Returns:
        Video metadata
    """
    if video_id not in uploaded_videos:
        raise HTTPException(status_code=404, detail="Video not found")

    video_data = uploaded_videos[video_id]
    metadata = video_data["metadata"]

    return {
        "video_id": video_id,
        "filename": video_data["filename"],
        "duration": metadata["duration"],
        "fps": metadata["fps"],
        "total_frames": metadata["total_frames"],
        "width": metadata["width"],
        "height": metadata["height"],
        "size_mb": video_data["size_mb"],
        "codec": metadata["codec"]
    }


@router.delete("/{video_id}")
async def delete_video(video_id: str):
    """
    Delete uploaded video

    Args:
        video_id: Video ID

    Returns:
        Success message
    """
    if video_id not in uploaded_videos:
        raise HTTPException(status_code=404, detail="Video not found")

    video_data = uploaded_videos[video_id]
    file_path = Path(video_data["file_path"])

    # Stop processor if active
    if video_id in active_processors:
        processor = active_processors[video_id]
        await processor.close()
        del active_processors[video_id]

    # Delete file
    if file_path.exists():
        file_path.unlink()
        logger.info(f"Deleted video file: {file_path}")

    # Remove from metadata
    del uploaded_videos[video_id]

    return {"message": "Video deleted successfully", "video_id": video_id}


@router.websocket("/ws/{video_id}")
async def video_websocket_endpoint(websocket: WebSocket, video_id: str):
    """
    WebSocket endpoint for video processing with detections

    Args:
        websocket: WebSocket connection
        video_id: Video ID to process
    """
    await websocket.accept()
    logger.info(f"Video WebSocket connection accepted: {video_id}")

    # Check if video exists
    if video_id not in uploaded_videos:
        await websocket.send_json({
            "type": "error",
            "message": "Video not found"
        })
        await websocket.close()
        return

    video_data = uploaded_videos[video_id]
    file_path = video_data["file_path"]

    # Create video processor
    processor = VideoFileProcessor(file_path, process_fps=10)

    try:
        # Initialize processor
        await processor.initialize()

        # Set up callbacks
        async def send_detection_result(result: dict):
            """Send detection results to client via WebSocket"""
            try:
                await websocket.send_json({
                    "type": "detection",
                    "data": result
                })
            except Exception as e:
                logger.error(f"Error sending detection: {e}")

        async def send_progress_update(progress: dict):
            """Send progress updates to client"""
            try:
                await websocket.send_json({
                    "type": "progress",
                    "data": progress
                })
            except Exception as e:
                logger.error(f"Error sending progress: {e}")

        async def send_completed():
            """Send completion message"""
            try:
                await websocket.send_json({
                    "type": "completed"
                })
            except Exception as e:
                logger.error(f"Error sending completed: {e}")

        # Configure callbacks
        processor.set_detection_callback(send_detection_result)
        processor.set_progress_callback(send_progress_update)
        processor.set_completed_callback(send_completed)

        # Store processor
        active_processors[video_id] = processor

        # Message handling loop
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            message_type = message.get("type")

            logger.info(f"Received video message type: {message_type}")

            if message_type == "start":
                # Start processing video
                speed = message.get("speed", 1.0)
                processor.set_playback_speed(speed)
                await processor.start_processing()

                await websocket.send_json({
                    "type": "started"
                })

            elif message_type == "pause":
                # Pause processing
                await processor.pause_processing()

                await websocket.send_json({
                    "type": "paused"
                })

            elif message_type == "resume":
                # Resume processing
                await processor.resume_processing()

                await websocket.send_json({
                    "type": "resumed"
                })

            elif message_type == "stop":
                # Stop processing
                await processor.stop_processing()

                await websocket.send_json({
                    "type": "stopped"
                })

            elif message_type == "seek":
                # Seek to frame or timestamp
                frame_number = message.get("frame_number")
                timestamp = message.get("timestamp")

                if frame_number is not None:
                    await processor.seek_to_frame(frame_number)
                elif timestamp is not None:
                    await processor.seek_to_timestamp(timestamp)

                await websocket.send_json({
                    "type": "seeked",
                    "frame_number": processor.current_frame_number
                })

            elif message_type == "settings":
                # Update processing settings
                settings_data = message.get("data", {})
                process_fps = settings_data.get("process_fps")
                confidence_threshold = settings_data.get("confidence_threshold")
                playback_speed = settings_data.get("playback_speed")

                processor.update_settings(
                    process_fps=process_fps,
                    confidence_threshold=confidence_threshold,
                    playback_speed=playback_speed
                )

                await websocket.send_json({
                    "type": "settings_updated",
                    "data": settings_data
                })

            elif message_type == "get_stats":
                # Send current statistics
                stats = processor.get_stats()
                await websocket.send_json({
                    "type": "stats",
                    "data": stats
                })

            elif message_type == "ping":
                # Respond to ping
                await websocket.send_json({
                    "type": "pong"
                })

            else:
                logger.warning(f"Unknown video message type: {message_type}")

    except WebSocketDisconnect:
        logger.info(f"Video WebSocket disconnected: {video_id}")

    except Exception as e:
        logger.error(f"Video WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass

    finally:
        # Cleanup
        if video_id in active_processors:
            await active_processors[video_id].close()
            del active_processors[video_id]

        logger.info(f"Video connection cleaned up: {video_id}")


@router.get("/active")
async def get_active_videos():
    """Get list of active video processing sessions"""
    return {
        "active_count": len(active_processors),
        "sessions": [
            {
                "video_id": video_id,
                "stats": processor.get_stats(),
                "metadata": processor.get_metadata()
            }
            for video_id, processor in active_processors.items()
        ]
    }

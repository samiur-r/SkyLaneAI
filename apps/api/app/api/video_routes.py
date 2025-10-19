"""Video upload and management routes"""
import os
import uuid
import logging
import subprocess
import asyncio
import time
from pathlib import Path
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
import json
import cv2
from app.services.video_file_processor import VideoFileProcessor
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Store active video processors (in production, use Redis or similar)
active_processors: Dict[str, VideoFileProcessor] = {}

# Store uploaded video metadata
uploaded_videos: Dict[str, Dict[str, Any]] = {}


async def _recover_uploaded_videos():
    """
    Recover video metadata from existing files in upload directory.
    This is called on startup to restore state after server restart.
    """
    upload_dir = _get_upload_dir()

    for file_path in upload_dir.glob("*.*"):
        if not _validate_video_file(file_path.name):
            continue

        # Extract video ID from filename (format: {uuid}.{ext})
        video_id = file_path.stem

        # Skip if already in memory
        if video_id in uploaded_videos:
            continue

        try:
            # Extract metadata
            processor = VideoFileProcessor(str(file_path))
            metadata = await processor.initialize()
            await processor.close()

            # Store metadata
            uploaded_videos[video_id] = {
                "video_id": video_id,
                "filename": file_path.name,
                "file_path": str(file_path),
                "size_mb": _get_file_size_mb(file_path),
                "metadata": metadata,
                "uploaded_at": None,
            }

            logger.info(f"Recovered video metadata: {video_id}")
        except Exception as e:
            logger.error(f"Failed to recover metadata for {file_path}: {e}")


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


async def _transcode_to_h264(input_path: Path, output_path: Path) -> bool:
    """
    Transcode video to H.264 codec for browser compatibility.

    Args:
        input_path: Path to input video file
        output_path: Path to output video file

    Returns:
        True if transcoding successful, False otherwise
    """
    try:
        # FFmpeg command for fast H.264 transcoding
        cmd = [
            'ffmpeg',
            '-i', str(input_path),
            '-c:v', 'libx264',          # H.264 video codec
            '-preset', 'fast',           # Fast encoding preset
            '-crf', '23',                # Constant quality (18-28, lower = better)
            '-c:a', 'aac',               # AAC audio codec
            '-b:a', '128k',              # Audio bitrate
            '-movflags', '+faststart',   # Enable streaming
            '-y',                        # Overwrite output file
            str(output_path)
        ]

        logger.info(f"Transcoding video: {input_path.name} -> {output_path.name}")

        # Run FFmpeg asynchronously
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            logger.error(f"FFmpeg transcoding failed: {stderr.decode()}")
            return False

        logger.info(f"Transcoding complete: {output_path.name}")
        return True

    except Exception as e:
        logger.error(f"Transcoding error: {e}")
        return False


async def _check_codec(file_path: Path) -> str:
    """
    Check video codec using ffprobe.

    Args:
        file_path: Path to video file

    Returns:
        Codec name (e.g., 'h264', 'mpeg4', 'vp9')
    """
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(file_path)
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            codec = stdout.decode().strip()
            return codec
        else:
            logger.warning(f"ffprobe failed: {stderr.decode()}")
            return 'unknown'

    except Exception as e:
        logger.error(f"Codec check error: {e}")
        return 'unknown'


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

        # Check video codec
        codec = await _check_codec(file_path)
        logger.info(f"Detected codec: {codec}")

        # Transcode if not H.264
        final_file_path = file_path
        if codec not in ['h264', 'hevc']:  # hevc (H.265) is also supported by most browsers
            logger.info(f"Video codec {codec} not browser-compatible, transcoding to H.264...")

            # Create transcoded file path
            transcoded_path = upload_dir / f"{video_id}_transcoded.mp4"

            # Transcode to H.264
            transcode_success = await _transcode_to_h264(file_path, transcoded_path)

            if not transcode_success:
                file_path.unlink()  # Delete original
                raise HTTPException(
                    status_code=500,
                    detail="Failed to transcode video to browser-compatible format"
                )

            # Delete original and use transcoded file
            file_path.unlink()
            final_file_path = transcoded_path
            logger.info(f"Transcoding successful, using: {final_file_path.name}")

        # Initialize video processor to extract metadata
        processor = VideoFileProcessor(str(final_file_path))
        try:
            metadata = await processor.initialize()
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            final_file_path.unlink()  # Delete file
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
            "file_path": str(final_file_path),
            "size_mb": _get_file_size_mb(final_file_path),
            "metadata": metadata,
            "uploaded_at": None,  # Will be set by proper datetime
            "transcoded": codec not in ['h264', 'hevc']
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


@router.get("/{video_id}/stream")
async def stream_video(video_id: str, request: Request):
    """
    Stream video file with range support for seeking

    Args:
        video_id: Video ID
        request: HTTP request (to get Range header)

    Returns:
        Video file stream
    """
    if video_id not in uploaded_videos:
        raise HTTPException(status_code=404, detail="Video not found")

    video_data = uploaded_videos[video_id]
    file_path = Path(video_data["file_path"])

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")

    # Detect media type from file extension
    ext = file_path.suffix.lower()
    media_type_map = {
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.ogg': 'video/ogg',
        '.avi': 'video/x-msvideo',
        '.mov': 'video/quicktime',
        '.mkv': 'video/x-matroska',
    }
    media_type = media_type_map.get(ext, 'video/mp4')

    # Return file with proper headers for video streaming
    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        headers={
            "Accept-Ranges": "bytes",
            "Content-Disposition": f'inline; filename="{video_data["filename"]}"',
            "Cache-Control": "no-cache",
        }
    )


@router.get("/{video_id}/mjpeg")
async def stream_mjpeg(video_id: str):
    """
    Stream annotated video as MJPEG from processor's completed frame buffer

    This endpoint streams the processed video with bounding boxes already rendered.
    Processing must be completed before playback can begin.

    Args:
        video_id: Video ID

    Returns:
        MJPEG stream response
    """
    # Check if processor exists
    if video_id not in active_processors:
        raise HTTPException(
            status_code=404,
            detail="Video processor not found. Upload and process video first."
        )

    processor = active_processors[video_id]

    # Check if processing is completed
    if not processor.is_mjpeg_ready():
        raise HTTPException(
            status_code=425,  # Too Early
            detail="Processing not completed yet. Wait for processing to finish."
        )

    logger.info(f"Starting MJPEG stream for video {video_id}")

    async def generate_mjpeg_frames():
        """Generate MJPEG frames from completed buffer"""
        try:
            # Calculate frame delay based on processing FPS
            frame_delay = 1.0 / processor.mjpeg_fps

            # Get reference to the frame buffer
            frame_buffer = processor.get_annotated_frames()
            total_frames = len(frame_buffer)

            logger.info(f"MJPEG stream ready: {total_frames} frames available")

            # Start playback
            processor.mjpeg_play()

            # Stream all frames
            while processor.mjpeg_current_index < total_frames:
                # Check if still playing (not paused/stopped)
                if not processor.mjpeg_playing:
                    await asyncio.sleep(0.1)  # Wait while paused
                    continue

                # Get current frame
                frame = frame_buffer[processor.mjpeg_current_index]
                processor.mjpeg_current_index += 1

                # Encode frame to JPEG
                encode_params = [cv2.IMWRITE_JPEG_QUALITY, 85]
                success, buffer = cv2.imencode('.jpg', frame, encode_params)

                if success:
                    # Yield frame in MJPEG format
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' +
                           buffer.tobytes() + b'\r\n')

                # Frame rate throttling
                await asyncio.sleep(frame_delay)

            logger.info(f"MJPEG stream completed for video {video_id}")
            processor.mjpeg_stop()

        except Exception as e:
            logger.error(f"Error streaming MJPEG frames: {e}")
            processor.mjpeg_stop()

    return StreamingResponse(
        generate_mjpeg_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


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

            elif message_type == "mjpeg_play":
                # Start MJPEG playback (after processing is complete)
                try:
                    processor.mjpeg_play()
                    await websocket.send_json({
                        "type": "mjpeg_playing"
                    })
                except RuntimeError as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })

            elif message_type == "mjpeg_pause":
                # Pause MJPEG playback
                processor.mjpeg_pause()
                await websocket.send_json({
                    "type": "mjpeg_paused"
                })

            elif message_type == "mjpeg_resume":
                # Resume MJPEG playback
                try:
                    processor.mjpeg_resume()
                    await websocket.send_json({
                        "type": "mjpeg_resumed"
                    })
                except RuntimeError as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })

            elif message_type == "mjpeg_stop":
                # Stop MJPEG playback
                processor.mjpeg_stop()
                await websocket.send_json({
                    "type": "mjpeg_stopped"
                })

            elif message_type == "get_status":
                # Get processing and playback status
                await websocket.send_json({
                    "type": "status",
                    "data": {
                        "processing_completed": processor.processing_completed,
                        "mjpeg_ready": processor.is_mjpeg_ready(),
                        "mjpeg_playing": processor.mjpeg_playing,
                        "total_frames": len(processor.get_annotated_frames())
                    }
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

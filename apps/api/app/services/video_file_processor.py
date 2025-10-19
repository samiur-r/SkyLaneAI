"""Video file processing service for uploaded videos"""
import asyncio
import time
import logging
from typing import Optional, Callable, Dict, Any
from pathlib import Path
import cv2
import numpy as np
from app.services.detector import detector
from app.models.schemas import Detection

logger = logging.getLogger(__name__)


class VideoFileProcessor:
    """Processes uploaded video files frame-by-frame with YOLO detection"""

    def __init__(
        self,
        video_path: str,
        process_fps: Optional[int] = None,
        confidence_threshold: float = 0.25
    ):
        """
        Initialize video file processor

        Args:
            video_path: Path to the video file
            process_fps: Target FPS for processing (None = use video's native FPS)
            confidence_threshold: Minimum confidence for detections
        """
        self.video_path = Path(video_path)
        self.process_fps = process_fps
        self.confidence_threshold = confidence_threshold

        # Video capture
        self.cap: Optional[cv2.VideoCapture] = None
        self.video_metadata: Optional[Dict[str, Any]] = None

        # Playback state
        self.is_playing = False
        self.is_paused = False
        self.playback_speed = 1.0
        self.current_frame_number = 0

        # Callback for detection results
        self.on_detection_callback: Optional[Callable] = None
        self.on_progress_callback: Optional[Callable] = None
        self.on_completed_callback: Optional[Callable] = None

        # Processing task
        self.processing_task: Optional[asyncio.Task] = None

        # Statistics
        self.stats = {
            "frames_processed": 0,
            "detections_count": 0,
            "avg_processing_time": 0,
            "start_time": None,
            "end_time": None
        }

    async def initialize(self) -> Dict[str, Any]:
        """
        Initialize video capture and extract metadata

        Returns:
            Video metadata dictionary
        """
        try:
            if not self.video_path.exists():
                raise FileNotFoundError(f"Video file not found: {self.video_path}")

            # Open video file
            self.cap = cv2.VideoCapture(str(self.video_path))

            if not self.cap.isOpened():
                raise RuntimeError(f"Failed to open video file: {self.video_path}")

            # Extract metadata
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = total_frames / fps if fps > 0 else 0

            self.video_metadata = {
                "fps": fps,
                "total_frames": total_frames,
                "width": width,
                "height": height,
                "duration": duration,
                "codec": self._get_codec_name()
            }

            # Set process FPS to video FPS if not specified
            if self.process_fps is None:
                self.process_fps = int(fps)

            logger.info(f"Video initialized: {self.video_metadata}")
            return self.video_metadata

        except Exception as e:
            logger.error(f"Error initializing video: {e}")
            raise

    def _get_codec_name(self) -> str:
        """Get video codec name"""
        if not self.cap:
            return "unknown"

        fourcc = int(self.cap.get(cv2.CAP_PROP_FOURCC))
        codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
        return codec

    def set_detection_callback(self, callback: Callable):
        """Set callback to send detection results"""
        self.on_detection_callback = callback

    def set_progress_callback(self, callback: Callable):
        """Set callback to send progress updates"""
        self.on_progress_callback = callback

    def set_completed_callback(self, callback: Callable):
        """Set callback when video processing completes"""
        self.on_completed_callback = callback

    async def start_processing(self):
        """Start processing video frames"""
        if self.is_playing:
            logger.warning("Processing already started")
            return

        if not self.cap:
            raise RuntimeError("Video not initialized. Call initialize() first.")

        self.is_playing = True
        self.is_paused = False
        self.stats["start_time"] = time.time()

        self.processing_task = asyncio.create_task(self._process_loop())
        logger.info(f"Started video processing at {self.process_fps} FPS")

    async def pause_processing(self):
        """Pause video processing"""
        self.is_paused = True
        logger.info("Video processing paused")

    async def resume_processing(self):
        """Resume video processing"""
        self.is_paused = False
        logger.info("Video processing resumed")

    async def stop_processing(self):
        """Stop processing video"""
        self.is_playing = False
        self.is_paused = False

        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass

        self.stats["end_time"] = time.time()
        logger.info("Stopped video processing")

    async def seek_to_frame(self, frame_number: int):
        """
        Seek to specific frame

        Args:
            frame_number: Target frame number (0-indexed)
        """
        if not self.cap or not self.video_metadata:
            raise RuntimeError("Video not initialized")

        # Clamp to valid range
        frame_number = max(0, min(frame_number, self.video_metadata["total_frames"] - 1))

        # Set frame position
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        self.current_frame_number = frame_number

        logger.info(f"Seeked to frame {frame_number}")

    async def seek_to_timestamp(self, timestamp: float):
        """
        Seek to specific timestamp in seconds

        Args:
            timestamp: Target timestamp in seconds
        """
        if not self.video_metadata:
            raise RuntimeError("Video not initialized")

        # Convert timestamp to frame number
        frame_number = int(timestamp * self.video_metadata["fps"])
        await self.seek_to_frame(frame_number)

    def set_playback_speed(self, speed: float):
        """
        Set playback speed

        Args:
            speed: Playback speed multiplier (e.g., 0.5, 1.0, 2.0)
        """
        self.playback_speed = max(0.1, min(speed, 4.0))  # Clamp between 0.1x and 4x
        logger.info(f"Playback speed set to {self.playback_speed}x")

    async def _process_loop(self):
        """Main processing loop"""
        try:
            if not self.cap or not self.video_metadata:
                raise RuntimeError("Video not initialized")

            # Calculate frame interval based on FPS and playback speed
            base_interval = 1.0 / self.process_fps

            while self.is_playing:
                # Handle pause
                if self.is_paused:
                    await asyncio.sleep(0.1)
                    continue

                # Adjust interval for playback speed
                frame_interval = base_interval / self.playback_speed

                # Read next frame
                ret, frame = self.cap.read()

                if not ret:
                    # End of video
                    logger.info("Reached end of video")
                    await self._on_video_completed()
                    break

                # Process frame
                await self._process_frame(frame, self.current_frame_number)

                # Update frame number
                self.current_frame_number += 1

                # Send progress update
                await self._send_progress_update()

                # Wait for next frame (accounting for processing time)
                await asyncio.sleep(frame_interval)

        except asyncio.CancelledError:
            logger.info("Processing loop cancelled")
        except Exception as e:
            logger.error(f"Error in processing loop: {e}")
        finally:
            self.is_playing = False

    async def _process_frame(self, frame: np.ndarray, frame_number: int):
        """
        Process a single frame with YOLO detection

        Args:
            frame: Video frame as numpy array (BGR format)
            frame_number: Frame sequence number
        """
        try:
            # Run detection (blocking operation, but fast enough)
            detections, processing_time = await asyncio.to_thread(
                detector.detect, frame
            )

            self.stats["frames_processed"] += 1
            self.stats["detections_count"] += len(detections)

            # Update average processing time
            if self.stats["frames_processed"] == 1:
                self.stats["avg_processing_time"] = processing_time
            else:
                alpha = 0.1  # Smoothing factor
                self.stats["avg_processing_time"] = (
                    alpha * processing_time +
                    (1 - alpha) * self.stats["avg_processing_time"]
                )

            # Calculate timestamp
            timestamp = frame_number / self.video_metadata["fps"] if self.video_metadata else 0

            # Send detections to frontend via callback
            if self.on_detection_callback:
                result = {
                    "frame_number": frame_number,
                    "timestamp": timestamp,
                    "detections": [det.model_dump() for det in detections],
                    "processing_time_ms": processing_time,
                    "frameWidth": frame.shape[1],
                    "frameHeight": frame.shape[0],
                    "stats": {
                        "frames_processed": self.stats["frames_processed"],
                        "detections_count": self.stats["detections_count"],
                        "avg_processing_time": self.stats["avg_processing_time"]
                    }
                }
                await self.on_detection_callback(result)

            logger.debug(
                f"Frame {frame_number}: {len(detections)} detections, "
                f"{processing_time:.1f}ms"
            )

        except Exception as e:
            logger.error(f"Error processing frame {frame_number}: {e}")

    async def _send_progress_update(self):
        """Send progress update to frontend"""
        if self.on_progress_callback and self.video_metadata:
            progress = {
                "current_frame": self.current_frame_number,
                "total_frames": self.video_metadata["total_frames"],
                "percentage": (self.current_frame_number / self.video_metadata["total_frames"]) * 100
            }
            await self.on_progress_callback(progress)

    async def _on_video_completed(self):
        """Handle video completion"""
        self.is_playing = False
        self.stats["end_time"] = time.time()

        if self.on_completed_callback:
            await self.on_completed_callback()

        logger.info(f"Video processing completed. Stats: {self.stats}")

    def update_settings(
        self,
        process_fps: Optional[int] = None,
        confidence_threshold: Optional[float] = None,
        playback_speed: Optional[float] = None
    ):
        """
        Update processing settings

        Args:
            process_fps: New target FPS
            confidence_threshold: New confidence threshold
            playback_speed: New playback speed
        """
        if process_fps is not None:
            self.process_fps = process_fps
            logger.info(f"Updated processing FPS to {process_fps}")

        if confidence_threshold is not None:
            self.confidence_threshold = confidence_threshold
            logger.info(f"Updated confidence threshold to {confidence_threshold}")

        if playback_speed is not None:
            self.set_playback_speed(playback_speed)

    def get_stats(self) -> dict:
        """Get current processing statistics"""
        return self.stats.copy()

    def get_metadata(self) -> Optional[Dict[str, Any]]:
        """Get video metadata"""
        return self.video_metadata

    async def close(self):
        """Clean up resources"""
        await self.stop_processing()

        if self.cap:
            self.cap.release()
            self.cap = None

        logger.info("Video file processor closed")

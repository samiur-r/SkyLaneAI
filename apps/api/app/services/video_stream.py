"""Video stream processing service"""
import asyncio
import time
import logging
from typing import Optional, Callable
from collections import deque
import numpy as np
from app.services.detector import detector
from app.models.schemas import Detection

logger = logging.getLogger(__name__)


class VideoStreamProcessor:
    """Processes video frames from WebRTC stream with YOLO detection"""

    def __init__(
        self,
        process_fps: int = 10,
        max_queue_size: int = 30,
        skip_frames: bool = True
    ):
        """
        Initialize video stream processor

        Args:
            process_fps: Target FPS for processing (e.g., 10 = process 10 frames per second)
            max_queue_size: Maximum number of frames to keep in queue
            skip_frames: If True, skip frames when processing is slow
        """
        self.process_fps = process_fps
        self.max_queue_size = max_queue_size
        self.skip_frames = skip_frames
        self.frame_queue = deque(maxlen=max_queue_size)
        self.is_processing = False
        self.last_process_time = 0
        self.frame_interval = 1.0 / process_fps  # Time between frames in seconds
        self.on_detection_callback: Optional[Callable] = None
        self.processing_task: Optional[asyncio.Task] = None

        # Statistics
        self.stats = {
            "frames_received": 0,
            "frames_processed": 0,
            "frames_skipped": 0,
            "avg_processing_time": 0,
            "detections_count": 0
        }

    def set_detection_callback(self, callback: Callable):
        """Set callback to send detection results"""
        self.on_detection_callback = callback

    async def on_frame_received(self, frame: np.ndarray, frame_number: int):
        """
        Called when a new frame is received from WebRTC

        Args:
            frame: Video frame as numpy array (BGR format)
            frame_number: Frame sequence number
        """
        self.stats["frames_received"] += 1

        # Add frame to queue with timestamp
        current_time = time.time()

        # Check if enough time has passed since last processing
        if current_time - self.last_process_time >= self.frame_interval:
            self.frame_queue.append({
                "frame": frame,
                "frame_number": frame_number,
                "timestamp": current_time
            })
        else:
            if self.skip_frames:
                self.stats["frames_skipped"] += 1

    async def start_processing(self):
        """Start processing frames from the queue"""
        if self.is_processing:
            logger.warning("Processing already started")
            return

        self.is_processing = True
        self.processing_task = asyncio.create_task(self._process_loop())
        logger.info(f"Started video processing at {self.process_fps} FPS")

    async def stop_processing(self):
        """Stop processing frames"""
        self.is_processing = False
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped video processing")

    async def _process_loop(self):
        """Main processing loop"""
        try:
            while self.is_processing:
                if len(self.frame_queue) > 0:
                    # Get the latest frame from queue
                    frame_data = self.frame_queue.popleft()
                    await self._process_frame(frame_data)
                else:
                    # No frames in queue, wait a bit
                    await asyncio.sleep(0.01)

        except asyncio.CancelledError:
            logger.info("Processing loop cancelled")
        except Exception as e:
            logger.error(f"Error in processing loop: {e}")

    async def _process_frame(self, frame_data: dict):
        """
        Process a single frame with YOLO detection

        Args:
            frame_data: Dictionary containing frame, frame_number, and timestamp
        """
        try:
            frame = frame_data["frame"]
            frame_number = frame_data["frame_number"]

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

            self.last_process_time = time.time()

            # Send detections to frontend via callback
            if self.on_detection_callback:
                result = {
                    "frame_number": frame_number,
                    "timestamp": frame_data["timestamp"],
                    "detections": [det.model_dump() for det in detections],
                    "processing_time_ms": processing_time,
                    "stats": self.stats.copy()
                }
                await self.on_detection_callback(result)

            logger.debug(
                f"Frame {frame_number}: {len(detections)} detections, "
                f"{processing_time:.1f}ms"
            )

        except Exception as e:
            logger.error(f"Error processing frame: {e}")

    def update_settings(self, process_fps: Optional[int] = None,
                       skip_frames: Optional[bool] = None):
        """
        Update processing settings

        Args:
            process_fps: New target FPS
            skip_frames: Enable/disable frame skipping
        """
        if process_fps is not None:
            self.process_fps = process_fps
            self.frame_interval = 1.0 / process_fps
            logger.info(f"Updated processing FPS to {process_fps}")

        if skip_frames is not None:
            self.skip_frames = skip_frames
            logger.info(f"Frame skipping: {skip_frames}")

    def get_stats(self) -> dict:
        """Get current processing statistics"""
        return self.stats.copy()

    def reset_stats(self):
        """Reset statistics"""
        self.stats = {
            "frames_received": 0,
            "frames_processed": 0,
            "frames_skipped": 0,
            "avg_processing_time": 0,
            "detections_count": 0
        }
        logger.info("Statistics reset")

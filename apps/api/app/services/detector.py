"""YOLO detection service"""
import os
import time
from pathlib import Path
from typing import Any
import numpy as np
from ultralytics import YOLO
from app.core.config import settings
from app.models.schemas import Detection, DetectionBox


class YOLODetector:
    """YOLO-based object detector"""

    def __init__(self):
        """Initialize the YOLO model"""
        self.model = None
        self.model_path = None
        self.load_model()

    def _ensure_models_dir(self) -> Path:
        """Ensure models directory exists"""
        models_dir = Path(settings.MODELS_DIR)
        models_dir.mkdir(parents=True, exist_ok=True)
        return models_dir

    def _get_model_path(self) -> str:
        """Get the full path to the model file"""
        if settings.MODEL_CACHE_ENABLED:
            models_dir = self._ensure_models_dir()
            model_path = models_dir / settings.MODEL_NAME
            return str(model_path)
        else:
            # Use model name directly (will download to ultralytics cache)
            return settings.MODEL_NAME

    def load_model(self) -> None:
        """Load the YOLO model with caching support"""
        try:
            self.model_path = self._get_model_path()

            # Check if model exists in cache
            if settings.MODEL_CACHE_ENABLED and os.path.exists(self.model_path):
                print(f"✓ Loading cached YOLO model from: {self.model_path}")
            else:
                print(f"✓ Downloading YOLO model: {settings.MODEL_NAME}")
                if settings.MODEL_CACHE_ENABLED:
                    print(f"  Will be cached to: {self.model_path}")

            # Load the model (will download if not exists)
            self.model = YOLO(self.model_path)

            # Move model to specified device (CPU or GPU)
            self.model.to(settings.MODEL_DEVICE)
            print(f"✓ YOLO model loaded successfully on device: {settings.MODEL_DEVICE}")

        except Exception as e:
            print(f"✗ Error loading YOLO model: {e}")
            raise

    def detect(self, image: np.ndarray) -> tuple[list[Detection], float]:
        """
        Perform object detection on an image

        Args:
            image: Input image as numpy array (BGR format)

        Returns:
            Tuple of (list of detections, processing time in ms)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")

        start_time = time.time()

        # Run inference
        results = self.model(
            image,
            conf=settings.CONFIDENCE_THRESHOLD,
            iou=settings.IOU_THRESHOLD,
            device=settings.MODEL_DEVICE,
            verbose=False
        )

        # Parse results
        detections = []
        for result in results:
            boxes = result.boxes
            for i in range(len(boxes)):
                box = boxes.xyxy[i].cpu().numpy()
                conf = float(boxes.conf[i].cpu().numpy())
                cls_id = int(boxes.cls[i].cpu().numpy())
                cls_name = result.names[cls_id]

                detection = Detection(
                    class_name=cls_name,
                    class_id=cls_id,
                    confidence=conf,
                    bbox=DetectionBox(
                        x1=float(box[0]),
                        y1=float(box[1]),
                        x2=float(box[2]),
                        y2=float(box[3])
                    )
                )
                detections.append(detection)

        processing_time = (time.time() - start_time) * 1000  # Convert to ms

        return detections, processing_time


# Global detector instance
detector = YOLODetector()

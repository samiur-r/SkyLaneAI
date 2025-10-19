"""YOLO detection service"""
import os
import time
from pathlib import Path
from typing import Any
import numpy as np
import cv2
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

    def render_detections(self, image: np.ndarray, detections: list[Detection]) -> np.ndarray:
        """
        Render bounding boxes and labels on image

        Args:
            image: Input image as numpy array (BGR format)
            detections: List of detections to render

        Returns:
            Annotated image
        """
        annotated = image.copy()

        # Color mapping for different classes
        class_colors = {
            'bird': (68, 68, 239),      # Red (BGR)
            'drone': (11, 158, 245),    # Amber (BGR)
            'aircraft': (246, 130, 59),  # Blue (BGR)
            'person': (129, 185, 16),    # Green (BGR)
            'car': (246, 92, 139),       # Purple (BGR)
            'balloon': (153, 72, 236),   # Pink (BGR)
            'kite': (166, 184, 20),      # Teal (BGR)
        }
        default_color = (128, 123, 107)  # Gray (BGR)

        for detection in detections:
            bbox = detection.bbox
            x1, y1 = int(bbox.x1), int(bbox.y1)
            x2, y2 = int(bbox.x2), int(bbox.y2)

            # Get color for this class
            color = class_colors.get(detection.class_name.lower(), default_color)

            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)

            # Prepare label
            label = f"{detection.class_name} {int(detection.confidence * 100)}%"

            # Get label size
            (label_w, label_h), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )

            # Position label above box, or below if too close to top
            label_y = y1 - 10 if y1 > 30 else y2 + label_h + 10
            label_x = x1

            # Draw label background
            cv2.rectangle(
                annotated,
                (label_x, label_y - label_h - 5),
                (label_x + label_w + 10, label_y + 5),
                color,
                -1
            )

            # Draw label text
            cv2.putText(
                annotated,
                label,
                (label_x + 5, label_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

        return annotated


# Global detector instance
detector = YOLODetector()

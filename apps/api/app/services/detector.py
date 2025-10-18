"""YOLO detection service"""
import time
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
        self.load_model()

    def load_model(self) -> None:
        """Load the YOLO model"""
        try:
            self.model = YOLO(settings.MODEL_PATH)
            print(f"✓ YOLO model loaded: {settings.MODEL_PATH}")
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

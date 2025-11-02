"""DETR (Detection Transformer) detection service"""
import time
from pathlib import Path
from typing import Any
import numpy as np
import cv2
from PIL import Image
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from app.core.config import settings
from app.models.schemas import Detection, DetectionBox


class DETRDetector:
    """DETR-based object detector"""

    def __init__(self):
        """Initialize the DETR model"""
        self.model = None
        self.processor = None
        self.device = None
        self.load_model()

    def load_model(self) -> None:
        """Load the DETR model from Hugging Face"""
        try:
            print(f"✓ Loading DETR model: facebook/detr-resnet-50")

            # Determine device
            if settings.MODEL_DEVICE == "cuda" and torch.cuda.is_available():
                self.device = torch.device("cuda")
            else:
                self.device = torch.device("cpu")

            # Load processor and model
            self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
            self.model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

            # Move model to device
            self.model.to(self.device)
            self.model.eval()

            print(f"✓ DETR model loaded successfully on device: {self.device}")

        except Exception as e:
            print(f"✗ Error loading DETR model: {e}")
            raise

    def detect(self, image: np.ndarray) -> tuple[list[Detection], float]:
        """
        Perform object detection on an image

        Args:
            image: Input image as numpy array (BGR format from OpenCV)

        Returns:
            Tuple of (list of detections, processing time in ms)
        """
        if self.model is None or self.processor is None:
            raise RuntimeError("Model not loaded")

        start_time = time.time()

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image
        pil_image = Image.fromarray(image_rgb)

        # Preprocess image
        inputs = self.processor(images=pil_image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Post-process outputs
        target_sizes = torch.tensor([pil_image.size[::-1]]).to(self.device)
        results = self.processor.post_process_object_detection(
            outputs,
            target_sizes=target_sizes,
            threshold=settings.CONFIDENCE_THRESHOLD
        )[0]

        # Parse results and filter by sky hazard classes
        detections = []
        sky_hazard_classes = settings.SKY_HAZARD_CLASSES

        # COCO class names (same as YOLO)
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            conf = float(score.cpu().numpy())
            cls_id = int(label.cpu().numpy())

            # Get class name from COCO classes
            cls_name = self.model.config.id2label[cls_id]

            # Filter: Only include sky hazard classes
            if sky_hazard_classes and cls_name not in sky_hazard_classes:
                continue

            # Extract box coordinates
            bbox = box.cpu().numpy()

            detection = Detection(
                class_name=cls_name,
                class_id=cls_id,
                confidence=conf,
                bbox=DetectionBox(
                    x1=float(bbox[0]),
                    y1=float(bbox[1]),
                    x2=float(bbox[2]),
                    y2=float(bbox[3])
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
            'bird': (68, 68, 239),       # Red (BGR)
            'drone': (11, 158, 245),     # Amber/Orange (BGR)
            'balloon': (153, 72, 236),   # Pink/Purple (BGR)
            'aircraft': (246, 130, 59),  # Blue (BGR)
            'airplane': (246, 130, 59),  # Blue (BGR)
            'person': (129, 185, 16),    # Green (BGR)
            'car': (246, 92, 139),       # Purple (BGR)
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
detr_detector = DETRDetector()

"""Context Enrichment Agent - Rule-based context extraction from detections"""
import logging
from app.models.schemas import Detection, EnrichedContext

logger = logging.getLogger(__name__)


class ContextEnrichmentAgent:
    """
    Rule-based agent that enriches detection data with contextual information.
    This agent does not use LLMs - it's purely computational for speed and cost efficiency.
    """

    # Size thresholds for different hazard types (in pixels^2)
    # These are calibrated for typical camera resolutions (1920x1080)
    # Note: Class names are already normalized (airplane/helicopter -> drone)
    SIZE_THRESHOLDS = {
        "bird": {"small": 5000, "medium": 15000},
        "drone": {"small": 8000, "medium": 20000},  # Includes airplane, helicopter, quadcopter
        "balloon": {"small": 10000, "medium": 25000},
        "kite": {"small": 7000, "medium": 18000},
        # Default for unknown classes
        "default": {"small": 6000, "medium": 15000}
    }

    # Threat level multipliers based on confidence
    CONFIDENCE_LEVELS = {
        "very_high": 0.85,  # >= 85%
        "high": 0.70,       # >= 70%
        "medium": 0.50,     # >= 50%
        "low": 0.0          # < 50%
    }

    def __init__(self, image_width: int = 1920, image_height: int = 1080):
        """
        Initialize the Context Enrichment Agent

        Args:
            image_width: Default image width for calculations
            image_height: Default image height for calculations
        """
        self.image_width = image_width
        self.image_height = image_height
        logger.info("ContextEnrichmentAgent initialized")

    def enrich(
        self,
        detection: Detection,
        image_width: int = None,
        image_height: int = None
    ) -> EnrichedContext:
        """
        Enrich a detection with contextual information

        Args:
            detection: The detection to enrich
            image_width: Override default image width
            image_height: Override default image height

        Returns:
            EnrichedContext with computed contextual data
        """
        # Use provided dimensions or defaults
        img_w = image_width or self.image_width
        img_h = image_height or self.image_height

        # Calculate bounding box area
        bbox = detection.bbox
        bbox_area = int((bbox.x2 - bbox.x1) * (bbox.y2 - bbox.y1))

        # Estimate size category
        estimated_size = self._estimate_size(detection.class_name, bbox_area)

        # Determine screen position
        screen_position = self._get_screen_position(bbox, img_w, img_h)

        # Calculate initial threat level
        threat_level = self._calculate_threat_level(
            detection.confidence,
            estimated_size,
            bbox_area,
            img_w * img_h
        )

        context = EnrichedContext(
            estimated_size=estimated_size,
            bbox_area_pixels=bbox_area,
            screen_position=screen_position,
            threat_level_raw=threat_level
        )

        logger.debug(
            f"Enriched {detection.class_name}: size={estimated_size}, "
            f"position={screen_position}, threat={threat_level}"
        )

        return context

    def _estimate_size(self, class_name: str, bbox_area: int) -> str:
        """
        Estimate object size category based on class and bounding box area

        Args:
            class_name: Name of detected class
            bbox_area: Bounding box area in pixels

        Returns:
            Size category: "small", "medium", or "large"
        """
        # Get thresholds for this class (or default)
        thresholds = self.SIZE_THRESHOLDS.get(
            class_name.lower(),
            self.SIZE_THRESHOLDS["default"]
        )

        if bbox_area < thresholds["small"]:
            return "small"
        elif bbox_area < thresholds["medium"]:
            return "medium"
        else:
            return "large"

    def _get_screen_position(
        self,
        bbox,
        image_width: int,
        image_height: int
    ) -> str:
        """
        Determine position of object on screen

        Args:
            bbox: Bounding box with x1, y1, x2, y2
            image_width: Image width in pixels
            image_height: Image height in pixels

        Returns:
            Position string (e.g., "upper-left", "center", "lower-right")
        """
        # Calculate center of bounding box
        center_x = (bbox.x1 + bbox.x2) / 2
        center_y = (bbox.y1 + bbox.y2) / 2

        # Divide screen into 3x3 grid
        # Vertical position
        if center_y < image_height * 0.33:
            vertical = "upper"
        elif center_y < image_height * 0.67:
            vertical = "middle"
        else:
            vertical = "lower"

        # Horizontal position
        if center_x < image_width * 0.33:
            horizontal = "left"
        elif center_x < image_width * 0.67:
            horizontal = "center"
        else:
            horizontal = "right"

        # Combine positions
        if horizontal == "center" and vertical == "middle":
            return "center"
        elif horizontal == "center":
            return vertical
        elif vertical == "middle":
            return horizontal
        else:
            return f"{vertical}-{horizontal}"

    def _calculate_threat_level(
        self,
        confidence: float,
        size: str,
        bbox_area: int,
        total_image_area: int
    ) -> str:
        """
        Calculate initial threat level based on multiple factors

        Args:
            confidence: Detection confidence (0-1)
            size: Size category ("small", "medium", "large")
            bbox_area: Bounding box area in pixels
            total_image_area: Total image area in pixels

        Returns:
            Threat level: "low", "moderate", "high", or "critical"
        """
        # Calculate what percentage of screen the object occupies
        screen_coverage = bbox_area / total_image_area

        # Determine confidence level
        if confidence >= self.CONFIDENCE_LEVELS["very_high"]:
            conf_multiplier = 1.0
        elif confidence >= self.CONFIDENCE_LEVELS["high"]:
            conf_multiplier = 0.8
        elif confidence >= self.CONFIDENCE_LEVELS["medium"]:
            conf_multiplier = 0.6
        else:
            conf_multiplier = 0.4

        # Size multiplier
        size_multipliers = {
            "small": 0.5,
            "medium": 0.75,
            "large": 1.0
        }
        size_multiplier = size_multipliers.get(size, 0.5)

        # Screen coverage multiplier (objects taking up more screen = higher threat)
        if screen_coverage > 0.15:  # > 15% of screen
            coverage_multiplier = 1.2
        elif screen_coverage > 0.08:  # > 8% of screen
            coverage_multiplier = 1.0
        elif screen_coverage > 0.03:  # > 3% of screen
            coverage_multiplier = 0.8
        else:
            coverage_multiplier = 0.6

        # Calculate composite threat score (0-1 scale)
        threat_score = conf_multiplier * size_multiplier * coverage_multiplier

        # Map to threat level
        if threat_score >= 0.85:
            return "critical"
        elif threat_score >= 0.65:
            return "high"
        elif threat_score >= 0.40:
            return "moderate"
        else:
            return "low"

    def enrich_batch(
        self,
        detections: list[Detection],
        image_width: int = None,
        image_height: int = None
    ) -> list[EnrichedContext]:
        """
        Enrich multiple detections at once

        Args:
            detections: List of detections to enrich
            image_width: Override default image width
            image_height: Override default image height

        Returns:
            List of EnrichedContext objects
        """
        return [
            self.enrich(det, image_width, image_height)
            for det in detections
        ]


# Global instance (can be reused across requests)
context_agent = ContextEnrichmentAgent()

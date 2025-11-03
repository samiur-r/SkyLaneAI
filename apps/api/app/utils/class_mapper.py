"""
Class name mapping and normalization for sky hazard detection.

This module provides utilities to map raw YOLO detection class names
to standardized hazard categories for consistent processing and display.
"""

# Map raw YOLO-World detections to standardized hazard types
CLASS_NAME_MAPPING = {
    # Aircraft -> Drone
    "airplane": "drone",
    "aircraft": "drone",
    "helicopter": "drone",
    "quadcopter": "drone",

    # Balloons
    "hot air balloon": "balloon",
    "weather balloon": "balloon",
    "sports ball": "balloon",  # May detect balloons as sports balls

    # Identity mappings (already standardized)
    "drone": "drone",
    "bird": "bird",
    "kite": "kite",
    "balloon": "balloon",
}


def normalize_class_name(raw_class_name: str) -> str:
    """
    Map raw YOLO class names to standardized hazard types.

    Args:
        raw_class_name: Raw class name from YOLO-World detection

    Returns:
        Standardized hazard type name (e.g., "drone", "bird", "balloon", "kite")

    Examples:
        >>> normalize_class_name("airplane")
        "drone"
        >>> normalize_class_name("helicopter")
        "drone"
        >>> normalize_class_name("hot air balloon")
        "balloon"
        >>> normalize_class_name("bird")
        "bird"
    """
    # Convert to lowercase for case-insensitive matching
    normalized = CLASS_NAME_MAPPING.get(
        raw_class_name.lower(),
        raw_class_name.lower()  # Return original if no mapping found
    )
    return normalized

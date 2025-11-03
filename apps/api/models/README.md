# Models Directory

This directory is used to cache YOLO-World models locally.

## About

When the application starts, it will automatically download the specified YOLO-World model (default: `yolov8l-world.pt`) to this directory. This avoids re-downloading the model on every restart.

YOLO-World is an open-vocabulary object detector that can detect ANY object using text prompts - no training required!

## Configuration

Configure model settings in `.env`:

```env
MODELS_DIR="models"                   # Directory to store models
MODEL_NAME="yolov8l-world.pt"         # YOLO-World model to use
MODEL_CACHE_ENABLED=true              # Enable local caching
CONFIDENCE_THRESHOLD=0.15             # Lower for small objects
```

## Available YOLO-World Models

YOLO-World models (from fastest to most accurate):

| Model | Size | Speed | Accuracy | Recommended For |
|-------|------|-------|----------|----------------|
| `yolov8s-world.pt` | ~32MB | Fastest | Good | Real-time, embedded devices |
| `yolov8m-world.pt` | ~99MB | Fast | Better | Balanced performance |
| `yolov8l-world.pt` | ~183MB | Medium | Excellent | Production (RECOMMENDED) |
| `yolov8x-world.pt` | ~252MB | Slower | Best | Maximum accuracy |

For aerial hazard detection (drones, birds, balloons), we recommend:
- **MacBook Air M4**: `yolov8l-world.pt` (large - best balance)
- **GPU Server**: `yolov8x-world.pt` (extra-large - maximum accuracy)
- **Embedded**: `yolov8s-world.pt` (small - fastest)

## Zero-Shot Detection

YOLO-World can detect custom classes without training! Configure in `config.py`:

```python
SKY_HAZARD_CLASSES = [
    "drone",        # Detects drones/UAVs
    "bird",         # Detects birds
    "airplane",     # Detects aircraft
    "helicopter",   # Detects helicopters
    "balloon",      # Detects balloons
    "kite"          # Detects kites
]
```

Add ANY class you want - YOLO-World will detect it!

## Switching Models

To use a different model, update `MODEL_NAME` in your `.env` file:

```env
MODEL_NAME="yolov8x-world.pt"
```

The new model will be downloaded automatically on next startup.

## Cache Location

- Models are cached in `apps/api/models/`
- This directory is git-ignored
- Delete this directory to force re-download of models

## Manual Download

If you want to pre-download a model:

```bash
cd apps/api
python -c "from ultralytics import YOLOWorld; YOLOWorld('yolov8l-world.pt')"
```

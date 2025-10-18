# Models Directory

This directory is used to cache YOLO models locally.

## About

When the application starts, it will automatically download the specified YOLO model (default: `yolo11n.pt`) to this directory. This avoids re-downloading the model on every restart.

## Configuration

Configure model settings in `.env` or `.env.example`:

```env
MODELS_DIR="models"              # Directory to store models
MODEL_NAME="yolo11n.pt"          # Model to use
MODEL_CACHE_ENABLED=true         # Enable local caching
```

## Available YOLO Models

YOLOv11 models (from fastest to most accurate):

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| `yolo11n.pt` | ~6MB | Fastest | Good |
| `yolo11s.pt` | ~22MB | Fast | Better |
| `yolo11m.pt` | ~50MB | Medium | Very Good |
| `yolo11l.pt` | ~100MB | Slow | Excellent |
| `yolo11x.pt` | ~150MB | Slowest | Best |

For real-time video streaming, we recommend:
- **Development/Testing**: `yolo11n.pt` (nano - fastest)
- **Production**: `yolo11s.pt` or `yolo11m.pt` (small/medium - balanced)

## Switching Models

To use a different model, update `MODEL_NAME` in your `.env` file:

```env
MODEL_NAME="yolo11s.pt"
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
uv run python -c "from ultralytics import YOLO; YOLO('models/yolo11n.pt')"
```

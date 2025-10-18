# SkyLaneAI v2 - Development Plan

## Overview

This document outlines the development plan for SkyLaneAI v2, broken down into phases:
- **Phase 1**: Project setup with Next.js frontend and FastAPI backend (Foundation)
- **Phase 2**: Live video streaming with WebRTC and real-time detection
- **Phase 3**: Advanced features (database, analytics, custom training)

---

## Phase 1: Project Setup & Foundation

### 1.1 Initialize Monorepo Structure
**Goal**: Set up pnpm workspace with proper configuration

**Tasks**:
- Create `pnpm-workspace.yaml` in root
- Set up root `package.json` with workspace scripts
- Configure shared TypeScript configs in `packages/config/tsconfig`
- Configure shared ESLint configs in `packages/config/eslint-config`
- Create `apps/` and `packages/` directories

**Files to create**:
```
pnpm-workspace.yaml
package.json
packages/config/tsconfig/base.json
packages/config/eslint-config/index.js
.gitignore
```

**Deliverables**:
- Working pnpm workspace
- Shared configuration packages
- Root-level scripts (dev, build, lint, type-check)

---

### 1.2 Setup Next.js Frontend (apps/web)

**Goal**: Initialize Next.js 15 application with shadcn/ui

**Tasks**:
- Run `pnpm create next-app` in apps/web
- Configure Next.js 15 with App Router
- Install and initialize shadcn/ui (`npx shadcn@latest init`)
- Install initial shadcn components (Button, Card, Input)
- Set up Tailwind CSS with custom theme
- Configure TypeScript with strict mode
- Create basic layout structure (header, main, footer)
- Add a simple landing page with branding

**Files to create**:
```
apps/web/app/layout.tsx
apps/web/app/page.tsx
apps/web/components/layout/header.tsx
apps/web/components/layout/footer.tsx
apps/web/lib/utils.ts
apps/web/components.json (shadcn config)
apps/web/tailwind.config.ts
```

**Dependencies**:
```json
{
  "next": "^15.0.0",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "tailwindcss": "^3.4.0",
  "@radix-ui/react-*": "latest",
  "class-variance-authority": "^0.7.0",
  "clsx": "^2.1.0",
  "tailwind-merge": "^2.2.0"
}
```

**Deliverables**:
- Running Next.js app on http://localhost:3000
- shadcn/ui components working
- Basic layout with header and footer
- Responsive design foundation

---

### 1.3 Setup FastAPI Backend (apps/api)

**Goal**: Create FastAPI application with proper structure

**Tasks**:
- Create `apps/api` directory structure
- Set up Python virtual environment
- Install FastAPI and dependencies
- Create main FastAPI application with CORS
- Add health check endpoint (`GET /health`)
- Add API versioning structure (`/api/v1/`)
- Configure environment variables with `python-dotenv`
- Add `.env.example` file

**Files to create**:
```
apps/api/app/main.py
apps/api/app/__init__.py
apps/api/app/core/config.py
apps/api/app/routers/__init__.py
apps/api/requirements.txt
apps/api/.env.example
apps/api/.gitignore
```

**Dependencies** (requirements.txt):
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
python-dotenv==1.0.1
python-multipart==0.0.12
pydantic==2.9.0
pydantic-settings==2.6.0
```

**Sample main.py**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SkyLaneAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/")
async def root():
    return {"message": "SkyLaneAI API v1"}
```

**Deliverables**:
- Running FastAPI app on http://localhost:8000
- Interactive API docs at http://localhost:8000/docs
- CORS configured for frontend communication

---

### 1.4 Shared Packages

**Goal**: Create shared TypeScript types for frontend-backend communication

**Tasks**:
- Create `packages/types` package
- Add basic types: `Video`, `Detection`, `ApiResponse`
- Configure package.json for proper exports
- Set up TypeScript compilation
- Add to workspace dependencies

**Files to create**:
```
packages/types/package.json
packages/types/tsconfig.json
packages/types/src/index.ts
packages/types/src/video.ts
packages/types/src/detection.ts
packages/types/src/api.ts
```

**Sample types**:
```typescript
// packages/types/src/video.ts
export interface Video {
  id: string;
  filename: string;
  duration: number;
  fps: number;
  resolution: string;
  status: 'uploading' | 'processing' | 'completed' | 'failed';
  uploadedAt: string;
  processedAt?: string;
}

// packages/types/src/detection.ts
export interface Detection {
  id: string;
  videoId: string;
  frameNumber: number;
  timestamp: number;
  hazardType: 'bird' | 'drone' | 'balloon' | 'kite';
  confidence: number;
  bbox: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}

// packages/types/src/api.ts
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}
```

**Deliverables**:
- Shared types package
- Type-safe communication between frontend and backend
- Proper TypeScript compilation

---

### 1.5 Development Environment

**Goal**: Set up seamless development workflow

**Tasks**:
- Add development scripts to root `package.json`
- Configure hot reload for both apps
- Create `.env.example` files for both apps
- Test API calls from frontend to backend
- Add README with setup instructions
- Verify end-to-end communication

**Root package.json scripts**:
```json
{
  "scripts": {
    "dev": "pnpm --parallel --filter web --filter api dev",
    "dev:web": "pnpm --filter web dev",
    "dev:api": "cd apps/api && source venv/bin/activate && uvicorn app.main:app --reload",
    "build": "pnpm --recursive build",
    "lint": "pnpm --recursive lint",
    "type-check": "pnpm --recursive type-check",
    "clean": "pnpm --recursive clean && rm -rf node_modules"
  }
}
```

**Environment variables**:

Frontend (apps/web/.env.local):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Backend (apps/api/.env):
```env
CORS_ORIGINS=http://localhost:3000
UPLOAD_DIR=./storage/videos
RESULTS_DIR=./storage/results
MAX_UPLOAD_SIZE=104857600  # 100MB
```

**Deliverables**:
- Single command to start both apps (`pnpm dev`)
- Environment variables properly configured
- Successful API call from frontend to backend
- Development documentation

---

## Phase 1 Success Criteria

✅ Monorepo structure with pnpm workspace
✅ Next.js frontend running on port 3000
✅ FastAPI backend running on port 8000
✅ Frontend can make API calls to backend
✅ shadcn/ui components working
✅ Shared types package accessible from frontend
✅ Hot reload working for both apps
✅ Clean code structure following best practices

**Estimated time**: 1-2 days

---

## Phase 2: Video Upload & Detection

### 2.1 Backend: Video Upload API

**Goal**: Create endpoint to accept video file uploads

**Tasks**:
- Create `app/routers/videos.py` router
- Implement `POST /api/v1/videos/upload` endpoint
- Add file validation (format: mp4, avi, mov; max size: 100MB)
- Save uploaded file to storage directory
- Generate unique video ID (UUID)
- Return video metadata and upload status
- Add error handling for invalid uploads

**Files to create/modify**:
```
apps/api/app/routers/videos.py
apps/api/app/schemas/video.py (Pydantic models)
apps/api/app/core/storage.py (file operations)
apps/api/storage/videos/ (directory)
```

**Implementation**:
```python
# app/routers/videos.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.video import VideoUploadResponse
import uuid
import os

router = APIRouter(prefix="/api/v1/videos", tags=["videos"])

UPLOAD_DIR = "./storage/videos"
ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov"}
MAX_SIZE = 100 * 1024 * 1024  # 100MB

@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):
    # Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Invalid file format")

    # Generate unique ID
    video_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{video_id}{ext}"

    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        if len(content) > MAX_SIZE:
            raise HTTPException(400, "File too large")
        buffer.write(content)

    return {
        "video_id": video_id,
        "filename": file.filename,
        "status": "uploaded",
        "file_path": file_path
    }
```

**Deliverables**:
- Working upload endpoint
- File validation
- Unique video IDs
- Error handling

---

### 2.2 Backend: Video Processing Service

**Goal**: Extract frames and metadata from uploaded videos

**Tasks**:
- Install OpenCV (`opencv-python`)
- Create `VideoProcessor` service class
- Implement frame extraction at intervals
- Extract video metadata (duration, fps, resolution)
- Save extracted frames temporarily
- Add logging for processing steps

**Files to create**:
```
apps/api/app/services/video_processor.py
apps/api/storage/frames/ (directory)
```

**Implementation**:
```python
# app/services/video_processor.py
import cv2
from pathlib import Path

class VideoProcessor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

    def get_metadata(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0

        return {
            "fps": fps,
            "duration": duration,
            "resolution": f"{width}x{height}",
            "frame_count": frame_count
        }

    def extract_frames(self, interval: int = 5):
        """Extract every Nth frame"""
        frames = []
        frame_idx = 0

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if frame_idx % interval == 0:
                frames.append((frame_idx, frame))

            frame_idx += 1

        self.cap.release()
        return frames
```

**Dependencies to add**:
```
opencv-python==4.10.0.84
numpy==2.1.0
```

**Deliverables**:
- VideoProcessor class
- Frame extraction logic
- Metadata extraction
- OpenCV integration

---

### 2.3 Backend: YOLOv11 Integration (Basic)

**Goal**: Set up YOLOv11 for object detection

**Tasks**:
- Install `ultralytics` package
- Download pre-trained YOLOv11 model (yolo11n.pt)
- Create `DetectionService` class
- Implement single frame inference
- Filter detections by confidence threshold
- Map COCO classes to hazard types (bird, kite)
- Format detection results with bounding boxes

**Files to create**:
```
apps/api/app/services/detection.py
apps/api/app/models/yolo11n.pt (downloaded)
```

**Implementation**:
```python
# app/services/detection.py
from ultralytics import YOLO
import numpy as np

class DetectionService:
    # COCO classes relevant to sky hazards
    HAZARD_CLASSES = {
        14: "bird",
        33: "kite",
        # More classes can be added after custom training
    }

    def __init__(self, model_path: str = "./app/models/yolo11n.pt"):
        self.model = YOLO(model_path)
        self.confidence_threshold = 0.5

    def detect(self, frame: np.ndarray):
        """Run detection on a single frame"""
        results = self.model(frame, conf=self.confidence_threshold)

        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])

                # Only keep relevant classes
                if class_id in self.HAZARD_CLASSES:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()

                    detections.append({
                        "hazard_type": self.HAZARD_CLASSES[class_id],
                        "confidence": float(box.conf[0]),
                        "bbox": {
                            "x": x1,
                            "y": y1,
                            "width": x2 - x1,
                            "height": y2 - y1
                        }
                    })

        return detections
```

**Model download script**:
```python
# scripts/download_model.py
from ultralytics import YOLO

# This will automatically download yolo11n.pt
model = YOLO('yolo11n.pt')
print("Model downloaded successfully!")
```

**Dependencies to add**:
```
ultralytics==8.3.0
torch>=2.0.0
torchvision>=0.15.0
```

**Deliverables**:
- YOLOv11 model downloaded
- DetectionService class
- Single frame inference working
- Confidence filtering

---

### 2.4 Backend: Batch Video Processing

**Goal**: Process entire video and aggregate detections

**Tasks**:
- Create processing pipeline combining VideoProcessor and DetectionService
- Extract frames at intervals (every 5th frame)
- Run batch inference on all frames
- Aggregate detection results with timestamps
- Save results to JSON file
- Add processing status tracking
- Handle errors gracefully

**Files to create/modify**:
```
apps/api/app/services/pipeline.py
apps/api/storage/results/ (directory)
```

**Implementation**:
```python
# app/services/pipeline.py
import json
from pathlib import Path
from app.services.video_processor import VideoProcessor
from app.services.detection import DetectionService

class ProcessingPipeline:
    def __init__(self):
        self.detector = DetectionService()

    async def process_video(self, video_id: str, video_path: str):
        """Process entire video and return detections"""

        # Extract frames and metadata
        processor = VideoProcessor(video_path)
        metadata = processor.get_metadata()
        frames = processor.extract_frames(interval=5)

        # Run detection on each frame
        all_detections = []
        for frame_idx, frame in frames:
            timestamp = frame_idx / metadata["fps"]
            detections = self.detector.detect(frame)

            for detection in detections:
                all_detections.append({
                    "frame_number": frame_idx,
                    "timestamp": round(timestamp, 2),
                    **detection
                })

        # Save results
        results = {
            "video_id": video_id,
            "metadata": metadata,
            "detections": all_detections,
            "total_detections": len(all_detections)
        }

        results_path = f"./storage/results/{video_id}.json"
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)

        return results
```

**Update videos router**:
```python
# Add to app/routers/videos.py
from app.services.pipeline import ProcessingPipeline

pipeline = ProcessingPipeline()

@router.post("/process/{video_id}")
async def process_video(video_id: str):
    # Find video file
    video_path = f"./storage/videos/{video_id}.mp4"  # Handle extensions properly

    # Process video
    results = await pipeline.process_video(video_id, video_path)

    return {
        "success": True,
        "video_id": video_id,
        "status": "completed",
        "total_detections": results["total_detections"]
    }
```

**Deliverables**:
- Complete processing pipeline
- Batch inference
- Results saved to JSON
- Processing status tracking

---

### 2.5 Backend: Results API

**Goal**: Provide endpoints to retrieve video and detection data

**Tasks**:
- Create `GET /api/v1/videos/{video_id}` endpoint
- Create `GET /api/v1/videos/{video_id}/detections` endpoint
- Load and return video metadata
- Load and return detection results from JSON
- Add pagination for detections
- Add filtering by hazard type

**Implementation**:
```python
# Add to app/routers/videos.py

@router.get("/{video_id}")
async def get_video(video_id: str):
    """Get video metadata and status"""
    results_path = f"./storage/results/{video_id}.json"

    if not Path(results_path).exists():
        raise HTTPException(404, "Video not found")

    with open(results_path) as f:
        data = json.load(f)

    return {
        "video_id": video_id,
        "metadata": data["metadata"],
        "total_detections": data["total_detections"],
        "status": "completed"
    }

@router.get("/{video_id}/detections")
async def get_detections(
    video_id: str,
    hazard_type: str = None,
    limit: int = 100,
    offset: int = 0
):
    """Get detection results with filtering"""
    results_path = f"./storage/results/{video_id}.json"

    if not Path(results_path).exists():
        raise HTTPException(404, "Results not found")

    with open(results_path) as f:
        data = json.load(f)

    detections = data["detections"]

    # Filter by hazard type
    if hazard_type:
        detections = [d for d in detections if d["hazard_type"] == hazard_type]

    # Pagination
    paginated = detections[offset:offset + limit]

    return {
        "detections": paginated,
        "total": len(detections),
        "limit": limit,
        "offset": offset
    }
```

**Deliverables**:
- Video metadata endpoint
- Detections endpoint with filtering
- Pagination support
- Error handling

---

### 2.6 Frontend: Video Upload Component

**Goal**: Create UI for uploading videos

**Tasks**:
- Install shadcn components: Button, Card, Progress
- Create `VideoUpload` component with drag-and-drop
- Add file validation (format, size)
- Implement upload progress bar
- Show upload status (uploading, processing, completed)
- Display error messages
- Call backend upload API

**Files to create**:
```
apps/web/components/video-upload.tsx
apps/web/lib/api-client.ts
```

**Implementation**:
```typescript
// components/video-upload.tsx
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface VideoUploadProps {
  onUploadComplete: (videoId: string) => void
}

export function VideoUpload({ onUploadComplete }: VideoUploadProps) {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState("")

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (!selectedFile) return

    // Validate file
    const validTypes = ["video/mp4", "video/avi", "video/quicktime"]
    if (!validTypes.includes(selectedFile.type)) {
      setError("Invalid file format. Please upload MP4, AVI, or MOV.")
      return
    }

    if (selectedFile.size > 100 * 1024 * 1024) {
      setError("File too large. Maximum size is 100MB.")
      return
    }

    setFile(selectedFile)
    setError("")
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    setProgress(0)

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch("http://localhost:8000/api/v1/videos/upload", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) throw new Error("Upload failed")

      const data = await response.json()
      setProgress(100)

      // Trigger processing
      await fetch(`http://localhost:8000/api/v1/videos/process/${data.video_id}`, {
        method: "POST"
      })

      onUploadComplete(data.video_id)
    } catch (err) {
      setError("Upload failed. Please try again.")
    } finally {
      setUploading(false)
    }
  }

  return (
    <Card className="p-6">
      <div className="space-y-4">
        <input
          type="file"
          accept="video/*"
          onChange={handleFileChange}
          className="w-full"
        />

        {file && <p className="text-sm">Selected: {file.name}</p>}

        {error && <p className="text-sm text-red-500">{error}</p>}

        {uploading && <Progress value={progress} />}

        <Button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="w-full"
        >
          {uploading ? "Uploading..." : "Upload & Process"}
        </Button>
      </div>
    </Card>
  )
}
```

**Deliverables**:
- Drag-and-drop upload UI
- File validation
- Progress tracking
- Error handling
- API integration

---

### 2.7 Frontend: Video Player with Detections

**Goal**: Display video with detection overlays

**Tasks**:
- Create `VideoPlayer` component with HTML5 video
- Add playback controls
- Create canvas overlay for bounding boxes
- Sync detections with video timeline
- Color-code boxes by hazard type
- Show labels and confidence scores
- Handle video loading states

**Files to create**:
```
apps/web/components/video-player.tsx
apps/web/components/detection-overlay.tsx
```

**Implementation**:
```typescript
// components/video-player.tsx
"use client"

import { useRef, useEffect, useState } from "react"
import { Detection } from "@repo/types"

interface VideoPlayerProps {
  videoUrl: string
  detections: Detection[]
}

export function VideoPlayer({ videoUrl, detections }: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [currentTime, setCurrentTime] = useState(0)

  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    const handleTimeUpdate = () => {
      setCurrentTime(video.currentTime)
      drawDetections()
    }

    video.addEventListener("timeupdate", handleTimeUpdate)
    return () => video.removeEventListener("timeupdate", handleTimeUpdate)
  }, [detections])

  const drawDetections = () => {
    const canvas = canvasRef.current
    const video = videoRef.current
    if (!canvas || !video) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Get detections for current time
    const currentDetections = detections.filter(
      d => Math.abs(d.timestamp - currentTime) < 0.2
    )

    // Draw bounding boxes
    currentDetections.forEach(detection => {
      const { bbox, hazard_type, confidence } = detection

      // Color by hazard type
      const colors = {
        bird: "#ef4444",
        drone: "#f59e0b",
        balloon: "#3b82f6",
        kite: "#8b5cf6"
      }

      ctx.strokeStyle = colors[hazard_type as keyof typeof colors] || "#fff"
      ctx.lineWidth = 3
      ctx.strokeRect(bbox.x, bbox.y, bbox.width, bbox.height)

      // Draw label
      ctx.fillStyle = ctx.strokeStyle
      ctx.fillRect(bbox.x, bbox.y - 25, 150, 25)
      ctx.fillStyle = "#fff"
      ctx.font = "14px sans-serif"
      ctx.fillText(
        `${hazard_type} ${(confidence * 100).toFixed(0)}%`,
        bbox.x + 5,
        bbox.y - 7
      )
    })
  }

  return (
    <div className="relative">
      <video
        ref={videoRef}
        src={videoUrl}
        controls
        className="w-full"
        onLoadedMetadata={() => {
          const canvas = canvasRef.current
          const video = videoRef.current
          if (canvas && video) {
            canvas.width = video.videoWidth
            canvas.height = video.videoHeight
          }
        }}
      />
      <canvas
        ref={canvasRef}
        className="absolute top-0 left-0 pointer-events-none"
      />
    </div>
  )
}
```

**Deliverables**:
- Video player with controls
- Canvas overlay for detections
- Real-time bounding boxes
- Color-coded hazard types
- Labels with confidence scores

---

### 2.8 Frontend: Results Display

**Goal**: Show detection summary and analytics

**Tasks**:
- Create `ResultsPanel` component
- Show detection summary (total, by type)
- Create detection timeline visualization
- Display frame-by-frame detection list
- Add filtering by hazard type
- Add export button (download JSON)
- Implement responsive design

**Files to create**:
```
apps/web/components/results-panel.tsx
apps/web/components/detection-list.tsx
apps/web/components/detection-summary.tsx
```

**Implementation**:
```typescript
// components/results-panel.tsx
"use client"

import { Detection } from "@repo/types"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface ResultsPanelProps {
  videoId: string
  detections: Detection[]
}

export function ResultsPanel({ videoId, detections }: ResultsPanelProps) {
  const summary = {
    total: detections.length,
    byType: detections.reduce((acc, d) => {
      acc[d.hazard_type] = (acc[d.hazard_type] || 0) + 1
      return acc
    }, {} as Record<string, number>)
  }

  const handleExport = () => {
    const blob = new Blob([JSON.stringify(detections, null, 2)], {
      type: "application/json"
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `detections-${videoId}.json`
    a.click()
  }

  return (
    <div className="space-y-4">
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Detection Summary</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-muted-foreground">Total Detections</p>
            <p className="text-2xl font-bold">{summary.total}</p>
          </div>
          {Object.entries(summary.byType).map(([type, count]) => (
            <div key={type}>
              <p className="text-sm text-muted-foreground capitalize">{type}s</p>
              <p className="text-2xl font-bold">{count}</p>
            </div>
          ))}
        </div>
        <Button onClick={handleExport} className="w-full mt-4">
          Export Results (JSON)
        </Button>
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Detection Timeline</h3>
        <div className="space-y-2">
          {detections.slice(0, 10).map((d, i) => (
            <div key={i} className="flex items-center justify-between text-sm">
              <span>{d.timestamp.toFixed(2)}s</span>
              <span className="capitalize">{d.hazard_type}</span>
              <span>{(d.confidence * 100).toFixed(0)}%</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
```

**Deliverables**:
- Detection summary card
- Timeline visualization
- Detection list with filtering
- Export functionality
- Responsive layout

---

### 2.9 Frontend: Index Page Integration

**Goal**: Create unified single-page interface

**Tasks**:
- Design page layout (upload → processing → results)
- Integrate VideoUpload component
- Add processing status indicator
- Integrate VideoPlayer and ResultsPanel
- Implement state management for flow
- Add loading states and skeletons
- Responsive design for mobile/desktop
- Add branding and instructions

**Files to create/modify**:
```
apps/web/app/page.tsx
```

**Implementation**:
```typescript
// app/page.tsx
"use client"

import { useState, useEffect } from "react"
import { VideoUpload } from "@/components/video-upload"
import { VideoPlayer } from "@/components/video-player"
import { ResultsPanel } from "@/components/results-panel"
import { Card } from "@/components/ui/card"

export default function HomePage() {
  const [videoId, setVideoId] = useState<string | null>(null)
  const [processing, setProcessing] = useState(false)
  const [detections, setDetections] = useState([])
  const [videoUrl, setVideoUrl] = useState("")

  useEffect(() => {
    if (!videoId) return

    setProcessing(true)

    // Poll for results
    const interval = setInterval(async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/v1/videos/${videoId}/detections`
        )
        const data = await response.json()

        if (data.detections.length > 0) {
          setDetections(data.detections)
          setVideoUrl(`http://localhost:8000/storage/videos/${videoId}.mp4`)
          setProcessing(false)
          clearInterval(interval)
        }
      } catch (error) {
        console.error("Error fetching results:", error)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [videoId])

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-2">SkyLaneAI</h1>
          <p className="text-muted-foreground">
            Sky Hazard Detection for Flying Taxis
          </p>
        </div>

        {/* Upload Section */}
        {!videoId && (
          <VideoUpload onUploadComplete={setVideoId} />
        )}

        {/* Processing Status */}
        {processing && (
          <Card className="p-6 text-center">
            <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4" />
            <p>Processing video and detecting hazards...</p>
          </Card>
        )}

        {/* Results */}
        {!processing && detections.length > 0 && (
          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <VideoPlayer videoUrl={videoUrl} detections={detections} />
            </div>
            <div>
              <ResultsPanel videoId={videoId!} detections={detections} />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
```

**Deliverables**:
- Complete single-page interface
- State management for upload → processing → results flow
- Loading states
- Responsive design
- Professional branding

---

### 2.10 Polish & Testing

**Goal**: Ensure production-ready quality

**Tasks**:
- Add loading skeletons for better UX
- Implement error boundaries
- Add toast notifications (shadcn Toast)
- Test with various video formats
- Test with different video sizes
- Handle edge cases (no detections, corrupted video)
- Add request logging in backend
- Optimize performance
- Write basic documentation

**Testing checklist**:
- [ ] Upload MP4 video
- [ ] Upload AVI video
- [ ] Upload MOV video
- [ ] Upload file > 100MB (should fail)
- [ ] Upload non-video file (should fail)
- [ ] Process video with many detections
- [ ] Process video with no detections
- [ ] Test on mobile device
- [ ] Test on tablet
- [ ] Test video playback controls
- [ ] Test detection filtering
- [ ] Test export functionality

**Deliverables**:
- Polished user experience
- Error handling
- Tested with various inputs
- Basic logging
- Documentation updated

---

## Phase 2 Success Criteria

✅ Users can upload videos (MP4, AVI, MOV)
✅ Backend processes videos and detects hazards (birds, kites)
✅ Results display with bounding boxes on video
✅ Detection summary and statistics shown
✅ Users can export detection results as JSON
✅ Responsive design works on all devices
✅ Error handling for edge cases
✅ Loading states provide good UX
✅ Code is well-structured and documented

**Estimated time**: 1-2 weeks

---

## Technology Stack Summary

**Frontend**:
- Next.js 15 (App Router)
- React 19
- TypeScript
- shadcn/ui (Radix UI + Tailwind)
- HTML5 Video + Canvas API

**Backend**:
- FastAPI
- Python 3.11+
- Pydantic v2
- OpenCV (cv2)
- Ultralytics YOLOv11
- PyTorch

**Infrastructure**:
- pnpm (monorepo)
- Local file storage
- JSON file database (temporary)

---

## Next Steps After Phase 2

**Phase 3** (Future):
- Supabase integration (database + storage)
- User authentication
- Video history and dashboard
- Custom YOLOv11 training on sky hazards
- Time-to-Contact (TTC) calculations
- Real-time camera feed support
- Advanced analytics
- Mobile app

---

## Development Timeline

**Week 1**: Phase 1 (Setup)
- Day 1-2: Monorepo, Next.js, FastAPI setup

**Week 2-3**: Phase 2 (Core Features)
- Week 2: Backend (Upload, Processing, Detection)
- Week 3: Frontend (UI Components, Integration)

**Week 4**: Phase 2 (Polish)
- Testing, bug fixes, documentation

**Total**: 3-4 weeks for MVP

---

## Resources & References

**Documentation**:
- Next.js: https://nextjs.org/docs
- FastAPI: https://fastapi.tiangolo.com/
- YOLOv11: https://docs.ultralytics.com/
- shadcn/ui: https://ui.shadcn.com/
- pnpm: https://pnpm.io/

**Tutorials**:
- pnpm workspace: https://pnpm.io/workspaces
- Next.js App Router: https://nextjs.org/docs/app
- FastAPI file uploads: https://fastapi.tiangolo.com/tutorial/request-files/
- YOLOv11 custom training: https://docs.ultralytics.com/modes/train/

---

*Last updated: 2025-10-13*

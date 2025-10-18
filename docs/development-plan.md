# SkyLaneAI v2 - Development Plan

## Overview

This document outlines the development plan for SkyLaneAI v2, broken down into phases:
- **Phase 1**: Project setup with Next.js frontend and FastAPI backend (Foundation)
- **Phase 2**: Live video streaming with WebRTC and real-time detection
- **Phase 3**: Advanced features (database, analytics, custom training)

---

## Phase 1: Project Setup & Foundation ✅ COMPLETED

**Status**: ✅ All tasks completed
**Completion Date**: 2025-10-18

### 1.1 Initialize Monorepo Structure ✅
**Goal**: Set up pnpm workspace with proper configuration

**Completed Tasks**:
- ✅ Created `pnpm-workspace.yaml` in root
- ✅ Set up root `package.json` with workspace scripts
- ✅ Configured shared TypeScript configs in `packages/config/tsconfig`
- ✅ Configured shared ESLint configs in `packages/config/eslint-config`
- ✅ Created `apps/` and `packages/` directories

**Files Created**:
```
✅ pnpm-workspace.yaml
✅ package.json
✅ packages/config/tsconfig/base.json
✅ packages/config/tsconfig/package.json
✅ packages/config/eslint-config/index.js
✅ packages/config/eslint-config/package.json
✅ .gitignore
```

**Deliverables**:
- ✅ Working pnpm workspace
- ✅ Shared configuration packages
- ✅ Root-level scripts (dev, build, lint, type-check)

---

### 1.2 Setup Next.js Frontend (apps/web) ✅

**Goal**: Initialize Next.js 15 application with shadcn/ui

**Completed Tasks**:
- ✅ Ran `pnpm create next-app` in apps/web
- ✅ Configured Next.js 15 with App Router
- ✅ Installed and initialized shadcn/ui
- ✅ Installed shadcn components (Button, Card, Input, Progress)
- ✅ Set up Tailwind CSS with custom theme
- ✅ Configured TypeScript with strict mode
- ✅ Created basic layout structure (header, main, footer)
- ✅ Added landing page with project branding and features

**Files Created**:
```
✅ apps/web/src/app/layout.tsx
✅ apps/web/src/app/page.tsx
✅ apps/web/src/components/layout/header.tsx
✅ apps/web/src/components/layout/footer.tsx
✅ apps/web/src/lib/utils.ts
✅ apps/web/components.json (shadcn config)
✅ apps/web/tailwind.config.ts
✅ apps/web/.env.local
```

**Deliverables**:
- ✅ Running Next.js app on http://localhost:3000
- ✅ shadcn/ui components working
- ✅ Basic layout with header and footer
- ✅ Responsive design foundation
- ✅ Professional landing page

---

### 1.3 Setup FastAPI Backend (apps/api) ✅

**Goal**: Create FastAPI application with proper structure

**Completed Tasks**:
- ✅ Created `apps/api` directory structure
- ✅ Set up Python virtual environment with Python 3.10
- ✅ Installed FastAPI, Uvicorn, and all dependencies
- ✅ Installed YOLOv11 (ultralytics) with PyTorch
- ✅ Created main FastAPI application with CORS
- ✅ Added health check endpoint (`GET /api/v1/health`)
- ✅ Added API versioning structure (`/api/v1/`)
- ✅ Configured environment variables with `python-dotenv`
- ✅ Added `.env.example` file

**Files Created**:
```
✅ apps/api/app/main.py
✅ apps/api/app/__init__.py
✅ apps/api/app/core/config.py
✅ apps/api/app/core/__init__.py
✅ apps/api/app/api/routes.py
✅ apps/api/app/api/__init__.py
✅ apps/api/app/models/schemas.py
✅ apps/api/app/models/__init__.py
✅ apps/api/app/services/detector.py
✅ apps/api/app/services/__init__.py
✅ apps/api/requirements.txt
✅ apps/api/.env.example
✅ apps/api/venv/ (Python virtual environment)
```

**Dependencies Installed**:
```
✅ fastapi==0.115.5
✅ uvicorn[standard]==0.32.1
✅ python-dotenv==1.0.1
✅ python-multipart==0.0.20
✅ pydantic==2.10.3
✅ pydantic-settings==2.6.1
✅ ultralytics==8.3.48 (YOLOv11)
✅ opencv-python==4.10.0.84
✅ numpy==2.1.3
✅ pillow==11.0.0
✅ pytest==8.3.4
✅ pytest-asyncio==0.24.0
✅ httpx==0.28.1
```

**Deliverables**:
- ✅ Running FastAPI app on http://localhost:8000
- ✅ Interactive API docs at http://localhost:8000/docs
- ✅ CORS configured for frontend communication
- ✅ Health check endpoint working

---

### 1.4 Shared Packages ✅

**Goal**: Create shared TypeScript types for frontend-backend communication

**Completed Tasks**:
- ✅ Created `packages/types` package
- ✅ Added types: `Video`, `Detection`, `ApiResponse`, `HealthResponse`
- ✅ Configured package.json for proper exports
- ✅ Set up TypeScript compilation
- ✅ Added to workspace dependencies

**Files Created**:
```
✅ packages/types/package.json
✅ packages/types/tsconfig.json
✅ packages/types/src/index.ts
✅ packages/types/src/video.ts
✅ packages/types/src/detection.ts
✅ packages/types/src/api.ts
```

**Deliverables**:
- ✅ Shared types package
- ✅ Type-safe communication between frontend and backend
- ✅ Proper TypeScript compilation

---

### 1.5 Development Environment ✅

**Goal**: Set up seamless development workflow

**Completed Tasks**:
- ✅ Added development scripts to root `package.json`
- ✅ Configured hot reload for both apps
- ✅ Created `.env.example` and `.env.local` files
- ✅ Tested API health endpoint
- ✅ Verified backend is running and accessible

**Root package.json scripts**:
```json
{
  "scripts": {
    "dev": "pnpm --parallel --filter web --filter api dev",
    "dev:web": "pnpm --filter web dev",
    "dev:api": "cd apps/api && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000",
    "build": "pnpm --recursive build",
    "lint": "pnpm --recursive lint",
    "type-check": "pnpm --recursive type-check",
    "clean": "pnpm --recursive clean && rm -rf node_modules"
  }
}
```

**Note**: The backend uses `uv` (Python package manager) instead of traditional venv activation. This provides faster dependency management and automatic virtual environment handling.

**Environment Variables**:

Frontend (apps/web/.env.local):
```env
✅ NEXT_PUBLIC_API_URL=http://localhost:8000
```

Backend (apps/api/.env.example):
```env
✅ API_TITLE="SkyLaneAI API"
✅ API_VERSION="2.0.0"
✅ CORS_ORIGINS=["http://localhost:3000"]
✅ MODEL_PATH="yolo11n.pt"
✅ CONFIDENCE_THRESHOLD=0.25
```

**Deliverables**:
- ✅ Development scripts ready
- ✅ Environment variables properly configured
- ✅ Backend API tested and working
- ✅ Clean project structure

---

## Phase 1 Success Criteria ✅

✅ Monorepo structure with pnpm workspace
✅ Next.js frontend running on port 3000
✅ FastAPI backend running on port 8000
✅ Backend API health check working
✅ shadcn/ui components installed and working
✅ Shared types package created
✅ Hot reload configured for both apps
✅ Clean code structure following best practices
✅ YOLOv11 and PyTorch installed
✅ Development environment fully configured

**Completion Date**: 2025-10-18
**Time Taken**: ~4 hours

---

## Phase 2: Live Video Streaming & Real-time Detection

**Status**: 🚧 Not Started
**Goal**: Implement live video streaming from webcam/camera with real-time object detection

### Overview
Phase 2 focuses on implementing WebRTC-based live video streaming with real-time YOLOv11 detection. Users will be able to stream video from their camera and see detected hazards in real-time.

---

### 2.1 Backend: WebRTC Video Streaming

**Goal**: Set up WebRTC signaling and video stream handling

**Tasks**:
- [ ] Install `aiortc` for WebRTC support in Python
- [ ] Create WebSocket endpoint for WebRTC signaling
- [ ] Implement video track receiver
- [ ] Set up peer connection handling
- [ ] Add frame buffering for processing

**Files to Create**:
```
apps/api/app/services/video_stream.py
apps/api/app/api/stream_routes.py
apps/api/app/services/webrtc_handler.py
```

**Dependencies to Add**:
```
aiortc==1.6.0
aiohttp==3.9.0
websockets==12.0
```

**Key Implementation**:
- WebSocket endpoint: `ws://localhost:8000/api/v1/stream/ws`
- Handle WebRTC offer/answer exchange
- Receive video frames from browser
- Buffer frames for detection processing

---

### 2.2 Backend: Real-time Detection Pipeline

**Goal**: Process video frames with YOLOv11 in real-time

**Tasks**:
- [ ] Integrate YOLOv11 detector service with video stream
- [ ] Implement frame queue for efficient processing
- [ ] Add frame skipping (process every Nth frame)
- [ ] Optimize detection for low latency
- [ ] Send detection results back to frontend via WebSocket

**Files to Modify/Create**:
```
apps/api/app/services/detector.py (already exists)
apps/api/app/services/stream_processor.py (new)
```

**Key Features**:
- Process frames at configurable FPS (e.g., 10 FPS)
- Skip frames if processing is too slow
- Send detections with bounding boxes to frontend
- Filter detections by confidence threshold

---

### 2.3 Frontend: WebRTC Video Capture

**Goal**: Capture video from user's camera and stream to backend

**Tasks**:
- [ ] Create `VideoCapture` component
- [ ] Request camera permissions
- [ ] Set up WebRTC peer connection
- [ ] Send video stream to backend
- [ ] Handle connection states (connecting, connected, error)

**Files to Create**:
```
apps/web/src/components/video/video-capture.tsx
apps/web/src/lib/webrtc-client.ts
apps/web/src/hooks/use-media-stream.ts
```

**Key Implementation**:
```typescript
// WebRTC setup
const peerConnection = new RTCPeerConnection()
const stream = await navigator.mediaDevices.getUserMedia({ video: true })
peerConnection.addTrack(stream.getVideoTracks()[0])
```

---

### 2.4 Frontend: Real-time Detection Overlay

**Goal**: Display live video with detection bounding boxes

**Tasks**:
- [ ] Create `DetectionOverlay` component
- [ ] Receive detection results via WebSocket
- [ ] Draw bounding boxes on canvas overlay
- [ ] Display labels and confidence scores
- [ ] Color-code by hazard type
- [ ] Add detection counter

**Files to Create**:
```
apps/web/src/components/video/detection-overlay.tsx
apps/web/src/components/video/detection-stats.tsx
```

**Key Features**:
- Canvas overlay synchronized with video
- Real-time bounding box updates
- Smooth animations
- Confidence threshold filter

---

### 2.5 Frontend: Control Panel

**Goal**: Add controls for video stream and detection settings

**Tasks**:
- [ ] Create start/stop stream buttons
- [ ] Add camera selection dropdown
- [ ] Add confidence threshold slider
- [ ] Add FPS selector
- [ ] Show connection status
- [ ] Display detection statistics

**Files to Create**:
```
apps/web/src/components/controls/stream-controls.tsx
apps/web/src/components/controls/detection-settings.tsx
```

**Controls to Implement**:
- Start/Stop Streaming
- Select Camera (front/back/external)
- Confidence Threshold (0.1 - 1.0)
- Processing FPS (5, 10, 15, 30)
- Enable/Disable Detection

---

### 2.6 Integration & Testing

**Goal**: Ensure end-to-end functionality

**Tasks**:
- [ ] Test camera access on different browsers
- [ ] Test WebRTC connection establishment
- [ ] Verify detection results accuracy
- [ ] Test latency and performance
- [ ] Handle edge cases (no camera, connection lost, etc.)
- [ ] Add error handling and user feedback

**Testing Checklist**:
- [ ] Chrome on desktop
- [ ] Firefox on desktop
- [ ] Safari on macOS
- [ ] Mobile browsers (Chrome/Safari)
- [ ] Test with different camera resolutions
- [ ] Test detection on bird videos
- [ ] Measure end-to-end latency

---

## Phase 2 Success Criteria

⬜ User can start/stop video stream from camera
⬜ WebRTC connection established successfully
⬜ Real-time object detection working
⬜ Bounding boxes displayed on live video
⬜ Detection statistics shown (count, FPS)
⬜ Configurable detection settings
⬜ Smooth performance with <500ms latency
⬜ Error handling for camera/connection issues
⬜ Works on major browsers (Chrome, Firefox, Safari)

**Estimated time**: 1-2 weeks

---

## Phase 2 Technical Architecture

### Frontend Flow:
1. User clicks "Start Stream"
2. Request camera permission
3. Establish WebRTC connection
4. Send video stream to backend
5. Receive detection results via WebSocket
6. Display bounding boxes on video

### Backend Flow:
1. Accept WebRTC connection
2. Receive video frames
3. Buffer frames in queue
4. Process every Nth frame with YOLOv11
5. Send detection results back to frontend
6. Handle disconnections gracefully

### Data Flow:
```
[Camera] → [Browser WebRTC] → [FastAPI WebSocket]
    → [Frame Buffer] → [YOLOv11] → [Detections]
    → [WebSocket] → [Frontend Canvas Overlay]
```

---

---

## Phase 3: Advanced Features (Future)

**Status**: 📋 Planned
**Goal**: Add advanced features, analytics, and production readiness

### Potential Features:
- Database integration (PostgreSQL/Supabase)
- User authentication and sessions
- Detection history and analytics dashboard
- Custom YOLOv11 training on sky hazard dataset
- Time-to-Contact (TTC) calculations for collision avoidance
- Video file upload and batch processing (optional)
- Export detection data (CSV, JSON)
- Advanced visualization (heatmaps, trajectories)
- Multi-camera support
- Mobile app (React Native)
- Deployment (Docker, cloud hosting)

**Estimated time**: Ongoing development

---

## Development Timeline

### Actual Timeline:
**Phase 1** (Completed): 2025-10-18 (~4 hours)
- ✅ Monorepo setup with pnpm
- ✅ Next.js 15 + shadcn/ui frontend
- ✅ FastAPI + YOLOv11 backend
- ✅ Shared types package
- ✅ Development environment

**Phase 2** (Planned): 1-2 weeks
- Week 1: WebRTC streaming, real-time detection backend
- Week 2: Frontend video capture, detection overlay, controls
- Testing and optimization

**Phase 3** (Future): Ongoing
- Advanced features as needed

---

## Resources & References

**Documentation**:
- Next.js: https://nextjs.org/docs
- FastAPI: https://fastapi.tiangolo.com/
- YOLOv11: https://docs.ultralytics.com/
- shadcn/ui: https://ui.shadcn.com/
- pnpm: https://pnpm.io/
- WebRTC: https://webrtc.org/
- aiortc (Python WebRTC): https://aiortc.readthedocs.io/

**Tutorials**:
- pnpm workspace: https://pnpm.io/workspaces
- Next.js App Router: https://nextjs.org/docs/app
- FastAPI WebSockets: https://fastapi.tiangolo.com/advanced/websockets/
- YOLOv11 custom training: https://docs.ultralytics.com/modes/train/
- WebRTC basics: https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API

---

## How to Run

### First Time Setup:
```bash
# Clone repository
git clone <repository-url>
cd SkylaneAI-v2

# Install frontend dependencies
pnpm install

# Setup Python backend (using uv)
# Install uv if you don't have it: curl -LsSf https://astral.sh/uv/install.sh | sh
cd apps/api
uv sync  # Automatically creates venv and installs dependencies
cd ../..
```

### Development:
```bash
# Option 1: Run both (frontend + backend) in parallel
pnpm dev

# Option 2: Run separately

# Terminal 1: Start Backend (using uv)
pnpm dev:api

# Terminal 2: Start Frontend
pnpm dev:web
```

### Alternative (Traditional venv):
```bash
# If you prefer traditional venv instead of uv
cd apps/api
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/v1/health

---

*Last updated: 2025-10-18*

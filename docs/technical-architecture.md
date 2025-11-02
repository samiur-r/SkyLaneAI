# SkyLaneAI v2 - Technical Architecture

**Last Updated**: 2025-11-02

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Diagram](#architecture-diagram)
4. [Backend Implementation](#backend-implementation)
5. [Frontend Implementation](#frontend-implementation)
6. [Data Flow](#data-flow)
7. [WebRTC Communication](#webrtc-communication)
8. [Real-time Detection Pipeline](#real-time-detection-pipeline)
9. [API Reference](#api-reference)
10. [Configuration](#configuration)
11. [Performance Optimization](#performance-optimization)
12. [Video Upload and Processing](#video-upload-and-processing)
13. [AI-Powered Alert Generation System](#ai-powered-alert-generation-system)

---

## System Overview

SkyLaneAI v2 is a real-time object detection system designed for aviation safety. It uses:
- **WebRTC** for low-latency video streaming from browser to server
- **YOLOv11** for real-time object detection
- **WebSocket** for bidirectional communication
- **Next.js 15** for the frontend
- **FastAPI** for the backend

### Core Features
- Live camera streaming from browser to server
- Real-time object detection (birds, drones, aircraft)
- Configurable detection settings (FPS, confidence threshold)
- Low-latency processing (<500ms target)
- Detection overlay with bounding boxes

---

## Implementation Summary

### ✅ What Has Been Built

**Phase 1: Foundation (Completed)**
- Monorepo setup with pnpm workspace
- Next.js 15 frontend with shadcn/ui
- FastAPI backend with YOLOv11
- Shared TypeScript types package

**Phase 2: Live Streaming & Detection (Completed)**

#### Backend (100% Complete)
1. **WebRTC Handler** - Manages video connections from browser
2. **Video Stream Processor** - Processes video frames at configurable FPS
3. **YOLO Detector** - Runs object detection on frames
4. **WebSocket API** - Real-time bidirectional communication

#### Frontend (100% Complete)
1. **WebRTC Client** - Connects to backend and streams video
2. **Video Components**:
   - `VideoCapture` - Shows live camera feed
   - `DetectionOverlay` - Draws bounding boxes on video
   - `DetectionStats` - Shows real-time statistics
3. **Control Components**:
   - `StreamControls` - Start/stop, camera selection
   - `DetectionSettings` - FPS, confidence threshold
4. **React Hooks**:
   - `useMediaStream` - Camera access and device management
   - `useWebRTC` - WebRTC connection management
   - `useDetections` - Detection results handling

### 📁 Files Created

**Backend:**
```
apps/api/app/
├── services/
│   ├── video_stream.py        ✅ Video processing pipeline
│   ├── webrtc_handler.py      ✅ WebRTC connection manager
│   └── detector.py            ✅ YOLO detector
└── api/
    └── stream_routes.py        ✅ WebSocket endpoints
```

**Frontend:**
```
apps/web/src/
├── lib/
│   └── webrtc-client.ts       ✅ WebRTC client
├── hooks/
│   ├── use-media-stream.ts    ✅ Camera access hook
│   ├── use-webrtc.ts          ✅ WebRTC hook
│   └── use-detections.ts      ✅ Detections hook
├── components/
│   ├── video/
│   │   ├── video-capture.tsx      ✅ Video display
│   │   ├── detection-overlay.tsx  ✅ Bounding boxes
│   │   └── detection-stats.tsx    ✅ Statistics
│   └── controls/
│       ├── stream-controls.tsx    ✅ Stream controls
│       └── detection-settings.tsx ✅ Settings panel
└── app/
    └── stream/
        └── page.tsx           ✅ Main stream page
```

**Shared:**
```
packages/types/src/
└── stream.ts                  ✅ WebRTC & stream types
```

---

## Complete End-to-End Flow (Simple Explanation)

### Overview
This section explains how the entire system works from start to finish in simple terms.

### Step 1: User Opens the Application

**What happens:**
- User visits `http://localhost:3000` (home page)
- Clicks "Start Live Detection" button
- Browser navigates to `/stream` page

**Behind the scenes:**
- Next.js loads the stream page
- React components initialize
- No camera or connections active yet

---

### Step 2: User Clicks "Start Stream"

**What the user sees:**
- Camera selection dropdown appears
- "Start Stream" button becomes active

**What happens:**
1. Browser requests list of available cameras
2. System displays camera options (front camera, back camera, external)
3. User selects a camera
4. User clicks "Start Stream"

**Behind the scenes:**
```typescript
// useMediaStream hook is called
navigator.mediaDevices.getUserMedia({ video: true })
```

---

### Step 3: Camera Permission Request

**What the user sees:**
- Browser shows permission popup: "Allow access to camera?"
- User clicks "Allow"

**What happens:**
- Browser requests camera access from the operating system
- If granted: Camera stream starts
- If denied: Error message shown

**Behind the scenes:**
```typescript
// If permission granted:
stream = MediaStream { videoTrack, audioTrack }

// If permission denied:
error = "Camera access denied. Please grant permissions."
```

---

### Step 4: Camera Starts Streaming

**What the user sees:**
- Live camera feed appears in the video player
- Connection status changes to "Connecting..."

**What happens:**
1. Video element displays the camera feed
2. WebSocket connects to backend server
3. WebRTC peer connection is created

**Behind the scenes:**
```typescript
// 1. Show video
videoElement.srcObject = stream

// 2. Connect WebSocket
websocket = new WebSocket('ws://localhost:8000/api/v1/stream/ws')

// 3. Create WebRTC connection
peerConnection = new RTCPeerConnection()
peerConnection.addTrack(stream.getVideoTracks()[0])
```

---

### Step 5: WebRTC Handshake (Connection Setup)

**What the user sees:**
- Status shows "Connecting..."
- Video is visible but no detections yet

**What happens (simplified):**
1. **Browser creates an "offer"** - "Hey server, I want to send you video"
2. **Server receives offer** - "OK, I'm ready to receive"
3. **Server creates an "answer"** - "Here's how to connect to me"
4. **Browser receives answer** - "Got it, connecting now"
5. **Connection established** - Video frames start flowing

**Behind the scenes (technical):**
```
Browser                          Server
  │                                │
  ├─── Offer (SDP) ───────────────▶│  "I want to send video"
  │                                │
  │◀── Answer (SDP) ───────────────┤  "Here's how to connect"
  │                                │
  ├─── ICE Candidates ───────────▶│  Network path negotiation
  │◀─── ICE Candidates ───────────┤
  │                                │
  │════ Connection Active ════════│  Video streaming starts
```

---

### Step 6: Video Frames Flow to Server

**What the user sees:**
- Status changes to "Connected"
- Video continues playing smoothly

**What happens:**
- Browser captures video at 30 frames per second (FPS)
- Each frame is sent to the server via WebRTC
- Server receives frames continuously

**Behind the scenes:**
```
Browser:
  Camera → 30 FPS → WebRTC → Internet → Server

Server (video_stream.py):
  Receives frame → Add to queue → Wait for processing
```

**Frame rate example:**
- Camera: 30 frames/second (one frame every 33ms)
- Server receives all 30 frames but only processes 10/second

---

### Step 7: Server Processes Frames

**What the user sees:**
- Processing statistics update in real-time
- Numbers like "Frames Processed: 150"

**What happens:**

**Stage 1: Frame Reception**
- Server receives frame from WebRTC
- Frame is raw video data (pixels)

**Stage 2: Frame Buffering**
- Frame added to a queue (like a waiting line)
- Queue holds max 30 frames
- If full, oldest frame is removed

**Stage 3: FPS Control**
- Server checks: "Has 100ms passed since last processing?"
- If yes → Process this frame
- If no → Skip and wait

**Stage 4: Frame Skipping** (optional)
- If queue has too many frames → Skip some
- Prevents system from getting overwhelmed
- Keeps latency low

**Stage 5: Frame Conversion**
- Convert frame to format YOLO understands
- Raw pixels → NumPy array (RGB image)

**Behind the scenes:**
```python
# Simplified processing loop
while streaming:
    # Get frame from queue
    frame = frame_queue.pop()

    # Check if enough time passed (100ms for 10 FPS)
    if time_since_last_process < 0.1:
        continue  # Skip

    # Convert frame
    image = convert_to_numpy(frame)

    # Run YOLO detection (next step)
    detections = yolo.detect(image)
```

---

### Step 8: YOLO Detection Runs

**What the user sees:**
- Nothing yet - processing happens in background

**What happens:**
1. **Frame enters YOLO model** - Image goes into neural network
2. **Model analyzes image** - Looks for objects (birds, drones, etc.)
3. **Model outputs detections** - List of found objects with locations
4. **Filtering** - Remove detections below confidence threshold (25%)

**Behind the scenes:**
```python
# Run YOLO inference
results = yolo_model(image)

# Example output:
detections = [
    {
        "class_name": "bird",
        "confidence": 0.87,  # 87% confident
        "bbox": { "x1": 100, "y1": 200, "x2": 300, "y2": 400 }
    },
    {
        "class_name": "drone",
        "confidence": 0.15,  # Too low - filtered out
        "bbox": { ... }
    }
]

# Filter by confidence
filtered = [d for d in detections if d.confidence >= 0.25]
# Result: Only bird (87%) is kept
```

**Processing time:**
- Typical: 40-80ms per frame
- Fast enough for real-time (10 FPS = 100ms between frames)

---

### Step 9: Detection Results Sent to Browser

**What happens:**
1. Server formats detection results as JSON
2. Sends via WebSocket to browser
3. Browser receives detection data

**Behind the scenes:**
```python
# Server sends:
websocket.send_json({
    "type": "detection",
    "data": {
        "frame_number": 123,
        "timestamp": 1697654321.123,
        "detections": [
            {
                "class_name": "bird",
                "class_id": 14,
                "confidence": 0.87,
                "bbox": { "x1": 100, "y1": 200, "x2": 300, "y2": 400 }
            }
        ],
        "processing_time_ms": 45.2,
        "stats": {
            "frames_received": 500,
            "frames_processed": 200,
            "frames_skipped": 300
        }
    }
})
```

```typescript
// Browser receives:
websocket.onmessage = (event) => {
    const message = JSON.parse(event.data)
    if (message.type === 'detection') {
        updateDetections(message.data.detections)
    }
}
```

---

### Step 10: Browser Draws Bounding Boxes

**What the user sees:**
- Red box appears around detected bird
- Label shows "bird 87%"
- Box moves as bird moves in video

**What happens:**

**Step 1: Receive Detection**
```typescript
// New detection arrives
detection = {
    className: "bird",
    confidence: 0.87,
    bbox: { x1: 100, y1: 200, x2: 300, y2: 400 },
    color: "#ef4444" // Red
}
```

**Step 2: Update React State**
```typescript
setDetections([detection])  // Triggers re-render
```

**Step 3: Canvas Draws Box**
```typescript
// DetectionOverlay component
const canvas = canvasRef.current
const ctx = canvas.getContext('2d')

// Match canvas size to video
canvas.width = video.videoWidth   // e.g., 1280
canvas.height = video.videoHeight // e.g., 720

// Draw bounding box
ctx.strokeStyle = "#ef4444"  // Red color
ctx.lineWidth = 3
ctx.strokeRect(
    100,  // x1
    200,  // y1
    200,  // width (x2 - x1)
    200   // height (y2 - y1)
)

// Draw label "bird 87%"
ctx.fillStyle = "#ef4444"
ctx.fillRect(100, 176, 80, 24)  // Background
ctx.fillStyle = "#ffffff"
ctx.fillText("bird 87%", 106, 188)  // Text
```

**Step 4: Smooth Animation**
- Uses `requestAnimationFrame()` for 60 FPS rendering
- Redraws canvas every time new detection arrives
- Old boxes automatically cleared

---

### Step 11: Real-Time Updates

**What the user sees:**
- Boxes continuously update as objects move
- Statistics update every second
- Everything happens smoothly

**What happens (continuous loop):**

```
Every 100ms (10 times per second):
  ┌─────────────────────────────────────┐
  │ 1. Camera captures frame            │
  │ 2. Browser sends to server          │
  │ 3. Server processes with YOLO       │
  │ 4. Server sends detection results   │
  │ 5. Browser draws bounding boxes     │
  │ 6. User sees updated video + boxes  │
  └─────────────────────────────────────┘

Every second:
  - Statistics update (FPS, latency, counts)
  - Connection health check (ping/pong)
```

---

### Step 12: User Adjusts Settings

**What the user can do:**
1. **Change FPS** (5, 10, 15, 20, 30)
2. **Adjust confidence threshold** (10% to 100%)
3. **Toggle frame skipping** (on/off)
4. **Switch camera** (front/back/external)

**Example: User changes FPS from 10 to 15**

**What happens:**
```typescript
// User moves slider to 15 FPS
onFpsChange(15)

// Frontend sends to backend
websocket.send({
    type: "settings",
    fps: 15,
    skip_frames: true
})

// Backend updates processing
processor.update_settings(fps=15)

// Now processes 15 frames/second instead of 10
```

**Example: User lowers confidence to 15%**

**What happens:**
```typescript
// User adjusts slider to 0.15
onConfidenceChange(0.15)

// More detections shown (lower threshold)
// Before: Only 87% confident detections
// After: Shows 87%, 52%, 33%, 19% detections
```

---

### Step 13: User Stops Stream

**What the user sees:**
- Clicks "Stop Stream" button
- Video feed stops
- Bounding boxes disappear
- Status shows "Disconnected"

**What happens:**
1. Camera stream stops
2. WebRTC connection closes
3. WebSocket disconnects
4. Detections cleared

**Behind the scenes:**
```typescript
// Stop camera
stream.getTracks().forEach(track => track.stop())

// Close WebRTC
peerConnection.close()

// Close WebSocket
websocket.close()

// Clear UI
setDetections([])
setStats(null)
```

---

## Summary: Complete Data Flow

### Quick Reference

```
USER ACTION → BROWSER → WEBRTC → SERVER → YOLO → BROWSER → DISPLAY

Detailed:
┌─────────┐
│ 1. User │ Clicks "Start Stream"
└────┬────┘
     ▼
┌──────────┐
│ 2. Camera│ Captures video @ 30 FPS
└────┬─────┘
     ▼
┌──────────────┐
│ 3. Browser   │ Sends frames via WebRTC
└──────┬───────┘
       ▼
┌──────────────┐
│ 4. Server    │ Receives frames, adds to queue
└──────┬───────┘
       ▼
┌──────────────┐
│ 5. Processor │ Processes @ 10 FPS, skips extras
└──────┬───────┘
       ▼
┌──────────────┐
│ 6. YOLO      │ Detects objects (40-80ms)
└──────┬───────┘
       ▼
┌──────────────┐
│ 7. Filter    │ Removes low confidence (<25%)
└──────┬───────┘
       ▼
┌──────────────┐
│ 8. WebSocket │ Sends detections to browser
└──────┬───────┘
       ▼
┌──────────────┐
│ 9. Browser   │ Updates React state
└──────┬───────┘
       ▼
┌──────────────┐
│ 10. Canvas   │ Draws bounding boxes
└──────┬───────┘
       ▼
┌──────────────┐
│ 11. User     │ Sees live video with detections!
└──────────────┘
```

### Timing Breakdown

| Step | Process | Time |
|------|---------|------|
| 1 | Camera capture | 33ms (30 FPS) |
| 2 | WebRTC send | 10-20ms |
| 3 | Server receive | <1ms |
| 4 | Queue wait | Variable |
| 5 | YOLO detection | 40-80ms |
| 6 | Filter results | <1ms |
| 7 | WebSocket send | 10-20ms |
| 8 | Browser receive | <1ms |
| 9 | Canvas render | 16ms (60 FPS) |
| **Total** | **End-to-end** | **~150-250ms** |

**Result**: Less than 500ms latency ✅ (Target achieved!)

---

## Technology Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **UI Library**: shadcn/ui + Tailwind CSS
- **Language**: TypeScript
- **Video**: WebRTC (browser native APIs)
- **State Management**: React hooks
- **Package Manager**: pnpm (workspace)

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **WebRTC**: aiortc (1.13.0)
- **Object Detection**: YOLOv11 (ultralytics 8.3.48)
- **Computer Vision**: OpenCV (4.10.0)
- **WebSocket**: FastAPI WebSocket + websockets
- **Package Manager**: uv (modern Python package manager)

### Shared
- **Monorepo**: pnpm workspace
- **Types**: Shared TypeScript types package
- **Communication**: WebSocket + WebRTC data channels

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         BROWSER (Frontend)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐        ┌──────────────────┐               │
│  │   User Camera   │───────▶│  Video Element   │               │
│  └─────────────────┘        └──────────────────┘               │
│                                      │                           │
│                                      ▼                           │
│                          ┌──────────────────────┐               │
│                          │  WebRTC Connection   │               │
│                          │  (RTCPeerConnection) │               │
│                          └──────────────────────┘               │
│                                      │                           │
│                                      ▼                           │
│                          ┌──────────────────────┐               │
│                          │  WebSocket Client    │               │
│                          │  (Signaling + Data)  │               │
│                          └──────────────────────┘               │
│                                      │                           │
│                              ┌───────┴────────┐                 │
│                              ▼                ▼                  │
│                    ┌──────────────┐  ┌──────────────┐          │
│                    │  Send Video  │  │   Receive    │          │
│                    │   Frames     │  │  Detections  │          │
│                    └──────────────┘  └──────────────┘          │
│                                              │                   │
│                                              ▼                   │
│                                   ┌─────────────────┐           │
│                                   │ Canvas Overlay  │           │
│                                   │ (Bounding Boxes)│           │
│                                   └─────────────────┘           │
│                                                                   │
└───────────────────────────────────┬─────────────────────────────┘
                                    │
                        WebSocket + WebRTC
                                    │
┌───────────────────────────────────▼─────────────────────────────┐
│                      BACKEND (FastAPI Server)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                    ┌──────────────────────┐                     │
│                    │  WebSocket Endpoint  │                     │
│                    │  /api/v1/stream/ws   │                     │
│                    └──────────────────────┘                     │
│                             │                                    │
│                             ▼                                    │
│                ┌────────────────────────────┐                   │
│                │ WebRTCConnectionHandler    │                   │
│                │ - Manage peer connection   │                   │
│                │ - Handle signaling         │                   │
│                │ - Create video track       │                   │
│                └────────────────────────────┘                   │
│                             │                                    │
│                             ▼                                    │
│                ┌────────────────────────────┐                   │
│                │   VideoTransformTrack      │                   │
│                │ - Receive video frames     │                   │
│                │ - Extract frame data       │                   │
│                └────────────────────────────┘                   │
│                             │                                    │
│                             ▼                                    │
│                ┌────────────────────────────┐                   │
│                │   VideoStreamProcessor     │                   │
│                │ - Frame queue (deque)      │                   │
│                │ - FPS control              │                   │
│                │ - Frame skipping           │                   │
│                └────────────────────────────┘                   │
│                             │                                    │
│                             ▼                                    │
│                ┌────────────────────────────┐                   │
│                │    YOLOv11 Detector        │                   │
│                │ - Load model (yolo11n.pt)  │                   │
│                │ - Run inference            │                   │
│                │ - Filter by confidence     │                   │
│                └────────────────────────────┘                   │
│                             │                                    │
│                             ▼                                    │
│                ┌────────────────────────────┐                   │
│                │    Detection Results       │                   │
│                │ - Bounding boxes           │                   │
│                │ - Class labels             │                   │
│                │ - Confidence scores        │                   │
│                └────────────────────────────┘                   │
│                             │                                    │
│                             ▼                                    │
│                    Send via WebSocket                            │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Backend Implementation

### Directory Structure

```
apps/api/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── core/
│   │   ├── config.py              # Configuration settings
│   │   └── __init__.py
│   ├── api/
│   │   ├── routes.py              # REST API routes (health check)
│   │   ├── stream_routes.py      # WebRTC/WebSocket routes
│   │   └── __init__.py
│   ├── services/
│   │   ├── detector.py            # YOLOv11 detection service
│   │   ├── video_stream.py        # Video stream processing
│   │   ├── webrtc_handler.py      # WebRTC connection handler
│   │   └── __init__.py
│   └── models/
│       ├── schemas.py             # Pydantic models
│       └── __init__.py
├── requirements.txt
├── .env.example
└── .env
```

### Key Components

#### 1. WebRTC Connection Handler ([webrtc_handler.py](apps/api/app/services/webrtc_handler.py))

**Purpose**: Manages WebRTC peer connections and signaling

```python
class WebRTCConnectionHandler:
    """
    Handles WebRTC peer connection lifecycle:
    - Create RTCPeerConnection
    - Handle SDP offer/answer exchange
    - Manage ICE candidates
    - Add video track receiver
    - Handle connection state changes
    """
```

**Key Methods**:
- `handle_offer(sdp)`: Process WebRTC offer from client
- `handle_ice_candidate(candidate)`: Process ICE candidates
- `add_video_processor(processor)`: Attach video stream processor
- `close()`: Clean up connection

**How it works**:
1. Client sends WebRTC offer (SDP)
2. Handler creates RTCPeerConnection
3. Handler sets remote description (offer)
4. Handler creates answer (SDP)
5. Handler adds video track to receive frames
6. Connection established via ICE candidates

---

#### 2. Video Stream Processor ([video_stream.py](apps/api/app/services/video_stream.py))

**Purpose**: Process video frames with YOLO detection at configurable FPS

```python
class VideoStreamProcessor:
    """
    Manages frame processing pipeline:
    - Frame buffering (deque, max 30 frames)
    - FPS control (default: 10 FPS)
    - Frame skipping (optional)
    - Async YOLO detection
    - Statistics tracking
    """
```

**Key Methods**:
- `add_frame(frame)`: Add frame to processing queue
- `process_frames()`: Main processing loop (async)
- `update_settings(fps, skip_frames)`: Dynamic configuration
- `get_stats()`: Return processing statistics

**Processing Flow**:
1. Receive frame from WebRTC track
2. Add to deque buffer (FIFO, max 30)
3. Check FPS timing (e.g., process every 100ms for 10 FPS)
4. Skip frames if enabled and queue is full
5. Convert frame to numpy array
6. Run YOLO detection (async)
7. Send results via WebSocket

**Performance Features**:
- **Frame skipping**: Drop frames if processing is slow
- **Async processing**: Use `asyncio.to_thread()` for CPU-bound YOLO
- **Frame buffer**: Prevent memory overflow with max queue size
- **FPS control**: Adjustable processing rate (5-30 FPS)
- **Statistics**: Track frames received, processed, skipped

---

#### 3. YOLO Detector Service ([detector.py](apps/api/app/services/detector.py))

**Purpose**: YOLOv11 model wrapper for object detection

```python
class YOLODetector:
    """
    YOLOv11 detection service:
    - Load model (yolo11n.pt)
    - Run inference on frames
    - Filter by confidence threshold
    - Return bounding boxes and labels
    """
```

**Key Methods**:
- `detect(frame)`: Run detection on single frame
- `detect_batch(frames)`: Batch processing (future optimization)

**Detection Output**:
```python
{
    "detections": [
        {
            "class_name": "bird",
            "class_id": 14,
            "confidence": 0.87,
            "bbox": {
                "x1": 100,
                "y1": 200,
                "x2": 300,
                "y2": 400
            }
        }
    ],
    "processing_time_ms": 45.2
}
```

---

#### 4. WebSocket Stream Endpoint ([stream_routes.py](apps/api/app/api/stream_routes.py))

**Endpoint**: `ws://localhost:8000/api/v1/stream/ws`

**Message Types** (Client → Server):

1. **offer** - WebRTC offer (SDP)
```json
{
  "type": "offer",
  "sdp": "v=0\r\no=- ..."
}
```

2. **ice_candidate** - ICE candidate
```json
{
  "type": "ice_candidate",
  "candidate": "candidate:..."
}
```

3. **settings** - Update processing settings
```json
{
  "type": "settings",
  "fps": 15,
  "skip_frames": true
}
```

4. **get_stats** - Request statistics
```json
{
  "type": "get_stats"
}
```

5. **ping** - Keep-alive
```json
{
  "type": "ping"
}
```

**Message Types** (Server → Client):

1. **answer** - WebRTC answer (SDP)
```json
{
  "type": "answer",
  "sdp": "v=0\r\no=- ..."
}
```

2. **detection** - Detection results
```json
{
  "type": "detection",
  "data": {
    "frame_number": 123,
    "timestamp": 1234567890.123,
    "detections": [...],
    "processing_time_ms": 45.2,
    "stats": {...}
  }
}
```

3. **stats** - Processing statistics
```json
{
  "type": "stats",
  "data": {
    "frames_received": 500,
    "frames_processed": 200,
    "frames_skipped": 300,
    "avg_processing_time": 42.5
  }
}
```

4. **error** - Error message
```json
{
  "type": "error",
  "message": "Connection failed"
}
```

5. **pong** - Keep-alive response
```json
{
  "type": "pong"
}
```

---

### Backend Configuration ([config.py](apps/api/app/core/config.py))

```python
class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "SkyLaneAI API"
    API_VERSION: str = "2.0.0"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # YOLO Model Configuration
    MODEL_PATH: str = "yolo11n.pt"
    CONFIDENCE_THRESHOLD: float = 0.25

    # Video Stream Configuration
    STREAM_FPS: int = 10
    STREAM_SKIP_FRAMES: bool = True
    STREAM_MAX_QUEUE_SIZE: int = 30
```

**Environment Variables** (`.env`):
```env
MODEL_PATH=yolo11n.pt
CONFIDENCE_THRESHOLD=0.25
STREAM_FPS=10
STREAM_SKIP_FRAMES=true
STREAM_MAX_QUEUE_SIZE=30
```

---

## Frontend Implementation

### Directory Structure (To Be Created)

```
apps/web/src/
├── app/
│   ├── page.tsx                   # Landing page
│   └── stream/
│       └── page.tsx               # Live stream page
├── components/
│   ├── video/
│   │   ├── video-capture.tsx      # Camera capture + WebRTC
│   │   ├── detection-overlay.tsx  # Canvas overlay with bounding boxes
│   │   └── detection-stats.tsx    # Statistics display
│   ├── controls/
│   │   ├── stream-controls.tsx    # Start/stop, camera selection
│   │   └── detection-settings.tsx # FPS, confidence threshold
│   └── ui/                        # shadcn/ui components
├── lib/
│   ├── webrtc-client.ts           # WebRTC client wrapper
│   └── websocket-client.ts        # WebSocket client wrapper
└── hooks/
    ├── use-media-stream.ts        # Camera access hook
    ├── use-webrtc.ts              # WebRTC connection hook
    └── use-detections.ts          # Detection results hook
```

### Key Components (To Be Implemented)

#### 1. WebRTC Client ([webrtc-client.ts](apps/web/src/lib/webrtc-client.ts))

**Purpose**: Manage WebRTC peer connection on client side

```typescript
class WebRTCClient {
  private peerConnection: RTCPeerConnection
  private websocket: WebSocket

  async connect(wsUrl: string): Promise<void>
  async addVideoTrack(stream: MediaStream): Promise<void>
  async createOffer(): Promise<RTCSessionDescriptionInit>
  async handleAnswer(answer: RTCSessionDescriptionInit): Promise<void>
  onDetection(callback: (detection: Detection) => void): void
  disconnect(): void
}
```

**How it works**:
1. Create `RTCPeerConnection`
2. Connect WebSocket to backend
3. Add local video track from camera
4. Create and send WebRTC offer
5. Receive and set answer
6. Listen for detection results

---

#### 2. Video Capture Component ([video-capture.tsx](apps/web/src/components/video/video-capture.tsx))

**Purpose**: Display live camera feed

```typescript
export function VideoCapture() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const { stream, error, requestCamera } = useMediaStream()

  // Display camera stream in video element
  // Handle permissions
  // Show loading/error states
}
```

**Features**:
- Request camera permission
- Display live video feed
- Camera selection (front/back/external)
- Error handling

---

#### 3. Detection Overlay Component ([detection-overlay.tsx](apps/web/src/components/video/detection-overlay.tsx))

**Purpose**: Draw bounding boxes on canvas over video

```typescript
export function DetectionOverlay({ detections, videoRef }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const video = videoRef.current

    // Sync canvas size with video
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    // Draw bounding boxes
    drawDetections(canvas, detections)
  }, [detections])
}
```

**Features**:
- Canvas overlay synchronized with video
- Draw bounding boxes with labels
- Color-coded by class (birds=red, drones=yellow, aircraft=blue)
- Display confidence scores
- Smooth animations

---

#### 4. Stream Controls ([stream-controls.tsx](apps/web/src/components/controls/stream-controls.tsx))

**Purpose**: Control video streaming

```typescript
export function StreamControls() {
  return (
    <div>
      <Button onClick={startStream}>Start Stream</Button>
      <Button onClick={stopStream}>Stop Stream</Button>
      <Select onChange={selectCamera}>
        <option>Front Camera</option>
        <option>Back Camera</option>
      </Select>
      <Badge>Status: {connectionStatus}</Badge>
    </div>
  )
}
```

---

#### 5. Detection Settings ([detection-settings.tsx](apps/web/src/components/controls/detection-settings.tsx))

**Purpose**: Configure detection parameters

```typescript
export function DetectionSettings() {
  return (
    <div>
      <Label>Confidence Threshold</Label>
      <Slider
        min={0.1}
        max={1.0}
        step={0.05}
        value={threshold}
        onChange={updateThreshold}
      />

      <Label>Processing FPS</Label>
      <Select value={fps} onChange={updateFPS}>
        <option value={5}>5 FPS</option>
        <option value={10}>10 FPS</option>
        <option value={15}>15 FPS</option>
        <option value={30}>30 FPS</option>
      </Select>
    </div>
  )
}
```

---

## Data Flow

### Complete Flow: Camera to Detection Overlay

```
1. USER INTERACTION
   ↓
   [User clicks "Start Stream"]
   ↓
2. CAMERA ACCESS
   ↓
   navigator.mediaDevices.getUserMedia({ video: true })
   ↓
   [MediaStream with video track]
   ↓
3. WEBRTC CONNECTION
   ↓
   WebSocket connect to ws://localhost:8000/api/v1/stream/ws
   ↓
   Create RTCPeerConnection
   ↓
   Add video track to peer connection
   ↓
   Create WebRTC offer (SDP)
   ↓
4. SIGNALING (Client → Server)
   ↓
   Send offer via WebSocket: { type: "offer", sdp: "..." }
   ↓
5. BACKEND PROCESSING (Server)
   ↓
   WebRTCConnectionHandler receives offer
   ↓
   Create RTCPeerConnection on server
   ↓
   Set remote description (offer)
   ↓
   Create answer (SDP)
   ↓
   Add VideoTransformTrack to receive frames
   ↓
6. SIGNALING (Server → Client)
   ↓
   Send answer via WebSocket: { type: "answer", sdp: "..." }
   ↓
7. CONNECTION ESTABLISHED
   ↓
   ICE candidates exchanged
   ↓
   WebRTC connection active
   ↓
8. VIDEO STREAMING
   ↓
   Browser sends video frames via WebRTC
   ↓
   Server receives frames in VideoTransformTrack.recv()
   ↓
   Frames added to VideoStreamProcessor queue
   ↓
9. FRAME PROCESSING
   ↓
   VideoStreamProcessor.process_frames() loop:
     - Check FPS timing (e.g., every 100ms for 10 FPS)
     - Get frame from queue
     - Skip if queue too full and skip_frames=true
     - Convert frame to numpy array
     - Call YOLODetector.detect(frame)
   ↓
10. YOLO DETECTION
    ↓
    Load frame into YOLOv11 model
    ↓
    Run inference
    ↓
    Filter detections by confidence threshold (>0.25)
    ↓
    Extract bounding boxes, labels, confidences
    ↓
11. SEND RESULTS (Server → Client)
    ↓
    Format detection results as JSON
    ↓
    Send via WebSocket: { type: "detection", data: {...} }
    ↓
12. FRONTEND RECEIVES DETECTIONS
    ↓
    WebSocket onmessage event
    ↓
    Parse detection data
    ↓
    Update React state: setDetections(data.detections)
    ↓
13. RENDER OVERLAY
    ↓
    DetectionOverlay component re-renders
    ↓
    Canvas draws bounding boxes on video
    ↓
    Display labels and confidence scores
    ↓
14. USER SEES RESULTS
    ↓
    [Live video with detection overlay]
```

**Latency Breakdown** (Target <500ms):
- Camera capture: ~16ms (60fps)
- WebRTC transmission: ~50-100ms
- Frame processing: ~40-80ms (depends on YOLO model size)
- WebSocket transmission: ~10-20ms
- Canvas rendering: ~16ms (60fps)
- **Total**: ~150-250ms (well under target)

---

## WebRTC Communication

### What is WebRTC?

**WebRTC** (Web Real-Time Communication) enables peer-to-peer audio/video/data streaming with low latency.

**Key Concepts**:

1. **RTCPeerConnection**: Main WebRTC API for establishing connections
2. **MediaStream**: Represents video/audio stream from camera
3. **SDP (Session Description Protocol)**: Describes connection parameters
4. **ICE (Interactive Connectivity Establishment)**: NAT traversal protocol
5. **Signaling**: Exchange connection information (typically via WebSocket)

### WebRTC Handshake Flow

```
CLIENT                                    SERVER
  │                                         │
  │  1. Create RTCPeerConnection            │
  │  2. Add local video track               │
  │  3. Create offer (SDP)                  │
  │  ────────────────────────────────────▶  │
  │        WebSocket: { type: "offer" }     │
  │                                         │
  │                                         │  4. Receive offer
  │                                         │  5. Create RTCPeerConnection
  │                                         │  6. Set remote description
  │                                         │  7. Create answer (SDP)
  │  ◀────────────────────────────────────  │
  │       WebSocket: { type: "answer" }     │
  │                                         │
  │  8. Set remote description (answer)     │
  │                                         │
  │  9. Exchange ICE candidates             │
  │  ◀───────────────────────────────────▶  │
  │                                         │
  │  10. Connection established!            │
  │  ════════════════════════════════════▶  │
  │        Video frames stream              │
  │                                         │
```

### Why WebRTC vs Regular HTTP Upload?

| Feature | WebRTC | HTTP Upload |
|---------|--------|-------------|
| Latency | 50-100ms | 200-500ms |
| Connection | Peer-to-peer | Client-server |
| Bandwidth | Efficient | High overhead |
| Real-time | Yes | No |
| Buffering | Minimal | Required |

---

## Real-time Detection Pipeline

### Pipeline Stages

```
┌──────────────────────────────────────────────────────────────┐
│                     DETECTION PIPELINE                        │
└──────────────────────────────────────────────────────────────┘

Stage 1: FRAME RECEPTION
┌─────────────────────────────────────────────────────────┐
│ VideoTransformTrack.recv()                              │
│ • Receive frame from WebRTC                             │
│ • Frame format: av.VideoFrame (yuv420p)                 │
│ • Rate: 30 FPS (from camera)                            │
└─────────────────────────────────────────────────────────┘
                         ▼
Stage 2: FRAME BUFFERING
┌─────────────────────────────────────────────────────────┐
│ VideoStreamProcessor.add_frame()                        │
│ • Add to deque buffer (FIFO)                            │
│ • Max size: 30 frames                                   │
│ • Drop oldest if full                                   │
└─────────────────────────────────────────────────────────┘
                         ▼
Stage 3: FPS CONTROL
┌─────────────────────────────────────────────────────────┐
│ Check processing timing                                 │
│ • Target: 10 FPS (100ms interval)                       │
│ • Skip if not enough time passed                        │
│ • Configurable: 5-30 FPS                                │
└─────────────────────────────────────────────────────────┘
                         ▼
Stage 4: FRAME SKIPPING (Optional)
┌─────────────────────────────────────────────────────────┐
│ if skip_frames and queue_size > threshold:              │
│ • Skip frame if queue is backing up                     │
│ • Prevents latency accumulation                         │
│ • Track skipped frames in stats                         │
└─────────────────────────────────────────────────────────┘
                         ▼
Stage 5: FRAME CONVERSION
┌─────────────────────────────────────────────────────────┐
│ Convert av.VideoFrame to numpy array                    │
│ • Format: RGB888                                        │
│ • Shape: (height, width, 3)                             │
│ • Data type: uint8                                      │
└─────────────────────────────────────────────────────────┘
                         ▼
Stage 6: YOLO INFERENCE
┌─────────────────────────────────────────────────────────┐
│ await asyncio.to_thread(detector.detect, frame)         │
│ • Run in thread pool (CPU-bound)                        │
│ • YOLOv11 inference                                     │
│ • Time: ~40-80ms                                        │
└─────────────────────────────────────────────────────────┘
                         ▼
Stage 7: CONFIDENCE FILTERING
┌─────────────────────────────────────────────────────────┐
│ Filter detections                                       │
│ • Remove confidence < threshold (0.25)                  │
│ • Keep only relevant classes (birds, drones, etc.)     │
└─────────────────────────────────────────────────────────┘
                         ▼
Stage 8: RESULT FORMATTING
┌─────────────────────────────────────────────────────────┐
│ Create detection result JSON                            │
│ • Bounding boxes (x1, y1, x2, y2)                       │
│ • Class labels and IDs                                  │
│ • Confidence scores                                     │
│ • Processing stats                                      │
└─────────────────────────────────────────────────────────┘
                         ▼
Stage 9: SEND TO CLIENT
┌─────────────────────────────────────────────────────────┐
│ await websocket.send_json(result)                       │
│ • Send via WebSocket                                    │
│ • Non-blocking                                          │
└─────────────────────────────────────────────────────────┘
```

### Frame Processing Strategy

**Why process at 10 FPS when camera sends 30 FPS?**

- **YOLO inference is slow**: ~40-80ms per frame
- **Processing 30 FPS would cause backlog**: Can't keep up
- **10 FPS is sufficient**: Smooth enough for detection
- **Frame skipping prevents latency**: Drop frames if queue backs up

**Adaptive Processing**:
```python
if time.time() - last_process_time < (1.0 / target_fps):
    continue  # Skip, not enough time passed

if skip_frames and len(frame_queue) > threshold:
    frame_queue.popleft()  # Drop oldest frame
    stats.frames_skipped += 1
    continue
```

---

## API Reference

### REST Endpoints

#### Health Check
```http
GET /api/v1/health
```

**Response**:
```json
{
  "status": "healthy",
  "api_version": "2.0.0",
  "model": "yolo11n.pt"
}
```

#### Active Connections
```http
GET /api/v1/stream/connections
```

**Response**:
```json
{
  "active_connections": 3,
  "connections": [
    {
      "id": "conn_123",
      "connected_at": "2025-10-18T10:30:00Z",
      "frames_processed": 1250
    }
  ]
}
```

### WebSocket Endpoint

#### Connect
```
ws://localhost:8000/api/v1/stream/ws
```

**Connection ID**: Generated by server, returned in first message

---

## Configuration

### Backend Settings

**File**: [apps/api/app/core/config.py](apps/api/app/core/config.py)

```python
# Model Configuration
MODEL_PATH = "yolo11n.pt"          # YOLO model file
CONFIDENCE_THRESHOLD = 0.25        # Minimum confidence (0.0-1.0)

# Stream Configuration
STREAM_FPS = 10                    # Processing FPS (5-30)
STREAM_SKIP_FRAMES = True          # Enable frame skipping
STREAM_MAX_QUEUE_SIZE = 30         # Max frame buffer size

# API Configuration
CORS_ORIGINS = ["http://localhost:3000"]
```

### Frontend Settings

**File**: [apps/web/.env.local](apps/web/.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

---

## Performance Optimization

### Backend Optimizations

1. **Async Frame Processing**
   ```python
   await asyncio.to_thread(detector.detect, frame)
   ```
   - Run CPU-bound YOLO in thread pool
   - Prevents blocking asyncio event loop

2. **Frame Buffering**
   ```python
   frame_queue = deque(maxlen=30)
   ```
   - FIFO queue with max size
   - Automatically drops oldest frames

3. **Frame Skipping**
   - Skip frames when queue backs up
   - Prevents latency accumulation
   - Configurable threshold

4. **FPS Control**
   - Process at target FPS (e.g., 10 FPS)
   - Don't process every frame from camera (30 FPS)
   - Reduce CPU usage

5. **Model Selection**
   - Use `yolo11n.pt` (nano) for speed
   - Upgrade to `yolo11s.pt` (small) for accuracy
   - Trade-off: speed vs accuracy

### Frontend Optimizations

1. **Canvas Rendering**
   - Use `requestAnimationFrame()` for smooth rendering
   - Only redraw when new detections arrive

2. **WebRTC Configuration**
   ```typescript
   const constraints = {
     video: {
       width: { ideal: 1280 },
       height: { ideal: 720 },
       frameRate: { ideal: 30 }
     }
   }
   ```

3. **State Management**
   - Use React hooks with proper dependencies
   - Avoid unnecessary re-renders
   - Memoize expensive computations

---

## Security Considerations

### Backend

1. **CORS Configuration**
   - Whitelist specific origins
   - Don't use wildcard in production

2. **WebSocket Authentication** (Future)
   - Add token-based authentication
   - Validate connections

3. **Rate Limiting** (Future)
   - Limit connections per IP
   - Prevent abuse

### Frontend

1. **Camera Permissions**
   - Request permissions explicitly
   - Handle denied permissions gracefully

2. **HTTPS in Production**
   - WebRTC requires HTTPS (or localhost)
   - Use SSL certificates

---

## Troubleshooting

### Common Issues

#### 1. WebRTC Connection Fails
**Symptoms**: No video streaming, connection timeout

**Solutions**:
- Check CORS settings in backend
- Verify WebSocket URL is correct
- Check firewall/network settings
- Use HTTPS in production (not HTTP)

#### 2. High Latency (>500ms)
**Symptoms**: Delayed detection results

**Solutions**:
- Lower processing FPS (10 → 5)
- Enable frame skipping
- Use smaller YOLO model (yolo11n)
- Check network bandwidth

#### 3. Frame Dropping
**Symptoms**: Choppy video, missed detections

**Solutions**:
- Increase frame queue size (30 → 60)
- Disable frame skipping
- Upgrade hardware (GPU support)

#### 4. No Detections Appearing
**Symptoms**: Video streams but no bounding boxes

**Solutions**:
- Lower confidence threshold (0.25 → 0.15)
- Check YOLO model is loaded
- Verify detection classes are correct
- Check WebSocket messages in browser console

---

## Video Upload and Processing

### Overview

In addition to live camera streaming, SkyLaneAI v2 supports uploading and processing pre-recorded video files. This feature uses **MJPEG streaming** (Motion JPEG) to deliver annotated video frames with bounding boxes already rendered on them.

### Key Innovation: MJPEG Streaming

Unlike the live stream feature which uses WebRTC + Canvas overlay, the video upload feature uses a **different approach** inspired by the original SkylaneAI:

**Traditional Approach (Live Stream)**:
- Video plays independently in HTML5 `<video>` element
- Detections sent via WebSocket as JSON
- Frontend draws bounding boxes on Canvas overlay
- **Challenge**: Synchronization between video and detections

**MJPEG Approach (Video Upload)** ✅:
- Backend processes video and **renders bounding boxes directly onto frames**
- Annotated frames buffered in memory
- After processing completes, frames streamed as MJPEG (Motion JPEG)
- Frontend displays MJPEG stream in `<img>` tag
- **Benefit**: Perfect synchronization (frames and boxes are one image)

### Architecture

The video upload feature follows a separated processing/playback model:

```
┌─────────────────────────────────────────────────────────────────┐
│              NEW VIDEO UPLOAD FLOW (MJPEG Streaming)            │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: UPLOAD & METADATA
   ↓
1. USER UPLOADS VIDEO
   Browser → FormData → POST /api/v1/video/upload
   ↓
2. SERVER SAVES & EXTRACTS METADATA
   Save to temp/uploads/{uuid}.mp4 → cv2.VideoCapture → Extract metadata
   ↓
   Return: video_id, duration, fps, resolution, total_frames, codec
   ↓
3. FRONTEND SHOWS PROCESSING UI
   Display video info → Show "Start Processing" button

PHASE 2: PROCESSING (Runs Once)
   ↓
4. USER CLICKS "START PROCESSING"
   Connect WebSocket → Send { type: "start" }
   ↓
5. SERVER PROCESSES ALL FRAMES
   Loop through video:
     - Read frame with cv2.VideoCapture
     - Run YOLO detection
     - Render bounding boxes ONTO frame using cv2.rectangle()
     - Buffer annotated frame in memory (deque)
     - Send progress updates (0% → 100%)
   ↓
6. PROCESSING COMPLETES
   All annotated frames buffered → Set processing_completed = True
   ↓
   Frontend receives "completed" message → Shows "Play" button

PHASE 3: PLAYBACK (Can Replay Multiple Times)
   ↓
7. USER CLICKS "PLAY"
   Frontend loads: <img src="/api/v1/video/{video_id}/mjpeg">
   ↓
8. SERVER STREAMS MJPEG
   Read from frame buffer → Encode as JPEG → Stream with MJPEG headers
   ↓
   multipart/x-mixed-replace boundary format
   ↓
9. FRONTEND DISPLAYS
   MjpegPlayer component shows annotated frames
   ↓
   Bounding boxes already on frames (perfect sync!)
   ↓
10. PLAYBACK CONTROLS
   Pause → Stops MJPEG stream
   Play again → Reloads MJPEG stream from beginning
```

---

### Backend Components

#### 1. VideoFileProcessor ([video_file_processor.py](apps/api/app/services/video_file_processor.py))

**Purpose**: Process uploaded video files frame-by-frame with YOLO detection and MJPEG streaming

```python
class VideoFileProcessor:
    """
    Processes uploaded video files with MJPEG output:
    - Opens video with cv2.VideoCapture
    - Extracts metadata (fps, duration, resolution, codec)
    - Reads frames sequentially
    - Runs YOLO detection on each frame
    - **NEW**: Renders bounding boxes onto frames using cv2.rectangle()
    - **NEW**: Buffers annotated frames in deque (up to 10,000 frames)
    - **NEW**: Supports MJPEG playback controls (play/pause/stop)
    - Sends detections + progress via WebSocket callback
    """
```

**Key Methods**:

*Processing Phase:*
- `initialize()`: Open video file and extract metadata
- `start_processing()`: Begin frame-by-frame processing (processes ALL frames)
- `pause_processing()`: Pause at current frame
- `resume_processing()`: Continue from current frame
- `stop_processing()`: Stop and cleanup

*MJPEG Playback Phase (NEW):*
- `mjpeg_play()`: Start MJPEG playback (requires processing_completed = True)
- `mjpeg_pause()`: Pause MJPEG stream
- `mjpeg_resume()`: Resume MJPEG stream
- `mjpeg_stop()`: Stop and reset to beginning
- `is_mjpeg_ready()`: Check if processing completed and frames buffered
- `get_annotated_frames()`: Get deque buffer of annotated frames
- `clear_frame_buffer()`: Free memory by clearing frame buffer

**Processing Loop**:
```python
async def _process_loop(self):
    while self.is_playing:
        if self.is_paused:
            await asyncio.sleep(0.1)
            continue

        # Read next frame
        ret, frame = self.cap.read()
        if not ret:
            await self._on_video_completed()
            break

        # Run YOLO detection
        detections, processing_time = await asyncio.to_thread(
            detector.detect, frame
        )

        # Send to frontend
        await self.on_detection_callback({
            "frame_number": self.current_frame_number,
            "timestamp": frame_number / fps,
            "detections": detections,
            "processing_time_ms": processing_time
        })

        # Wait for next frame (accounting for playback speed)
        await asyncio.sleep(frame_interval / playback_speed)
```

**Metadata Extraction**:
```python
# Extract video metadata using OpenCV
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
duration = total_frames / fps
```

---

#### 2. Video Routes ([video_routes.py](apps/api/app/api/video_routes.py))

**Upload Endpoint**:
```http
POST /api/v1/video/upload
Content-Type: multipart/form-data

Request:
- file: Video file (MP4, AVI, MOV, MKV)

Response:
{
  "video_id": "uuid",
  "filename": "sample.mp4",
  "duration": 30.5,
  "fps": 30.0,
  "total_frames": 915,
  "width": 1920,
  "height": 1080,
  "size_mb": 12.4,
  "codec": "h264"
}
```

**Metadata Endpoint**:
```http
GET /api/v1/video/{video_id}/metadata

Response:
{
  "video_id": "uuid",
  "filename": "sample.mp4",
  "duration": 30.5,
  ...
}
```

**Delete Endpoint**:
```http
DELETE /api/v1/video/{video_id}

Response:
{
  "message": "Video deleted successfully",
  "video_id": "uuid"
}
```

**WebSocket Endpoint**:
```
ws://localhost:8000/api/v1/video/ws/{video_id}
```

**WebSocket Messages (Client → Server)**:
```json
// Start processing
{ "type": "start", "speed": 1.0 }

// Pause processing
{ "type": "pause" }

// Resume processing
{ "type": "resume" }

// Stop processing
{ "type": "stop" }

// Seek to frame
{ "type": "seek", "frame_number": 150 }

// Seek to timestamp
{ "type": "seek", "timestamp": 5.2 }

// Update settings
{
  "type": "settings",
  "data": {
    "process_fps": 10,
    "confidence_threshold": 0.25,
    "playback_speed": 1.5
  }
}
```

**WebSocket Messages (Server → Client)**:
```json
// Detection results (same format as live stream)
{
  "type": "detection",
  "data": {
    "frame_number": 123,
    "timestamp": 4.1,
    "detections": [...],
    "processing_time_ms": 45.2,
    "frameWidth": 1920,
    "frameHeight": 1080
  }
}

// Processing progress
{
  "type": "progress",
  "data": {
    "current_frame": 123,
    "total_frames": 915,
    "percentage": 13.4
  }
}

// Video completed
{ "type": "completed" }

// State changes
{ "type": "started" }
{ "type": "paused" }
{ "type": "resumed" }
{ "type": "stopped" }
{ "type": "seeked", "frame_number": 150 }
```

---

### Frontend Components

#### 1. useVideoUpload Hook ([use-video-upload.ts](apps/web/src/hooks/use-video-upload.ts))

**Purpose**: Manage video file uploads

```typescript
export function useVideoUpload() {
  const uploadVideo = async (file: File) => {
    // Validate file type and size
    // Create FormData and upload
    // Return metadata
  }

  const deleteVideo = async (videoId: string) => {
    // Delete from server
  }

  return {
    uploadVideo,
    deleteVideo,
    uploadProgress,
    videoMetadata,
    isUploading,
    error
  }
}
```

**Features**:
- File validation (type, size)
- Upload progress tracking
- Error handling
- Metadata storage

---

#### 2. useVideoStream Hook ([use-video-stream.ts](apps/web/src/hooks/use-video-stream.ts))

**Purpose**: WebSocket connection for video detection streaming

```typescript
export function useVideoStream({ videoId, onDetection, onProgress }) {
  const connect = async () => {
    // Connect to ws://localhost:8000/api/v1/video/ws/{videoId}
  }

  const play = (speed: number) => {
    // Send start message
  }

  const pause = () => {
    // Send pause message
  }

  const seek = (options) => {
    // Send seek message
  }

  return {
    connect,
    disconnect,
    play,
    pause,
    resume,
    stop,
    seek,
    updateSettings,
    connectionStatus,
    isConnected,
    progress
  }
}
```

**Similar to `useWebRTC`** but for video files instead of live camera.

---

#### 3. VideoUpload Component ([video-upload.tsx](apps/web/src/components/video/video-upload.tsx))

**Purpose**: Drag-and-drop upload interface

**Features**:
- Drag-and-drop zone
- File type validation
- Upload progress bar
- Selected file preview
- Error/success messages

**UI States**:
- **Idle**: Drag-and-drop zone with upload icon
- **File Selected**: Show file info (name, size)
- **Uploading**: Progress bar with percentage
- **Success**: Checkmark with success message
- **Error**: Error alert with message

---

#### 4. VideoPlayer Component ([video-player.tsx](apps/web/src/components/video/video-player.tsx))

**Purpose**: Play uploaded video with custom controls

**Features**:
- HTML5 `<video>` element with Object URL
- Custom controls overlay
- Play/pause button
- Seek slider (timeline)
- Skip forward/backward (10s)
- Playback speed selector (0.5x, 1x, 1.5x, 2x)
- Time display (current / duration)

**Synchronization**:
```typescript
// Video player plays at native FPS
// Server processes at configured FPS (e.g., 10 FPS)
// Frontend syncs detections with video time

const handleTimeUpdate = () => {
  const currentFrame = Math.floor(video.currentTime * fps)
  // Show detections matching current frame
  const matchingDetections = detections.filter(
    d => d.frameNumber === currentFrame
  )
  setVisibleDetections(matchingDetections)
}
```

---

#### 5. Video Detection Page ([/video/page.tsx](apps/web/src/app/video/page.tsx))

**Two-Mode Interface**:

**Mode 1: Upload Mode** (no video uploaded)
- Large drag-and-drop upload zone
- Upload button
- Instructions and supported formats

**Mode 2: Playback Mode** (video uploaded)
- **Left Column (2/3 width)**:
  - Video player with detection overlay
  - Video metadata card (duration, resolution, FPS, size)
  - Processing progress bar
  - Detection statistics

- **Right Column (1/3 width)**:
  - Connection status badge
  - Start/Pause/Resume/Delete buttons
  - Detection settings (FPS, confidence threshold)

**Reused Components**:
- `DetectionOverlay` - Same overlay used for live stream
- `DetectionStats` - Same statistics display
- `DetectionSettings` - Same settings panel

**State Management**:
```typescript
const [videoMetadata, setVideoMetadata] = useState(null)
const [videoFile, setVideoFile] = useState(null)
const [isProcessing, setIsProcessing] = useState(false)

// Upload flow
1. User uploads file → setVideoFile(file)
2. Upload completes → setVideoMetadata(metadata)
3. Mode switches to playback

// Processing flow
1. Click "Start Processing" → connect() → play()
2. Receive detections → addDetectionResult()
3. Detections drawn on overlay
4. Progress updates in real-time
```

---

### Data Flow: Video Upload to Detection

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPLETE VIDEO FLOW                           │
└─────────────────────────────────────────────────────────────────┘

Step 1: UPLOAD
  User drags video → VideoUpload component → FormData
  ↓
  POST /api/v1/video/upload
  ↓
  Server saves to temp/uploads/{uuid}.mp4
  ↓
  Extract metadata with cv2.VideoCapture
  ↓
  Return video_id + metadata
  ↓
  Frontend stores metadata, shows video player

Step 2: CONNECT
  User clicks "Start Processing"
  ↓
  useVideoStream.connect()
  ↓
  WebSocket connects to ws://.../video/ws/{video_id}
  ↓
  Server creates VideoFileProcessor instance
  ↓
  Connection established

Step 3: START PROCESSING
  Frontend sends: { type: "start", speed: 1.0 }
  ↓
  Server starts processing loop
  ↓
  Read frame with cv2.VideoCapture
  ↓
  Run YOLO detection (reuses detector.detect())
  ↓
  Send detection results via WebSocket

Step 4: RECEIVE DETECTIONS
  Frontend receives detection message
  ↓
  useVideoStream calls onDetection(message)
  ↓
  useDetections.addDetectionResult(message)
  ↓
  State updated with new detections
  ↓
  DetectionOverlay re-renders with bounding boxes

Step 5: SYNC WITH VIDEO
  Video plays at native FPS (e.g., 30 FPS)
  ↓
  Server processes at configured FPS (e.g., 10 FPS)
  ↓
  Frontend buffers all detections
  ↓
  On video.timeupdate:
    - Calculate current frame number
    - Filter detections matching current frame
    - Show only matching detections on overlay

Step 6: PLAYBACK CONTROLS
  User clicks pause → Send { type: "pause" }
  ↓
  Server pauses frame reading
  ↓
  User seeks to 5s → Send { type: "seek", timestamp: 5.0 }
  ↓
  Server: cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
  ↓
  Processing resumes from new position
```

---

### Key Differences: Live Stream vs Video Upload

| Feature | Live Stream (WebRTC) | Video Upload |
|---------|---------------------|--------------|
| **Input Source** | Browser camera via WebRTC | Uploaded video file |
| **Frame Source** | `VideoTransformTrack.recv()` | `cv2.VideoCapture.read()` |
| **Frame Rate** | Camera FPS (30 FPS) | Video native FPS or configurable |
| **Playback Control** | None (real-time only) | Play, pause, seek, speed control |
| **Video Display** | MediaStream on `<video>` | Object URL on `<video>` |
| **Frame Sync** | Real-time (no sync needed) | Sync by frame number/timestamp |
| **Processing** | Continuous stream | Can pause/resume/seek |
| **Storage** | None (live only) | Temporary file storage |
| **Detection Pipeline** | VideoStreamProcessor | VideoFileProcessor |
| **WebSocket** | `/api/v1/stream/ws` | `/api/v1/video/ws/{video_id}` |

---

### Shared Components

Both live streaming and video upload **reuse the same**:
1. **YOLODetector** - Same YOLO model and detection logic
2. **DetectionOverlay** - Same canvas rendering for bounding boxes
3. **DetectionStats** - Same statistics display component
4. **DetectionSettings** - Same settings panel (FPS, confidence)
5. **Detection Types** - Same TypeScript interfaces
6. **Detection Processing** - Similar frame processing pattern

This design ensures **consistency** and **code reuse** across both features.

---

### File Storage and Cleanup

**Upload Directory**:
```python
VIDEO_UPLOAD_DIR = "temp/uploads"  # Configurable
```

**File Naming**:
```python
# Files stored as: {uuid}.{extension}
# Example: 3fa85f64-5717-4562-b3fc-2c963f66afa6.mp4
```

**Cleanup Strategy**:
- Videos deleted when user clicks "Delete" button
- Future: Auto-cleanup after `VIDEO_CLEANUP_HOURS` (default: 24 hours)
- Future: Cleanup on server restart (scan temp directory)

**Storage Limits**:
```python
VIDEO_MAX_SIZE_MB = 100  # Maximum file size
VIDEO_ALLOWED_FORMATS = [".mp4", ".avi", ".mov", ".mkv"]
```

---

### Performance Considerations

**1. Frame Processing Rate**:
- Video plays at native FPS (e.g., 30 FPS)
- Server processes at configured FPS (e.g., 10 FPS)
- Reduces CPU usage while maintaining smooth detection

**2. Playback Speed Control**:
- User can speed up (2x) or slow down (0.5x) processing
- Useful for quick analysis or detailed inspection

**3. Frame Skipping**:
- Server processes every Nth frame based on FPS setting
- Example: 30 FPS video, 10 FPS processing = process every 3rd frame

**4. Memory Management**:
- Video file kept in temp storage (not loaded into memory)
- Only current frame in memory during processing
- Detections sent immediately (not buffered on server)

**5. Frontend Buffering**:
- Frontend buffers all received detections
- Filters by frame number for current video time
- Enables smooth playback without re-requesting detections

---

## Next Steps

### Phase 3: Video Upload Enhancements

**Completed ✅**:
- Video upload and storage
- Frame-by-frame processing
- Playback controls
- Detection overlay
- Progress tracking

**Future Enhancements**:
- Export processed video with bounding boxes burned in
- Download detection results as JSON/CSV
- Video trimming before processing
- Batch video processing (multiple videos)
- Video thumbnails/previews
- Detection timeline visualization
- Auto-cleanup scheduled task

### Phase 4: Database Integration

- Store detection history
- User authentication
- Analytics dashboard
- Custom YOLO training
- Mobile app
- Deployment (Docker, cloud)

---

## Summary: Video Upload Feature Architecture

### Separation of Concerns

The video upload feature has been redesigned to **separate processing from playback**:

**Before (Coupled)**:
- Processing and playback happened simultaneously
- Couldn't replay without reprocessing
- Complex synchronization issues

**After (Separated)** ✅:
- **Phase 1**: Process entire video once (0% → 100%)
- **Phase 2**: Play processed video multiple times
- No synchronization issues (frames pre-rendered)
- Clean user experience

### Key Components Summary

**Backend**:
1. **YOLODetector.render_detections()** - NEW method to draw bounding boxes on frames
2. **VideoFileProcessor.annotated_frames** - NEW deque buffer for annotated frames
3. **VideoFileProcessor.mjpeg_*()** - NEW playback control methods
4. **GET /api/v1/video/{id}/mjpeg** - NEW MJPEG streaming endpoint
5. **WebSocket messages** - NEW mjpeg_play/pause/resume/stop commands

**Frontend**:
1. **MjpegPlayer component** - NEW simple `<img>` tag for MJPEG streams
2. **Separated UI states** - Processing vs Playback modes
3. **Play/Pause controls** - Appear after processing completes

### Technical Advantages

✅ **Perfect Synchronization**: Frames and detections are merged on backend
✅ **No Flickering**: Detections burned into frames, always visible
✅ **Replayability**: Watch annotated video multiple times without reprocessing
✅ **Simpler Frontend**: Just an `<img>` tag, no complex canvas overlay
✅ **Backend-Controlled**: Video plays at exact processing FPS
✅ **Memory Efficient**: Frames streamed on-demand, not stored on disk
✅ **Proven Architecture**: Based on original SkylaneAI's successful implementation

### User Workflow

```
1. Upload video → See video info
2. Click "Start Processing" → Progress bar (0% → 100%)
3. Wait for completion → "Play" button appears
4. Click "Play" → Watch annotated video
5. Can pause/resume/replay anytime
```

### Performance Characteristics

| Metric | Value |
|--------|-------|
| **Frame Buffer** | Up to 10,000 frames in memory |
| **MJPEG Quality** | 85% JPEG compression |
| **Streaming FPS** | Matches processing FPS (default 10 FPS) |
| **Memory Usage** | ~50-100 MB per minute of video |
| **Replay Speed** | Instant (no reprocessing needed) |

---

## AI-Powered Alert Generation System

### Overview

SkyLaneAI v2 features a sophisticated **4-agent alert generation system** that transforms raw YOLOv11 detections into natural language alerts with actionable recommendations. The system generates **one intelligent alert per second** of video, dramatically improving user experience and efficiency.

### Problem & Solution

**Before (Per-Frame Alerts)**:
- YOLOv11 detects at 10 FPS = 10 detections per second
- Same object detected 10 times = 10 redundant alerts
- 5-second video = 50 potential manual clicks required ❌
- Overwhelming for users, high cognitive load

**After (Time-Based Alerts)** ✅:
- System automatically selects BEST detection per second
- 4 AI agents generate 1 comprehensive alert per second
- 5-second video = 5 automatic alerts displayed in timeline
- Zero user clicks required, seamless experience

### Architecture: 4-Agent Pipeline

The alert generation system uses **4 specialized AI agents** working in sequence:

```
┌─────────────────────────────────────────────────────────────┐
│               4-AGENT ALERT PIPELINE                         │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  YOLO Detection  │ → Raw detection: class, bbox, confidence
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│  AGENT 1: Context Enrichment Agent                           │
│  - Analyzes bounding box size (small/medium/large)           │
│  - Determines screen position (center/left/right/etc)        │
│  - Calculates bbox area in pixels                            │
│  - Assesses threat level (low/moderate/high/critical)        │
│  Output: EnrichedContext                                     │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│  AGENT 2: Message Agent                                      │
│  - Crafts natural language message                           │
│  - Generates emoji for visual impact (🦅, 🚁, ⚠️)            │
│  - Creates title and detailed body                           │
│  - Structures information in sections                        │
│  Output: CraftedMessage                                      │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│  AGENT 3: Action Agent                                       │
│  - Recommends primary action (immediate response)            │
│  - Suggests secondary action (follow-up)                     │
│  - Provides reasoning for recommendations                    │
│  - Assigns urgency level (immediate/urgent/caution/advisory) │
│  Output: ActionRecommendation                                │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│  AGENT 4: Priority Agent                                     │
│  - Calculates overall priority score (0-100)                 │
│  - Determines priority level (critical/high/medium/low)      │
│  - Breaks down factors: threat, confidence, size, urgency    │
│  - Provides weighted scoring for each factor                 │
│  Output: PriorityAssessment                                  │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│  Complete NaturalLanguageAlert                               │
│  {                                                            │
│    detection: {...},                                          │
│    context: {...},                                            │
│    message: {title, emoji, body, sections},                  │
│    action: {primary, secondary, reasoning, urgency},         │
│    priority: {score, level, factors}                         │
│  }                                                            │
└───────────────────────────────────────────────────────────────┘
```

### Agent Implementation Details

#### Agent 1: Context Enrichment Agent
**File**: `apps/api/app/agents/context_agent.py`

**Input**: Raw YOLOv11 detection
```python
{
  "class_name": "bird",
  "confidence": 0.87,
  "bbox": {"x1": 100, "y1": 200, "x2": 300, "y2": 400}
}
```

**Output**: Enriched context
```python
{
  "estimated_size": "medium",        # small/medium/large
  "bbox_area_pixels": 40000,
  "screen_position": "center-right", # 9 positions
  "threat_level_raw": "high"         # low/moderate/high/critical
}
```

**Logic**:
- Size: Based on bbox area % of frame
- Position: Divides frame into 3x3 grid
- Threat: Combines size + confidence + class type

---

#### Agent 2: Message Agent
**File**: `apps/api/app/agents/message_agent.py`

**Uses**: Anthropic Claude API (claude-3-5-sonnet-20241022)

**Input**: Detection + EnrichedContext

**Output**: Natural language message
```python
{
  "title": "Medium Bird Detected - Center Right",
  "emoji": "🦅",
  "body": "A **medium-sized bird** has been detected in the **center-right** area...",
  "sections": {
    "detection": "Bird at 87% confidence",
    "location": "Center-right, 40,000 px²",
    "assessment": "High threat due to size and position"
  }
}
```

**Prompt Engineering**:
- System prompt defines aviation safety context
- Structured output format (JSON schema)
- Emphasis on clarity and actionability

---

#### Agent 3: Action Agent
**File**: `apps/api/app/agents/action_agent.py`

**Uses**: Anthropic Claude API

**Input**: Detection + EnrichedContext

**Output**: Action recommendations
```python
{
  "primary_action": "Maintain increased vigilance and prepare for evasive maneuvers",
  "secondary_action": "Monitor bird's trajectory and alert air traffic control if necessary",
  "reasoning": "Medium bird at high confidence warrants elevated caution",
  "urgency": "urgent"  # immediate/urgent/caution/advisory
}
```

**Decision Matrix**:
| Threat Level | Confidence | Urgency |
|--------------|------------|---------|
| Critical | >0.7 | Immediate |
| High | >0.5 | Urgent |
| Moderate | >0.3 | Caution |
| Low | Any | Advisory |

---

#### Agent 4: Priority Agent
**File**: `apps/api/app/agents/priority_agent.py`

**Uses**: Anthropic Claude API

**Input**: Detection + EnrichedContext + Message + Action

**Output**: Priority assessment
```python
{
  "overall_score": 78.5,  # 0-100 scale
  "priority_level": "high",  # critical/high/medium/low
  "factors": {
    "threat_level": {"value": "high", "score": 90, "weight": 0.4},
    "confidence": {"value": 0.87, "score": 87, "weight": 0.3},
    "size_impact": {"value": "medium", "score": 70, "weight": 0.2},
    "urgency": {"value": "urgent", "score": 80, "weight": 0.1}
  }
}
```

**Scoring Formula**:
```python
overall_score = (
    threat_score × 0.4 +
    confidence × 100 × 0.3 +
    size_score × 0.2 +
    urgency_score × 0.1
)
```

---

### Time-Based Alert Generation

#### Processing Flow

**Backend** (`apps/api/app/services/video_file_processor.py`):

```python
class VideoFileProcessor:
    # Time-based alert state
    enable_time_based_alerts = True
    current_second = 0
    detections_in_current_second = []  # Buffer for detections

    async def _process_frame(self, frame):
        # 1. Run YOLO detection
        detections = await detector.detect(frame)

        # 2. Enrich context (Agent 1)
        contexts = [context_agent.enrich(d) for d in detections]

        # 3. Calculate video second
        video_second = int(timestamp)

        # 4. Store in buffer for current second
        for det, ctx in zip(detections, contexts):
            self.detections_in_current_second.append((det, ctx, width, height))

        # 5. When second changes, generate alert
        if video_second > self.current_second:
            await self._generate_alert_for_second(self.current_second)
            self.current_second = video_second
            self.detections_in_current_second.clear()

    async def _generate_alert_for_second(self, second):
        # 1. Select BEST detection from buffer
        best_detection, best_context = self._select_best_detection()

        # 2. Run all 4 agents
        alert = await alert_workflow.generate_complete_alert(
            detection=best_detection,
            image_width=width,
            image_height=height
        )

        # 3. Send to frontend via WebSocket
        await self.on_alert_callback({
            "second": second,
            "timestamp": float(second),
            "alert": {
                "detection": alert.detection.model_dump(),
                "context": alert.context.model_dump(),
                "message": alert.message.model_dump(),
                "action": alert.action.model_dump(),
                "priority": alert.priority.model_dump()
            }
        })
```

#### Best Detection Selection

**Algorithm**: Prioritize most critical detection per second

```python
def _select_best_detection(self):
    """
    Priority score = (threat_level × 0.5) +
                     (confidence × 0.3) +
                     (size × 0.2)

    Threat scores: critical=100, high=75, moderate=50, low=25
    """
    best_score = -1
    best_item = None

    for det, ctx, width, height in self.detections_in_current_second:
        # Calculate priority
        threat_score = {"critical": 100, "high": 75, "moderate": 50, "low": 25}[ctx.threat_level_raw]
        confidence_score = det.confidence * 100
        size_score = min((ctx.bbox_area_pixels / (width * height)) * 100 * 10, 100)

        priority = (
            threat_score * 0.5 +
            confidence_score * 0.3 +
            size_score * 0.2
        )

        if priority > best_score:
            best_score = priority
            best_item = (det, ctx, width, height)

    return best_item
```

---

### Frontend Components

#### 1. Alert Timeline Component
**File**: `apps/web/src/components/video/alert-timeline.tsx`

**Features**:
- Scrollable timeline with all alerts (one per second)
- Color-coded by priority (critical=red, high=orange, medium=yellow, low=blue)
- Shows timestamp, emoji, title, priority score
- Expandable details (inline, no modal)
- "Jump to Time" button for video seeking
- Highlights current alert based on playback position

**Inline Expandable Details** (NEW):
When user clicks "View Details", the alert expands inline to show:
- Priority Analysis with score breakdown
- Detection Context (size, position, area, threat level)
- Recommended Actions (primary/secondary with urgency badge)
- Full Message body with formatted text

**Visual Design**:
```
┌─────────────────────────────────────────────────────────┐
│ ⏰ Alert Timeline                           [5 alerts]  │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 🦅 00:01 [LOW] Small bird detected        Score: 35 │ │
│ │ Maintain normal vigilance and continue observation  │ │
│ │ [Jump to Time] [View Details ▼]                     │ │
│ └─────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 🚁 00:03 [HIGH] Large drone approaching  Score: 78  │ │  ← CURRENT
│ │ Prepare for evasive maneuvers immediately           │ │
│ │ [Jump to Time] [Hide Details ▲]                     │ │
│ │                                                      │ │
│ │ 📊 Priority Analysis: 78.5                          │ │
│ │   Threat Level: high (90) × 40%                     │ │
│ │   Confidence: 87% × 30%                             │ │
│ │                                                      │ │
│ │ 🎯 Detection Context                                │ │
│ │   Size: large, Position: center-right               │ │
│ │   Area: 120,000 px², Threat: high                   │ │
│ │                                                      │ │
│ │ ⚡ Recommended Actions [URGENT]                     │ │
│ │   PRIMARY: Prepare evasive maneuvers                │ │
│ │   SECONDARY: Alert air traffic control              │ │
│ │                                                      │ │
│ │ 📄 Full Message: A large drone has been...         │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

#### 2. useTimeBasedAlerts Hook
**File**: `apps/web/src/hooks/use-time-based-alerts.ts`

**API**:
```typescript
export function useTimeBasedAlerts() {
  const [alerts, setAlerts] = useState<TimeBasedAlert[]>([]);

  // Add new alert from WebSocket
  const addAlert = (message: WSTimeBasedAlertMessage) => {
    const alert: TimeBasedAlert = {
      second: message.data.second,
      timestamp: message.data.timestamp,
      priorityLevel: message.data.alert.priority.priority_level,
      priorityScore: message.data.alert.priority.overall_score,
      title: message.data.alert.message.title,
      emoji: message.data.alert.message.emoji,
      hazardType: message.data.alert.detection.class_name,
      primaryAction: message.data.alert.action.primary_action,
      urgency: message.data.alert.action.urgency,
      fullAlert: message.data.alert
    };

    setAlerts(prev => [...prev, alert].sort((a, b) => a.timestamp - b.timestamp));
  };

  // Clear all alerts
  const clearAlerts = () => setAlerts([]);

  // Get alert at specific timestamp
  const getAlertAtTimestamp = (timestamp: number) => {
    const second = Math.floor(timestamp);
    return alerts.find(a => a.second === second);
  };

  // Get statistics
  const getStatistics = () => {
    return {
      totalAlerts: alerts.length,
      bySeverity: countBySeverity(alerts),
      byUrgency: countByUrgency(alerts),
      averageScore: calculateAverageScore(alerts),
      topAlert: findTopAlert(alerts)
    };
  };

  return { alerts, addAlert, clearAlerts, getAlertAtTimestamp, getStatistics };
}
```

---

#### 3. Video Page Integration
**File**: `apps/web/src/app/video/page.tsx`

**Integration**:
```typescript
// Initialize time-based alerts hook
const { alerts, addAlert, clearAlerts } = useTimeBasedAlerts();

// Handle WebSocket messages
const { connect, play } = useVideoStream({
  videoId: videoMetadata?.videoId,
  onDetection: (message) => {
    addDetectionResult(message); // Per-frame detections
  },
  onTimeBasedAlert: (message) => {
    addAlert(message); // One alert per second
    console.log('Time-based alert:', message.data.second, message.data.alert.priority.priority_level);
  },
  onCompleted: () => {
    setProcessingCompleted(true);
  }
});

// Display alert timeline
{alerts.length > 0 && (
  <AlertTimeline
    alerts={alerts}
    currentTimestamp={currentVideoTime}
  />
)}

// Cleanup on video delete
const handleDeleteVideo = async () => {
  clearAlerts(); // Clear time-based alerts
  clearDetections(); // Clear per-frame detections
};
```

---

### WebSocket Message Flow

**New Message Type** (`apps/api/app/api/video_routes.py`):
```json
{
  "type": "time_based_alert",
  "data": {
    "second": 3,
    "timestamp": 3.0,
    "alert": {
      "detection": {
        "class_name": "drone",
        "class_id": 1,
        "confidence": 0.89,
        "bbox": {"x1": 150, "y1": 250, "x2": 450, "y2": 550}
      },
      "context": {
        "estimated_size": "large",
        "bbox_area_pixels": 120000,
        "screen_position": "center-right",
        "threat_level_raw": "high"
      },
      "message": {
        "title": "Large Drone Detected - High Threat",
        "emoji": "🚁",
        "body": "A **large drone** has been detected in the **center-right** area of the frame...",
        "sections": {...}
      },
      "action": {
        "primary_action": "Prepare for evasive maneuvers immediately",
        "secondary_action": "Alert air traffic control and monitor trajectory",
        "reasoning": "Large drone at high confidence poses significant collision risk",
        "urgency": "urgent"
      },
      "priority": {
        "overall_score": 78.5,
        "priority_level": "high",
        "factors": {
          "threat_level": {"value": "high", "score": 90, "weight": 0.4},
          "confidence": {"value": 0.89, "score": 89, "weight": 0.3},
          "size_impact": {"value": "large", "score": 85, "weight": 0.2},
          "urgency": {"value": "urgent", "score": 80, "weight": 0.1}
        }
      }
    }
  }
}
```

---

### API Endpoints

**Removed Obsolete Endpoints** (as of 2025-11-02):
- ❌ `POST /api/v1/alerts/generate-complete` - Previously used by now-deleted AlertDetailModal
- ❌ `POST /api/v1/alerts/generate-message` - Development/testing endpoint, unused
- ❌ `POST /api/v1/alerts/generate-action` - Development/testing endpoint, unused

**Remaining Endpoints**:
- ✅ `POST /api/v1/alerts/generate-batch` - Batch alert generation (future analytics)
- ✅ `POST /api/v1/alerts/generate-summary` - Summary report generation (future analytics)

**Note**: Time-based alerts are generated automatically during video processing and sent via WebSocket. No manual HTTP API calls needed from frontend.

---

### Performance & Cost Analysis

**Processing Efficiency**:
| Metric | Value |
|--------|-------|
| Video Length | 60 seconds |
| YOLO Detections | 600 (10 FPS × 60s) |
| Detections Stored | 600 (all sent to frontend) |
| Alerts Generated | 60 (one per second) |
| LLM API Calls | 240 (4 agents × 60 seconds) |
| Total Cost | ~$0.036 (60 × 4 × $0.00015/call) |
| Processing Time | ~2-3 minutes for 60s video |

**Cost Breakdown**:
- Context Agent: Rule-based, no API call
- Message Agent: ~$0.00015 per call
- Action Agent: ~$0.00015 per call
- Priority Agent: ~$0.00015 per call
- **Total per alert**: ~$0.00045

**User Experience Benefits**:
- ✅ Zero manual clicks required
- ✅ Comprehensive alerts with rich context
- ✅ Actionable recommendations for pilots
- ✅ Priority-sorted timeline for quick scanning
- ✅ Perfect synchronization (one alert = one second of video)

---

### Removed Obsolete Components

**Deleted Files** (as of 2025-11-02):
1. `apps/web/src/components/video/detection-context-panel.tsx` - Replaced by inline expandable details in AlertTimeline
2. `apps/web/src/components/video/alert-detail-modal.tsx` - Replaced by inline expandable details in AlertTimeline

**Reason for Removal**:
- Modal-based detail view was cumbersome (required clicking, opening, closing)
- Inline expandable details provide better UX (view multiple alerts at once)
- Consistent with time-based alert design philosophy (seamless, automatic)

---

*Last updated: 2025-11-02*

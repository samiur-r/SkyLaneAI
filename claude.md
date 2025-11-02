# SkyLaneAI v2 - Claude Development Context

**Last Updated**: 2025-11-02

## Project Vision

SkyLaneAI v2 is a safety-critical system designed to protect flying taxis and other aerial vehicles from sky hazards. The system analyzes video feeds in real-time to detect birds, drones, balloons, and kites, calculating Time-to-Contact (TTC) to provide graded collision warnings.

## Architecture Overview

### Technology Choices & Rationale

**Frontend: Next.js (App Router)**
- Server-side rendering for optimal performance
- App Router for modern React patterns
- Built-in API routes for edge functions
- Excellent TypeScript support

**UI Framework: shadcn/ui**
- Accessible, customizable components
- Built on Radix UI primitives
- Tailwind CSS integration
- Copy-paste component approach for flexibility

**Backend: FastAPI**
- Async support for real-time video processing
- Automatic API documentation (OpenAPI/Swagger)
- High performance for ML inference
- Native Python integration with YOLOv11

**Object Detection: YOLOv11**
- Latest YOLO version with improved accuracy
- Real-time inference capabilities
- Custom training for sky hazard detection
- Efficient GPU utilization

**Database & Auth: Supabase**
- PostgreSQL database with real-time subscriptions
- Built-in authentication and authorization
- Storage for video files
- RESTful and GraphQL APIs

**Monorepo: pnpm**
- Fast, efficient package management
- Workspace protocol for shared packages
- Reduced disk space usage
- Faster installation times

## Current Implementation Status

### ✅ Implemented Features
- **Video Upload & Processing**: Upload videos for hazard detection analysis
- **Real-time Detection Display**: Video player with bounding boxes and detection labels
- **Alert Timeline**: Interactive timeline showing all detections throughout the video
- **Detection Filtering**: Filter alerts by hazard type and severity level
- **AI-Powered Alert System**: Context-aware alert generation with message agents
- **Responsive UI**: Modern interface built with shadcn/ui components
- **Documentation Page**: Comprehensive docs at `/docs` explaining features and technology
- **Layout Components**: Header with Home/Docs navigation, Footer with GitHub and contact links

### 🚧 In Development
- **Live Camera Feed**: Real-time WebRTC/WebSocket streaming from cameras
- **Time-to-Contact (TTC)**: Collision risk calculation and prediction
- **Graded Warning System**: Color-coded threat levels (Green, Yellow, Orange, Red)
- **User Authentication**: Secure login via Supabase Auth
- **Video History**: Database storage and retrieval of past analyses
- **Dashboard Analytics**: Statistical visualizations and trends
- **Multi-camera Support**: Simultaneous monitoring of multiple feeds

## Project Structure Deep Dive

```
SkyLaneAI/
├── apps/
│   ├── web/                          # Next.js Frontend
│   │   ├── app/
│   │   │   ├── page.tsx             # Home/Landing page
│   │   │   ├── layout.tsx           # Root layout with Header/Footer
│   │   │   ├── globals.css          # Global styles
│   │   │   ├── docs/                # Documentation page
│   │   │   │   └── page.tsx
│   │   │   ├── video/               # Video analysis page
│   │   │   │   └── page.tsx
│   │   │   └── stream/              # Live stream page (in progress)
│   │   │       └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/                  # shadcn/ui components
│   │   │   ├── video/
│   │   │   │   ├── video-upload-zone.tsx
│   │   │   │   ├── alert-timeline.tsx
│   │   │   │   ├── video-player-with-detections.tsx
│   │   │   │   └── alert-filters.tsx
│   │   │   └── layout/
│   │   │       ├── header.tsx       # Navigation: Home, Docs
│   │   │       └── footer.tsx       # GitHub link, Contact email
│   │   ├── lib/
│   │   │   └── utils.ts             # Utility functions (cn, etc.)
│   │   ├── public/
│   │   └── package.json
│   │
│   └── api/                          # FastAPI Backend
│       ├── app/
│       │   ├── api/
│       │   │   ├── alert_routes.py  # Alert management endpoints
│       │   │   ├── stream_routes.py # WebRTC streaming (in progress)
│       │   │   └── upload_routes.py # Video upload/processing
│       │   ├── agents/
│       │   │   ├── alert_agent.py   # AI-powered alert generation
│       │   │   ├── context_agent.py # Alert context analysis
│       │   │   └── message_agent.py # Alert message generation
│       │   ├── services/
│       │   │   ├── detection_service.py  # YOLOv11 detection
│       │   │   └── video_service.py      # Video processing
│       │   └── main.py              # FastAPI application
│       ├── temp/                     # Temporary upload storage
│       └── requirements.txt
│
├── pnpm-workspace.yaml
├── package.json
├── .gitignore
├── README.md                         # Project documentation
└── CLAUDE.md                         # This file - development context
```

## Core Components & Responsibilities

### Frontend (Next.js)

**Pages**
- **Home Page** (`/`): Landing page with feature overview and call-to-action buttons
- **Documentation Page** (`/docs`): Comprehensive guide explaining system features, technology stack, and warning levels
- **Video Analysis Page** (`/video`): Upload videos and view real-time detection results
- **Stream Page** (`/stream`): Live camera feed analysis (in progress)

**Video Analysis Features**
- **Video Upload Zone**: Drag-and-drop file upload with FormData submission
- **Video Player with Detections**: HTML5 video player with overlaid bounding boxes
- **Alert Timeline**: Interactive timeline showing all detections with filtering capabilities
- **Alert Filters**: Filter by hazard type (bird, drone, etc.) and severity level
- **Detection Display**: Real-time bounding box overlays synced with video playback

**Layout Components**
- **Header**: Navigation with links to Home (`/`) and Docs (`/docs`)
- **Footer**: Links to GitHub (https://github.com/samiur-r) and Contact (samiur.rahman.akif@gmail.com)

### Backend (FastAPI)

**API Endpoints**
- `POST /upload`: Upload video file for processing
- `POST /analyze`: Analyze uploaded video and return detections
- `GET /alerts/{alert_id}`: Retrieve alert details
- `POST /stream/offer`: WebRTC connection for live streaming (in progress)

**Video Processing Pipeline** (Implemented)
1. Video upload via multipart/form-data
2. Temporary storage in `/temp/uploads/`
3. Video transcoding (if needed)
4. Frame extraction using OpenCV
5. YOLOv11 inference on each frame
6. Detection aggregation and formatting
7. Return JSON with detections and video metadata

**AI-Powered Alert System** (Implemented)
- **Alert Agent**: Orchestrates alert generation workflow
- **Context Agent**: Analyzes detection patterns and provides context
- **Message Agent**: Generates natural language alert descriptions
- Uses Claude API for intelligent alert generation

**YOLOv11 Detection Model**
- Pre-trained YOLOv11 model from Ultralytics
- Detects: person, bicycle, car, motorcycle, airplane, bus, train, truck, bird, etc.
- Confidence threshold: 0.5 (configurable)
- Returns: class, confidence, bounding box coordinates

**Future: Time-to-Contact Algorithm** (Planned)
```python
# Planned implementation
def calculate_ttc(detection, previous_detection, fps, camera_params):
    # Calculate object size change
    size_current = detection.bbox_area
    size_previous = previous_detection.bbox_area

    # Estimate depth and approach speed
    depth_ratio = size_previous / size_current
    time_delta = 1 / fps
    approach_speed = (depth_ratio - 1) / time_delta

    # Calculate TTC
    ttc = estimate_distance(detection) / approach_speed
    return ttc, calculate_warning_level(ttc)
```

## Data Storage

### Current Implementation
Currently, the application uses **file-based storage** without a persistent database:

**Video Storage**
- Uploaded videos are stored temporarily in `apps/api/temp/uploads/`
- Files are transcoded if necessary (e.g., H.264 codec conversion)
- Video files are accessed directly by the frontend via file path

**Detection Data**
- Detections are computed on-demand during video analysis
- Results are returned as JSON in the API response
- No persistent storage of detection history

**Alert Data**
- Alerts are generated dynamically using AI agents
- Stored temporarily during the analysis session
- No long-term storage or history

### Future Database Schema (Supabase - Planned)

When implementing persistent storage, the following schema will be used:

**videos**
```sql
CREATE TABLE videos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  file_path TEXT NOT NULL,
  duration FLOAT,
  fps FLOAT,
  resolution TEXT,
  status TEXT CHECK (status IN ('uploading', 'processing', 'completed', 'failed')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**detections**
```sql
CREATE TABLE detections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
  frame_number INT NOT NULL,
  timestamp FLOAT NOT NULL,
  class TEXT NOT NULL,
  confidence FLOAT NOT NULL,
  bbox_x FLOAT NOT NULL,
  bbox_y FLOAT NOT NULL,
  bbox_width FLOAT NOT NULL,
  bbox_height FLOAT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**alerts**
```sql
CREATE TABLE alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
  severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  message TEXT NOT NULL,
  context TEXT,
  acknowledged BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Development Guidelines

### Code Style

**TypeScript/JavaScript**
- Use functional components with hooks
- Prefer named exports over default exports
- Use const for immutable values
- Implement proper error boundaries
- Add JSDoc comments for complex functions

**Python**
- Follow PEP 8 style guide
- Use type hints for all functions
- Async/await for I/O operations
- Proper exception handling
- Docstrings for all public functions

### Component Patterns

**React Components**
```typescript
// components/video/video-player.tsx
interface VideoPlayerProps {
  videoUrl: string;
  detections: Detection[];
  onTimeUpdate?: (time: number) => void;
}

export function VideoPlayer({
  videoUrl,
  detections,
  onTimeUpdate
}: VideoPlayerProps) {
  // Implementation
}
```

**FastAPI Routers**
```python
# routers/videos.py
from fastapi import APIRouter, Depends, UploadFile
from app.schemas.video import VideoResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/videos", tags=["videos"])

@router.post("/upload", response_model=VideoResponse)
async def upload_video(
    file: UploadFile,
    user = Depends(get_current_user)
):
    # Implementation
    pass
```

### State Management

**Frontend State**
- React Context for global state (auth, theme)
- React Query for server state (videos, detections)
- Local state for UI interactions
- Supabase Realtime for live updates

**Backend State**
- Stateless API design
- Database as source of truth
- Redis for caching (optional, future)
- WebSocket for real-time connections

### Testing Strategy

**Frontend Tests**
- Unit: Jest + React Testing Library
- Integration: Playwright
- E2E: Playwright with real Supabase instance

**Backend Tests**
- Unit: pytest with mocking
- Integration: pytest with test database
- Load: Locust for performance testing

### Security Considerations

**Authentication**
- Supabase Auth with JWT tokens
- Refresh token rotation
- MFA support (optional)

**Authorization**
- Row Level Security (RLS) in Supabase
- API endpoint guards with dependencies
- Role-based access control (RBAC)

**Data Privacy**
- Video encryption at rest (Supabase Storage)
- HTTPS for all communications
- GDPR compliance (data deletion)

**API Security**
- Rate limiting (FastAPI middleware)
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention (ORM/parameterized queries)

## Performance Optimization

### Frontend
- Image optimization with Next.js Image
- Code splitting with dynamic imports
- Lazy loading for components
- Memoization for expensive computations
- Virtual scrolling for large lists

### Backend
- Async video processing
- Batch inference for efficiency
- WebSocket for real-time data
- Database query optimization (indexes)
- CDN for video delivery

### ML Model
- TensorRT optimization (GPU)
- Model quantization (INT8)
- Batch processing where possible
- Frame sampling for non-critical scenarios

## Deployment Considerations

**Frontend (Vercel)**
- Automatic deployments from main branch
- Preview deployments for PRs
- Environment variables in Vercel dashboard
- Edge functions for API routes

**Backend (Options)**
1. **Docker + Cloud Run**: Serverless containers
2. **AWS EC2 + GPU**: Dedicated inference server
3. **Kubernetes**: Scalable cluster deployment

**Database (Supabase)**
- Production instance with backups
- Connection pooling (PgBouncer)
- Read replicas for scaling

## Monitoring & Observability

**Application Monitoring**
- Error tracking: Sentry
- Performance: Vercel Analytics
- Logs: Supabase Logs + CloudWatch

**Model Monitoring**
- Inference latency tracking
- Detection accuracy metrics
- False positive/negative rates
- Model drift detection

## Future Enhancements

**Phase 2**
- Mobile app (React Native)
- Advanced analytics dashboard
- Multi-model ensemble
- 3D trajectory prediction

**Phase 3**
- Weather integration
- Drone traffic management integration
- Predictive hazard modeling
- Real-time notification system (SMS/Push)

## API Design Principles

**RESTful Conventions**
- Noun-based endpoints
- Proper HTTP methods (GET, POST, PUT, DELETE)
- Meaningful status codes
- Pagination for list endpoints

**Response Format**
```json
{
  "success": true,
  "data": {},
  "error": null,
  "meta": {
    "page": 1,
    "total": 100
  }
}
```

**Versioning**
- URL-based versioning: `/api/v1/`
- Maintain backward compatibility
- Deprecation notices in headers

## Common Development Tasks

### Adding a New Hazard Type
1. Update YOLOv11 training data
2. Retrain model with new class
3. Update detection schema
4. Add UI components for new type
5. Update documentation

### Adding a New API Endpoint
1. Define Pydantic schema
2. Create router function
3. Add authentication/authorization
4. Write unit tests
5. Update API documentation

### Adding a New UI Component
1. Create component with TypeScript
2. Add to shadcn/ui if reusable
3. Write Storybook story (optional)
4. Add unit tests
5. Document props with JSDoc

## Troubleshooting

**Video Upload Issues**
- Check Supabase Storage bucket policies
- Verify file size limits
- Ensure correct MIME types

**Detection Accuracy Problems**
- Verify model confidence threshold
- Check lighting conditions in video
- Ensure model is loaded correctly
- Review training data quality

**Performance Issues**
- Profile with browser DevTools
- Check database query performance
- Monitor GPU utilization
- Review video resolution/bitrate

## Current User Workflow

1. **Landing** → User visits home page at `/`
2. **Navigation** → Clicks "Upload Video" button or navigates to `/video`
3. **Upload** → Drags and drops video file or clicks to browse
4. **Processing** → Video is uploaded to backend, transcoded if needed, and analyzed with YOLOv11
5. **Results** → Detection results displayed with:
   - Video player with bounding box overlays
   - Interactive alert timeline
   - Filter controls by hazard type and severity
   - AI-generated alert descriptions
6. **Review** → User can scrub through video, filter alerts, and review detections

## Key Configuration

**Frontend Environment Variables** (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend Configuration**
- FastAPI runs on port 8000
- YOLOv11 model: `yolo11n.pt` (nano version)
- Video storage: `apps/api/temp/uploads/`
- Supported formats: MP4, AVI, MOV, MKV
- Max file size: Limited by system memory

## Resources

**Documentation**
- Next.js: https://nextjs.org/docs
- FastAPI: https://fastapi.tiangolo.com
- YOLOv11: https://docs.ultralytics.com
- shadcn/ui: https://ui.shadcn.com
- Tailwind CSS: https://tailwindcss.com/docs

**Project Links**
- GitHub Repository: https://github.com/samiur-r/SkyLaneAI
- Issues: https://github.com/samiur-r/SkyLaneAI/issues
- Contact: samiur.rahman.akif@gmail.com

---

This document should be updated as the project evolves. When making significant architectural changes, update this file to reflect the new design decisions.

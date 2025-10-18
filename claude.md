# SkyLaneAI v2 - Claude Development Context

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

## Project Structure Deep Dive

```
SkylaneAI-v2/
├── apps/
│   ├── web/                          # Next.js Frontend
│   │   ├── app/
│   │   │   ├── (auth)/              # Auth route group
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   ├── (dashboard)/         # Dashboard route group
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── page.tsx
│   │   │   │   ├── videos/
│   │   │   │   ├── live/
│   │   │   │   ├── analytics/
│   │   │   │   └── settings/
│   │   │   ├── api/                 # API routes
│   │   │   │   └── webhook/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/                  # shadcn/ui components
│   │   │   ├── video/
│   │   │   │   ├── video-player.tsx
│   │   │   │   ├── video-uploader.tsx
│   │   │   │   └── detection-overlay.tsx
│   │   │   ├── hazards/
│   │   │   │   ├── hazard-card.tsx
│   │   │   │   ├── ttc-indicator.tsx
│   │   │   │   └── warning-badge.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── stats-card.tsx
│   │   │   │   └── detection-chart.tsx
│   │   │   └── layout/
│   │   │       ├── header.tsx
│   │   │       ├── sidebar.tsx
│   │   │       └── footer.tsx
│   │   ├── lib/
│   │   │   ├── supabase/
│   │   │   │   ├── client.ts
│   │   │   │   ├── server.ts
│   │   │   │   └── middleware.ts
│   │   │   ├── hooks/
│   │   │   │   ├── use-video-upload.ts
│   │   │   │   ├── use-detections.ts
│   │   │   │   └── use-realtime.ts
│   │   │   └── utils.ts
│   │   ├── public/
│   │   ├── styles/
│   │   └── package.json
│   │
│   └── api/                          # FastAPI Backend
│       ├── app/
│       │   ├── core/
│       │   │   ├── config.py        # Configuration management
│       │   │   ├── security.py      # Auth & security
│       │   │   └── dependencies.py  # FastAPI dependencies
│       │   ├── models/
│       │   │   ├── detection.py     # YOLOv11 integration
│       │   │   ├── ttc.py          # Time-to-Contact calculations
│       │   │   └── video.py        # Video processing
│       │   ├── routers/
│       │   │   ├── __init__.py
│       │   │   ├── videos.py       # Video upload/processing
│       │   │   ├── detections.py   # Hazard detection
│       │   │   ├── streams.py      # Live camera feeds
│       │   │   └── auth.py         # Authentication
│       │   ├── schemas/
│       │   │   ├── video.py
│       │   │   ├── detection.py
│       │   │   └── user.py
│       │   ├── services/
│       │   │   ├── supabase.py     # Supabase integration
│       │   │   ├── video_processor.py
│       │   │   └── notification.py
│       │   └── main.py
│       ├── scripts/
│       │   ├── download_model.py
│       │   └── train_model.py
│       ├── tests/
│       ├── requirements.txt
│       └── Dockerfile
│
├── packages/
│   ├── types/                        # Shared TypeScript types
│   │   ├── index.ts
│   │   ├── hazard.ts
│   │   ├── detection.ts
│   │   └── video.ts
│   ├── config/                       # Shared configs
│   │   ├── eslint-config/
│   │   └── tsconfig/
│   └── utils/                        # Shared utilities
│
├── supabase/
│   ├── migrations/
│   │   ├── 20240101000000_initial_schema.sql
│   │   ├── 20240101000001_add_videos_table.sql
│   │   ├── 20240101000002_add_detections_table.sql
│   │   └── 20240101000003_add_rls_policies.sql
│   ├── functions/                    # Edge functions
│   └── config.toml
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── pnpm-workspace.yaml
├── package.json
├── turbo.json
├── .gitignore
├── README.md
└── claude.md
```

## Core Components & Responsibilities

### Frontend (Next.js)

**Video Player with Detection Overlay**
- Display video with real-time bounding boxes
- Color-coded overlays based on TTC warnings
- Frame-by-frame scrubbing with detection timeline
- Performance optimized with Canvas API

**Video Uploader**
- Drag-and-drop interface
- Progress tracking with chunked uploads
- Supabase Storage integration
- Format validation (MP4, AVI, MOV)

**Live Stream Monitor**
- WebRTC/WebSocket connection to camera feeds
- Real-time detection overlay
- Multi-camera grid view
- Alert notifications for critical warnings

**Dashboard & Analytics**
- Detection history and statistics
- Hazard type distribution charts
- TTC trend analysis
- Export functionality for reports

### Backend (FastAPI)

**Video Processing Pipeline**
1. Video upload to Supabase Storage
2. Frame extraction (OpenCV)
3. Batch inference with YOLOv11
4. Detection post-processing
5. TTC calculation for each hazard
6. Results stored in database

**Real-time Stream Processing**
1. WebSocket/RTSP stream ingestion
2. Frame buffering and sampling
3. Concurrent inference (async)
4. Real-time results broadcast
5. Alert generation for critical TTC

**YOLOv11 Detection Model**
- Custom trained on sky hazard dataset
- Classes: bird, drone, balloon, kite (with subclasses)
- Confidence threshold: 0.5 (configurable)
- IOU threshold: 0.45 for NMS
- GPU inference for real-time performance

**Time-to-Contact Algorithm**
```python
# Pseudocode
def calculate_ttc(detection, previous_detection, fps, camera_params):
    # Calculate object size change (using bounding box)
    size_current = detection.bbox_area
    size_previous = previous_detection.bbox_area

    # Estimate depth using similar triangles
    depth_ratio = size_previous / size_current

    # Calculate approach speed
    time_delta = 1 / fps
    approach_speed = (depth_ratio - 1) / time_delta

    # TTC = distance / speed
    ttc = estimate_distance(detection) / approach_speed

    return ttc, calculate_warning_level(ttc)
```

## Database Schema

### Tables

**users**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

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
  created_at TIMESTAMPTZ DEFAULT NOW(),
  processed_at TIMESTAMPTZ
);
```

**detections**
```sql
CREATE TABLE detections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
  frame_number INT NOT NULL,
  timestamp FLOAT NOT NULL,
  hazard_type TEXT NOT NULL,
  confidence FLOAT NOT NULL,
  bbox_x FLOAT NOT NULL,
  bbox_y FLOAT NOT NULL,
  bbox_width FLOAT NOT NULL,
  bbox_height FLOAT NOT NULL,
  ttc FLOAT,
  warning_level TEXT CHECK (warning_level IN ('green', 'yellow', 'orange', 'red')),
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**camera_feeds**
```sql
CREATE TABLE camera_feeds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  stream_url TEXT NOT NULL,
  status TEXT CHECK (status IN ('active', 'inactive', 'error')),
  last_active TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**alerts**
```sql
CREATE TABLE alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  detection_id UUID REFERENCES detections(id) ON DELETE CASCADE,
  camera_feed_id UUID REFERENCES camera_feeds(id),
  severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  acknowledged BOOLEAN DEFAULT FALSE,
  acknowledged_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Row Level Security (RLS)

Enable RLS on all tables and create policies:
```sql
-- Users can only access their own data
CREATE POLICY "Users can view own videos"
  ON videos FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own videos"
  ON videos FOR INSERT
  WITH CHECK (auth.uid() = user_id);
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

## Resources

**Documentation**
- Next.js: https://nextjs.org/docs
- FastAPI: https://fastapi.tiangolo.com
- YOLOv11: https://docs.ultralytics.com
- Supabase: https://supabase.com/docs
- shadcn/ui: https://ui.shadcn.com

**Community**
- GitHub Discussions
- Discord Server (TBD)
- Stack Overflow tag: `skylaneai`

---

This document should be updated as the project evolves. When making significant architectural changes, update this file to reflect the new design decisions.

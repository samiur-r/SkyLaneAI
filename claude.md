# SkyLaneAI v2 - Claude Development Context

**Last Updated**: 2025-11-03

## Project Vision

SkyLaneAI v2 is a safety-critical system designed to protect flying taxis and other aerial vehicles from sky hazards. The system analyzes video feeds to detect birds, drones, balloons, and kites, providing intelligent AI-powered alerts through a sophisticated multi-agent system.

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
- Pre-trained YOLOv11 model from Ultralytics
- Real-time inference capabilities
- Detects COCO classes: bird, kite, airplane, sports ball
- Efficient GPU/CPU utilization

**AI Multi-Agent System: LangGraph + OpenAI**
- **LangGraph**: Orchestrates agent workflow
- **OpenAI GPT**: Powers intelligent decision-making
- **Specialized Agents**:
  - **Context Agent** (Rule-based): Analyzes detection patterns, size, position, and calculates initial threat levels
  - **Action Agent** (LLM-powered): Provides actionable pilot recommendations
  - **Message Agent** (LLM-powered): Generates natural language alert messages
  - **Priority Agent** (Rule-based): Scores and ranks alerts by urgency

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
- **Multi-Agent AI System**: Four specialized agents working together:
  - Context enrichment with size/position/threat analysis
  - LLM-powered action recommendations for pilots
  - Natural language message generation
  - Priority scoring and alert ranking
- **Responsive UI**: Modern interface built with shadcn/ui components
- **Documentation Page**: Comprehensive docs at `/docs` explaining features and technology
- **Layout Components**: Header with Home/Docs navigation, Footer with GitHub and contact links

### 🚧 In Development
- **Live Camera Feed**: Real-time WebRTC/WebSocket streaming from cameras
- **Time-to-Contact (TTC)**: Collision risk calculation and prediction
- **Graded Warning System**: Color-coded threat levels (Green, Yellow, Orange, Red)
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
│       │   │   ├── routes.py        # Main video processing routes
│       │   │   ├── alert_routes.py  # Alert generation endpoints
│       │   │   ├── video_routes.py  # Video upload endpoints
│       │   │   └── stream_routes.py # WebRTC streaming (in progress)
│       │   ├── agents/
│       │   │   ├── context_agent.py # Rule-based context enrichment
│       │   │   ├── action_agent.py  # LLM-powered action recommendations
│       │   │   ├── message_agent.py # LLM-powered message generation
│       │   │   └── priority_agent.py # Rule-based priority scoring
│       │   ├── services/
│       │   │   ├── detector.py      # YOLOv11 detection service
│       │   │   ├── video_file_processor.py  # Video processing
│       │   │   ├── video_stream.py  # Stream handling (in progress)
│       │   │   └── webrtc_handler.py # WebRTC (in progress)
│       │   ├── models/
│       │   │   └── schemas.py       # Pydantic models
│       │   ├── core/
│       │   │   └── config.py        # Configuration
│       │   └── main.py              # FastAPI application
│       ├── temp/                    # Temporary upload storage
│       └── requirements.txt
│
├── pnpm-workspace.yaml
├── package.json
├── .gitignore
├── README.md                        # Project documentation
└── CLAUDE.md                        # This file - development context
```

## Multi-Agent System Architecture

### Agent Workflow

```
Video Frame → YOLOv11 Detection → Multi-Agent Pipeline → Alert
```

**1. Context Agent (Rule-based)**
- Analyzes bounding box size and calculates area
- Determines screen position (upper-left, center, etc.)
- Estimates size category (small, medium, large)
- Calculates initial threat level (low, moderate, high, critical)
- Fast, deterministic, no API costs

**2. Action Agent (LLM-powered via OpenAI)**
- Receives detection + enriched context
- Generates PRIMARY and SECONDARY action recommendations
- Provides REASONING for recommendations
- Determines URGENCY level (advisory, caution, urgent, immediate)
- Uses aviation safety protocols

**3. Message Agent (LLM-powered via OpenAI)**
- Creates natural language alert messages
- Formats message with title, emoji, and structured sections
- Includes Detection Details and Threat Assessment
- Generates fallback messages if LLM fails
- Professional, aviation-focused tone

**4. Priority Agent (Rule-based)**
- Scores alerts using weighted system:
  - Threat level (40%)
  - Action urgency (30%)
  - Confidence (20%)
  - Size (10%)
- Ranks multiple alerts by priority
- Helps pilots focus on critical threats first

### Agent Communication

Agents communicate through Pydantic schemas:
- `Detection`: Raw YOLOv11 output
- `EnrichedContext`: Context agent output
- `ActionRecommendation`: Action agent output
- `CraftedMessage`: Message agent output
- `PriorityScore`: Priority agent output

### Configuration

LLM agents use:
- Model: Configurable via `OPENAI_MODEL` (default: gpt-4o-mini)
- Temperature: Low (0.2-0.3) for consistent safety recommendations
- Timeout: Configurable via `ALERT_GENERATION_TIMEOUT`
- Fallback: Rule-based logic if LLM fails

## Core Components & Responsibilities

### Frontend (Next.js)

**Pages**
- **Home Page** (`/`): Landing page with feature overview
- **Documentation Page** (`/docs`): Comprehensive guide
- **Video Analysis Page** (`/video`): Upload and analyze videos
- **Stream Page** (`/stream`): Live camera feed (in progress)

**Video Analysis Features**
- **Video Upload Zone**: Drag-and-drop file upload
- **Video Player with Detections**: HTML5 video player with overlaid bounding boxes
- **Alert Timeline**: Interactive timeline with filtering
- **Alert Filters**: Filter by hazard type and severity
- **Detection Display**: Real-time bounding box overlays

**Layout Components**
- **Header**: Navigation to Home (`/`) and Docs (`/docs`)
- **Footer**: GitHub link and contact email

### Backend (FastAPI)

**API Endpoints**
- `POST /process-video`: Upload and analyze video
- `POST /generate-alert`: Generate AI alert for detection
- `GET /health`: Health check endpoint

**Video Processing Pipeline**
1. Video upload via multipart/form-data
2. Temporary storage in `/temp/uploads/`
3. Frame extraction using OpenCV
4. YOLOv11 inference on each frame
5. Detection aggregation and formatting
6. Return JSON with detections and metadata

**Alert Generation Pipeline**
1. Receive detection data
2. Context Agent enriches with contextual analysis
3. Action Agent generates pilot recommendations (LLM)
4. Message Agent crafts natural language alert (LLM)
5. Priority Agent scores alert urgency
6. Return complete alert with all components

**YOLOv11 Detection**
- Model: `yolo11n.pt` (nano) or configurable
- Detects: bird, kite, airplane, sports ball
- Confidence threshold: 0.25 (configurable)
- Returns: class, confidence, bounding box coordinates

## Data Storage

### Current Implementation
File-based storage without persistent database:

**Video Storage**
- Uploaded videos stored temporarily in `apps/api/temp/uploads/`
- Videos accessible directly by frontend via file path
- Automatic cleanup recommended (not currently implemented)

**Detection Data**
- Computed on-demand during video analysis
- Results returned as JSON in API response
- No persistent storage

**Alert Data**
- Generated dynamically using AI agents
- Stored temporarily during analysis session
- No long-term storage

### Future Enhancements (Planned)
- Cloud storage integration (S3, Azure Blob)
- Time-series database for detection patterns
- Alert history and acknowledgment tracking

## Development Guidelines

### Code Style

**TypeScript/JavaScript**
- Use functional components with hooks
- Prefer named exports over default exports
- Implement proper error boundaries
- Add JSDoc comments for complex functions

**Python**
- Follow PEP 8 style guide
- Use type hints for all functions
- Async/await for I/O operations
- Proper exception handling
- Docstrings for all public functions

### Testing Strategy

**Frontend Tests**
- Unit: Jest + React Testing Library
- Integration: Playwright
- E2E: Playwright

**Backend Tests**
- Unit: pytest with mocking
- Integration: pytest with test video files
- Load: Locust for performance testing

### Security Considerations

**API Security**
- Rate limiting (planned)
- CORS configuration
- Input validation with Pydantic
- Secure API key management (OpenAI)

**Data Privacy**
- Temporary file storage
- HTTPS for all communications
- No persistent user data currently

## Performance Optimization

### Frontend
- Image optimization with Next.js Image
- Code splitting with dynamic imports
- Lazy loading for components
- Memoization for expensive computations

### Backend
- Async video processing
- Model caching (YOLO models cached locally)
- Frame sampling for efficiency
- LLM timeout handling

### ML Model
- YOLOv11 nano for speed (or configurable variant)
- GPU acceleration when available
- Batch processing where possible

## Environment Variables

### Frontend (.env.local in apps/web)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env in apps/api)
```env
# OpenAI API for alert generation
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
ALERT_GENERATION_TIMEOUT=30

# Model configuration
MODEL_NAME=yolo11n.pt
MODELS_DIR=models
MODEL_CACHE_ENABLED=true
MODEL_DEVICE=cpu
CONFIDENCE_THRESHOLD=0.25
IOU_THRESHOLD=0.45

# Sky hazard classes
SKY_HAZARD_CLASSES=["bird", "kite", "airplane", "sports ball"]

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Video settings
MAX_UPLOAD_SIZE=10485760  # 10MB
DEFAULT_PROCESS_FPS=10
```

## Common Development Tasks

### Adding a New Agent
1. Create agent class in `apps/api/app/agents/`
2. Define input/output schemas in `models/schemas.py`
3. Implement agent logic (rule-based or LLM-powered)
4. Add agent to workflow in alert routes
5. Write unit tests
6. Update documentation

### Adding a New API Endpoint
1. Define Pydantic schema in `models/schemas.py`
2. Create router function in `api/`
3. Add route to `main.py`
4. Write unit tests
5. Update API documentation

### Adding a New UI Component
1. Create component in `apps/web/components/`
2. Add to shadcn/ui if reusable
3. Import and use in pages
4. Add unit tests
5. Document props with JSDoc

## Troubleshooting

**Video Upload Issues**
- Verify temp directory exists: `apps/api/temp/uploads/`
- Check file size limits (10MB default)
- Ensure correct MIME types (mp4, avi, mov, mkv)

**Detection Issues**
- Verify YOLO model downloaded in `models/` directory
- Check confidence threshold (default: 0.25)
- Review SKY_HAZARD_CLASSES configuration

**Alert Generation Issues**
- Verify OPENAI_API_KEY is set
- Check OpenAI API quota/rate limits
- Review timeout settings (default: 30s)
- Check fallback messages if LLM fails

## Current User Workflow

1. **Landing** → User visits home page at `/`
2. **Navigation** → Clicks "Upload Video" or navigates to `/video`
3. **Upload** → Drags and drops video file
4. **Processing** → Video analyzed with YOLOv11
5. **AI Alert Generation** → Multi-agent system generates intelligent alerts
6. **Results** → User sees:
   - Video player with bounding boxes
   - Interactive alert timeline
   - AI-generated alert messages with:
     - Natural language descriptions
     - Actionable pilot recommendations
     - Priority scores
     - Threat assessments
   - Filter controls

## Resources

**Documentation**
- Next.js: https://nextjs.org/docs
- FastAPI: https://fastapi.tiangolo.com
- YOLOv11: https://docs.ultralytics.com
- shadcn/ui: https://ui.shadcn.com
- LangGraph: https://langchain-ai.github.io/langgraph/
- OpenAI API: https://platform.openai.com/docs

**Project Links**
- GitHub: https://github.com/samiur-r/SkyLaneAI
- Issues: https://github.com/samiur-r/SkyLaneAI/issues
- Contact: samiur.rahman.akif@gmail.com

---

**Note**: TTC (Time-to-Contact) calculation and graded warning system (Green/Yellow/Orange/Red) are planned features, not yet implemented. Current implementation focuses on detection and AI-powered alert generation.

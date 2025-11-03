# SkyLaneAI v2

**Sky Hazard Detection with Collision Risk Assessment for Flying Taxis**

## Overview

SkyLaneAI is an intelligent video analysis system designed to detect sky hazards (birds, drones, balloons, kites) from uploaded videos and live camera feeds. The system provides real-time overlays with bounding boxes and graded warnings using Time-to-Contact (TTC) calculations to ensure safe navigation for flying taxis and other aerial vehicles.

## Tech Stack

### Frontend
- **Next.js** (Latest) - React framework with App Router
- **shadcn/ui** - High-quality, accessible UI components
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling

### Backend
- **FastAPI** - High-performance Python web framework
- **YOLO-World** - Open-vocabulary object detection (zero-shot)
- **OpenCV** - Video processing and computer vision
- **LangGraph** - AI agent framework for intelligent alerts
- **OpenAI API** - Context-aware alert generation

### Infrastructure
- **pnpm** - Fast, disk-efficient package manager
- **Monorepo** - Unified workspace architecture

## Project Structure

```
SkyLaneAI/
├── apps/
│   ├── web/                    # Next.js frontend application
│   │   ├── app/                # App Router pages
│   │   ├── components/         # React components
│   │   ├── lib/                # Utilities and helpers
│   │   └── public/             # Static assets
│   └── api/                    # FastAPI backend
│       ├── app/
│       │   ├── core/           # Core configuration
│       │   ├── models/         # ML models and detection
│       │   ├── routers/        # API endpoints
│       │   ├── services/       # Business logic
│       │   └── main.py         # FastAPI application
│       └── requirements.txt
├── packages/
│   ├── types/                  # Shared TypeScript types
│   └── config/                 # Shared configurations
├── pnpm-workspace.yaml
├── package.json
└── README.md
```

## Features

### ✅ Currently Implemented
- **Video Upload & Processing**: Upload and analyze pre-recorded videos for hazard detection
- **Real-time Detection Display**: View detected hazards with bounding boxes and labels
- **Alert Timeline**: Interactive timeline showing all detections throughout the video
- **Detection Filtering**: Filter alerts by hazard type and severity level
- **AI-Powered Alerts**: Intelligent, context-aware alert messages using LangGraph agents
- **Responsive UI**: Modern, accessible interface built with shadcn/ui components
- **Documentation**: Comprehensive docs page explaining the system and technology

### 🚧 In Development
- **Live Camera Feed**: Real-time analysis of camera feeds via WebRTC
- **Time-to-Contact (TTC)**: Calculate collision risk and warning levels
- **Graded Warnings**: Color-coded threat levels (Green, Yellow, Orange, Red)
- **Dashboard Analytics**: Visualize detection statistics and patterns
- **Multi-camera Support**: Monitor multiple feeds simultaneously

## Prerequisites

- **Node.js** >= 20.x
- **pnpm** >= 9.x
- **Python** >= 3.11
- **OpenAI API Key** (for AI-powered alert generation)
- **GPU** (recommended for YOLOv11 inference)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/samiur-r/SkyLaneAI.git
cd SkyLaneAI
```

### 2. Install Dependencies

```bash
# Install pnpm globally if not already installed
npm install -g pnpm

# Install all workspace dependencies
pnpm install
```

### 3. Environment Setup

#### Frontend (.env.local in apps/web)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Backend (.env in apps/api)
```env
# OpenAI API for alert generation
OPENAI_API_KEY=your_openai_api_key

# Model configuration
MODEL_NAME=yolo11l.pt
MODELS_DIR=models
MODEL_CACHE_ENABLED=true
MODEL_DEVICE=cpu
CONFIDENCE_THRESHOLD=0.25
IOU_THRESHOLD=0.45

# Sky hazard classes to detect
SKY_HAZARD_CLASSES=["bird", "kite", "airplane", "sports ball"]

# CORS configuration
CORS_ORIGINS=["http://localhost:3000"]
```

### 4. Backend Setup (FastAPI)

```bash
cd apps/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# The YOLOv11 model will be downloaded automatically on first run
```

### 5. Run Development Servers

#### Terminal 1: Frontend
```bash
pnpm --filter web dev
```

#### Terminal 2: Backend
```bash
cd apps/api
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Available Pages
- **Home** (`/`): Landing page with feature overview
- **Video Analysis** (`/video`): Upload and analyze videos for hazard detection
- **Live Stream** (`/stream`): Real-time camera feed analysis (coming soon)
- **Documentation** (`/docs`): Complete guide to SkyLaneAI features and technology

## API Endpoints

### Video Processing
- `POST /upload` - Upload video file for analysis
- `POST /analyze` - Analyze uploaded video and return detections

### Alert Generation
- `POST /alerts/generate` - Generate AI-powered context-aware alerts
- `GET /alerts/{alert_id}` - Retrieve specific alert details

### WebRTC Streaming (In Development)
- `POST /stream/offer` - Initiate WebRTC connection for live feed

## YOLOv11 Integration

The system uses YOLOv11 for object detection, leveraging the COCO dataset classes:

### Detected Sky Hazard Classes
The system filters YOLO detections to focus on sky hazards:
- **bird** - Birds of various sizes and flocks
- **kite** - Kites and similar flying objects
- **airplane** - Aircraft and potentially drones
- **sports ball** - May detect balloons

### Model Configuration
The default model is `yolo11l.pt` (large variant) for accuracy. You can switch to other variants in `.env`:
- `yolo11n.pt` - Nano (fastest, smallest)
- `yolo11s.pt` - Small
- `yolo11m.pt` - Medium
- `yolo11l.pt` - Large (default, good balance)
- `yolo11x.pt` - Extra Large (most accurate, slowest)

## Time-to-Contact (TTC) Algorithm

TTC is calculated using:
```
TTC = Distance / Relative_Velocity
```

Warning levels:
- **Green**: TTC > 10 seconds (Safe)
- **Yellow**: 5 < TTC ≤ 10 seconds (Monitor)
- **Orange**: 2 < TTC ≤ 5 seconds (Caution)
- **Red**: TTC ≤ 2 seconds (Critical)

## Deployment

### Frontend (Vercel)

**Quick Deploy:**
1. Push your code to GitHub
2. Go to [Vercel](https://vercel.com/new)
3. Import your repository
4. Vercel auto-detects Next.js configuration
5. Add environment variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-api.onrender.com
   ```
6. Deploy!

**Manual build:**
```bash
pnpm --filter web build
vercel --prod
```

### Backend (Render)

**Option 1: Blueprint Deployment (Recommended)**
1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Render auto-detects `render.yaml` in the root
6. Set environment variables when prompted:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `CORS_ORIGINS`: `["https://your-app.vercel.app"]`
7. Click "Apply" and wait 5-10 minutes

**Option 2: Manual Deployment**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: skylaneai-api
   - **Root Directory**: `apps/api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as above)
6. Click "Create Web Service"

**Important Notes:**
- Free tier spins down after 15 min of inactivity
- First request after spin-down takes 30-60s
- YOLO model downloads on first request (~30s)
- See [apps/api/DEPLOYMENT.md](apps/api/DEPLOYMENT.md) for detailed guide

## Development

### Code Quality
```bash
# Linting
pnpm lint

# Type checking
pnpm type-check

# Formatting
pnpm format
```

### Testing
```bash
# Frontend tests
pnpm --filter web test

# Backend tests
cd apps/api
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- YOLOv11 by Ultralytics
- Next.js team for the excellent framework
- shadcn for beautiful UI components
- OpenAI for GPT models powering intelligent alerts
- LangGraph for AI agent orchestration

## Support

For issues and questions:
- GitHub Issues: https://github.com/samiur-r/SkyLaneAI/issues
- Documentation: Available at `/docs` in the application
- Email: samiur.rahman.akif@gmail.com

## Roadmap

- [ ] Multi-model ensemble for improved accuracy
- [ ] 3D trajectory prediction
- [ ] Weather integration for enhanced risk assessment
- [ ] Mobile app for iOS and Android
- [ ] Integration with drone traffic management systems
- [ ] Advanced analytics dashboard
- [ ] Real-time notification system
- [ ] API for third-party integrations

---

Built with passion for aviation safety 🚁✨

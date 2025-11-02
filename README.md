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
- **Supabase Client** - Real-time data and authentication

### Backend
- **FastAPI** - High-performance Python web framework
- **YOLOv11** - State-of-the-art object detection model
- **OpenCV** - Video processing and computer vision
- **Supabase** - Database, authentication, and storage

### Infrastructure
- **pnpm** - Fast, disk-efficient package manager
- **Monorepo** - Unified workspace architecture
- **Supabase** - Backend-as-a-Service platform

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
├── supabase/
│   ├── migrations/             # Database migrations
│   └── config.toml             # Supabase configuration
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
- **Responsive UI**: Modern, accessible interface built with shadcn/ui components
- **Documentation**: Comprehensive docs page explaining the system and technology

### 🚧 In Development
- **Live Camera Feed**: Real-time analysis of camera feeds
- **Time-to-Contact (TTC)**: Calculate collision risk and warning levels
- **Graded Warnings**: Color-coded threat levels (Green, Yellow, Orange, Red)
- **User Authentication**: Secure login and user management via Supabase
- **Video History**: Store and review past analyses
- **Dashboard Analytics**: Visualize detection statistics and patterns
- **Multi-camera Support**: Monitor multiple feeds simultaneously

## Prerequisites

- **Node.js** >= 20.x
- **pnpm** >= 9.x
- **Python** >= 3.11
- **Supabase Account** (for backend services)
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
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Backend (.env in apps/api)
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key
MODEL_PATH=./models/yolov11.pt
CONFIDENCE_THRESHOLD=0.5
IOU_THRESHOLD=0.45
```

### 4. Supabase Setup

```bash
# Initialize Supabase (if not already done)
npx supabase init

# Link to your Supabase project
npx supabase link --project-ref your-project-ref

# Push database migrations
npx supabase db push
```

### 5. Backend Setup (FastAPI)

```bash
cd apps/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Download YOLOv11 model (if not included)
python scripts/download_model.py
```

### 6. Run Development Servers

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
- `POST /api/v1/upload` - Upload video for analysis
- `POST /api/v1/analyze/stream` - Start live stream analysis
- `GET /api/v1/detections/{video_id}` - Get detection results

### Hazard Detection
- `POST /api/v1/detect` - Real-time frame detection
- `GET /api/v1/hazards/types` - List supported hazard types
- `POST /api/v1/ttc/calculate` - Calculate Time-to-Contact

### User Management
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/user/history` - Get user's analysis history

## Database Schema

### Key Tables
- `users` - User accounts and profiles
- `videos` - Uploaded and processed videos
- `detections` - Detected hazards with metadata
- `camera_feeds` - Live camera feed configurations
- `alerts` - TTC-based warning alerts

## YOLOv11 Integration

The system uses YOLOv11 for object detection with custom training on sky hazards:

### Supported Hazard Classes
1. Bird (small, medium, large flocks)
2. Drone (consumer, commercial)
3. Balloon (party, weather)
4. Kite (recreational, sport)

### Model Training
```bash
cd apps/api
python scripts/train_model.py --data config/hazards.yaml --epochs 100
```

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
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
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

### Supabase
Production database and authentication are managed through [Supabase dashboard](https://supabase.com/dashboard).

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
- Supabase for the backend infrastructure

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

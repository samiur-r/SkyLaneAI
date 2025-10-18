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
SkylaneAI-v2/
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

### 🎯 Core Features
- **Real-time Hazard Detection**: Detect birds, drones, balloons, and kites in video streams
- **Video Upload & Processing**: Analyze pre-recorded videos for hazard assessment
- **Live Camera Feed**: Real-time analysis of camera feeds
- **Bounding Box Overlays**: Visual indicators for detected hazards
- **Time-to-Contact (TTC)**: Calculate collision risk and warning levels
- **Graded Warnings**: Color-coded threat levels (Green, Yellow, Orange, Red)

### 📊 Additional Features
- **User Authentication**: Secure login and user management via Supabase
- **Video History**: Store and review past analyses
- **Dashboard Analytics**: Visualize detection statistics and patterns
- **Multi-camera Support**: Monitor multiple feeds simultaneously
- **Export Reports**: Generate detailed hazard reports

## Prerequisites

- **Node.js** >= 20.x
- **pnpm** >= 9.x
- **Python** >= 3.11
- **Supabase Account** (for backend services)
- **GPU** (recommended for YOLOv11 inference)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SkylaneAI-v2.git
cd SkylaneAI-v2
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
```bash
pnpm --filter web build
vercel --prod
```

### Backend
Backend deployment options will be configured in future phases.

### Supabase
Production database and authentication are managed through Supabase dashboard.

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
- GitHub Issues: https://github.com/yourusername/SkylaneAI-v2/issues
- Documentation: https://docs.skylaneai.com
- Email: support@skylaneai.com

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

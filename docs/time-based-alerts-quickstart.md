# Time-Based Alert System - Quick Start Guide

**Last Updated**: 2025-11-02

---

## What's New? 🎉

The system now generates **1 alert per second** automatically instead of requiring manual clicks on each detection!

### Before vs After

| Feature | Old System | New System |
|---------|-----------|------------|
| Alert Generation | Click each detection | Automatic per second |
| 5-second video | 50 potential alerts | 5 automatic alerts |
| User clicks needed | 50 | 0 |
| Cost (5s video) | $0 - $30 | $0.003 |
| UI Display | Individual cards | Timeline view |

---

## How It Works

### Simple Explanation

1. **Video uploads** → You upload a 10-second video
2. **Processing starts** → YOLO detects objects at 10 FPS
3. **Every second**:
   - System collects all detections (e.g., 10 bird detections in second 3)
   - Picks the BEST one (highest threat + confidence + size)
   - Generates natural language alert using LLM
   - Sends to frontend automatically
4. **Timeline displays** → All 10 alerts shown in scrollable timeline
5. **Watch video** → Current alert highlights as video plays

### Example

**Second 0 (frames 0-9)**:
- Detections: bird@92%, bird@85%, drone@40%
- **Best**: bird@92% (high threat, high confidence)
- **Alert Generated**: "🦅 Large Bird Detected - Center Screen"

**Second 1 (frames 10-19)**:
- Detections: drone@78%, drone@75%
- **Best**: drone@78%
- **Alert Generated**: "🚁 Drone Approaching - Immediate Action Required"

---

## Quick Start

### 1. Start the System

**Backend**:
```bash
cd apps/api
source venv/bin/activate
uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd apps/web
pnpm dev
```

### 2. Upload & Process Video

1. Go to: `http://localhost:3000/video`
2. Click **"Upload Video"** or drag & drop
3. Select a video file (recommended: 5-30 seconds)
4. Click **"Upload"** button
5. Wait for upload to complete
6. Click **"Start Processing"**

### 3. Watch Alerts Appear

As the video processes, you'll see:
- **Progress bar** showing completion percentage
- **Console logs**: `Time-based alert received: 3 high`
- **Alert Timeline** appearing below video player

### 4. Interact with Timeline

**Timeline Card**:
```
┌────────────────────────────────────────────┐
│ 📍 00:03 [HIGH] Score: 87                  │
│ 🦅 Large Bird Detected - Center Screen    │
│ Execute evasive maneuver                   │
│ [Jump to Time] [View Details]             │
└────────────────────────────────────────────┘
```

**Actions**:
- **Jump to Time**: Seeks video to that moment
- **View Details**: Opens modal with full alert (all 4 agents)
- **Auto-scroll**: Timeline follows video playback

---

## Understanding the Timeline

### Color Coding

| Priority | Color | Badge | When Used |
|----------|-------|-------|-----------|
| **Critical** | Red | `🔴 CRITICAL` | Immediate danger (score ≥ 80) |
| **High** | Orange | `🟠 HIGH` | Serious threat (score ≥ 60) |
| **Medium** | Yellow | `🟡 MEDIUM` | Moderate concern (score ≥ 40) |
| **Low** | Blue | `🔵 LOW` | Minor detection (score < 40) |

### Priority Score

The priority score (0-100) is calculated by:

```
Score = (Threat Level × 0.5) +
        (Confidence × 0.3) +
        (Size × 0.2)
```

**Example**:
- Large bird, high threat, 92% confidence
- Threat: 75 (high) × 0.5 = 37.5
- Confidence: 92 × 0.3 = 27.6
- Size: 100 (large) × 0.2 = 20.0
- **Total Score**: 85.1 → **HIGH priority**

---

## Testing the System

### Test Video Recommendations

**Good Test Videos**:
- Birds flying across sky (5-10 seconds)
- Drone footage with other drones visible
- Videos with multiple hazard types
- Clear, well-lit outdoor scenes

**Avoid**:
- Very dark or foggy videos
- Shaky/unstable footage
- Videos with no detectable objects
- Extremely long videos (>5 minutes on first test)

### Expected Results

**For a 10-second video with continuous bird activity**:
- ✅ 10 alerts generated (one per second)
- ✅ Each second picks highest priority detection
- ✅ Timeline shows all 10 alerts sorted by time
- ✅ Current alert highlights during playback
- ✅ Total cost: ~$0.006 (10 × $0.0006)

### Verification Checklist

1. **Backend Logs** (watch during processing):
   ```
   INFO: Generating alert for second 0: bird (confidence: 0.92)
   INFO: Alert generated for second 0: Priority=high (87.5)
   INFO: Sent time-based alert for second 0: high
   ```

2. **Frontend Console**:
   ```
   Time-based alert received: 0 high
   Time-based alert received: 1 medium
   Time-based alert received: 2 critical
   ```

3. **UI Elements**:
   - ✅ AlertTimeline component visible
   - ✅ Alert cards show correct timestamps
   - ✅ Color-coded priority badges
   - ✅ "View Details" button works
   - ✅ "Jump to Time" seeks correctly

---

## Troubleshooting

### Problem: No alerts appearing

**Symptoms**:
- Video processes successfully
- Detections appear in detection panel
- But AlertTimeline is empty

**Solution**:
1. Check browser console for errors
2. Verify `OPENAI_API_KEY` is set in backend `.env`
3. Check backend logs: `tail -f apps/api/logs/app.log | grep alert`
4. Ensure LLM agents are working: `python apps/api/test_complete_workflow.py`

### Problem: Alerts delayed or slow

**Symptoms**:
- Alerts appear 3-5 seconds after timestamp
- Processing seems slower than expected

**Solution**:
- **Expected**: 1-2 seconds per alert (LLM call time)
- This is normal! Alerts for second 0 arrive ~1.5 seconds later
- If longer: Check internet connection (OpenAI API)
- If much longer: Check OpenAI API rate limits

### Problem: Too many/duplicate alerts

**Symptoms**:
- Multiple alerts for same second
- More than expected number of alerts

**Solution**:
1. Check `processor.enable_time_based_alerts` is `True` (not set multiple times)
2. Verify only one `VideoFileProcessor` instance exists
3. Check for WebSocket reconnections in logs

### Problem: Frontend errors

**Symptoms**:
- `Module not found: @/components/ui/scroll-area`

**Solution**:
```bash
cd apps/web
npx shadcn@latest add scroll-area
```

**Symptoms**:
- Type errors with `WSTimeBasedAlertMessage`

**Solution**:
```bash
cd packages/types
pnpm build
cd ../../apps/web
pnpm dev
```

---

## API Configuration

### Backend Settings

**File**: `apps/api/.env`

```bash
# Required for LLM agents
OPENAI_API_KEY=sk-...

# Model (default: gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# Timeout for LLM calls (default: 5 seconds)
ALERT_GENERATION_TIMEOUT=5

# Enable/disable time-based alerts
# (Can also be set per-processor instance)
ENABLE_TIME_BASED_ALERTS=true
```

### Frontend Settings

**File**: `apps/web/.env.local`

```bash
# Backend URLs
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

---

## Advanced Usage

### Disable Time-Based Alerts

If you want to go back to the old per-detection system:

**Backend** (`video_routes.py`):
```python
processor = VideoFileProcessor(file_path, process_fps=10)
processor.enable_time_based_alerts = False  # Disable
```

### Customize Selection Algorithm

**File**: `apps/api/app/services/video_file_processor.py`

```python
def _select_best_detection(self):
    # Change weights (must sum to 1.0):
    priority = (
        threat_score * 0.6 +      # Increase threat importance
        confidence_score * 0.2 +  # Decrease confidence importance
        size_score * 0.2          # Keep size same
    )
```

### Filter Timeline by Priority

**Frontend** (custom implementation):
```typescript
const criticalAlerts = alerts.filter(a => a.priorityLevel === 'critical');

<AlertTimeline
  alerts={criticalAlerts}  // Show only critical
  currentTimestamp={time}
/>
```

---

## Performance Tips

### For Long Videos

**10+ minute videos**:
- Cost: ~$0.36 per 10 minutes (600 seconds × $0.0006)
- Time: ~2 minutes to generate all alerts (1-2s per second)
- Memory: ~1.2 MB in browser (600 alerts)

**Recommendations**:
1. Process in chunks if needed
2. Monitor OpenAI API usage dashboard
3. Consider caching similar alerts (future feature)

### For High-Frequency Detections

**50+ detections per second**:
- Selection algorithm handles this efficiently
- Processing time: <5ms per second for selection
- No impact on LLM cost (still 1 call per second)

---

## Next Steps

### Explore Features

1. **View Details Modal**
   - Click "View Details" on any alert
   - See full LLM-generated message
   - Review action recommendations
   - Check priority score breakdown

2. **Video Navigation**
   - Click "Jump to Time" to seek
   - Watch alert highlight follow playback
   - Use timeline as video chapter navigation

3. **Alert Statistics**
   ```typescript
   const stats = getAlertStatistics();
   console.log('Total alerts:', stats.totalAlerts);
   console.log('Critical count:', stats.priorityCounts.critical);
   console.log('Average score:', stats.averagePriorityScore);
   ```

### Provide Feedback

Test with your actual flight videos and report:
- Alert accuracy (are priorities correct?)
- Selection quality (best detection chosen?)
- UI/UX improvements needed
- Performance issues
- Cost concerns

---

## Summary

✅ **System is working if**:
- Alerts appear automatically (no clicks)
- One alert per second of video
- Timeline is scrollable and organized
- Current alert highlights during playback
- "View Details" shows full LLM content

🎯 **Expected behavior**:
- 5-second video = 5 alerts in ~10 seconds
- 30-second video = 30 alerts in ~60 seconds
- Cost scales linearly: $0.0006 per second

🚀 **You're ready to use the system!**

For detailed technical documentation, see: `docs/time-based-alert-implementation.md`

---

**Questions?** Check the troubleshooting section or review backend logs.

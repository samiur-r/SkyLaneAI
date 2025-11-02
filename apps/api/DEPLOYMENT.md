# Deploying SkyLaneAI API to Render

## Prerequisites

1. GitHub account with your repository pushed
2. Render account (free tier works fine)
3. OpenAI API key (for alert generation features)

## Deployment Steps

### Option 1: Deploy via Render Blueprint (Recommended)

1. **Push your code to GitHub** (if not already)
   ```bash
   git add .
   git commit -m "Add Render deployment config"
   git push origin main
   ```

2. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New +" → "Blueprint"

3. **Connect Repository**
   - Connect your GitHub account
   - Select your repository
   - Render will automatically detect `render.yaml`

4. **Configure Environment Variables**
   Render will prompt you to set these:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `CORS_ORIGINS`: Add your frontend URL (e.g., `["https://your-app.vercel.app"]`)

5. **Deploy**
   - Click "Apply"
   - Render will build and deploy your service
   - Wait ~5-10 minutes for first deployment

### Option 2: Manual Deployment

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New +" → "Web Service"

2. **Connect Repository**
   - Connect GitHub and select your repository
   - Select the branch: `main`

3. **Configure Service**
   - **Name**: `skylaneai-api`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `apps/api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Plan**
   - Select "Free" tier to start

5. **Environment Variables**
   Add these in the "Environment" section:

   **Required:**
   - `PYTHON_VERSION`: `3.11.0`
   - `OPENAI_API_KEY`: Your OpenAI API key

   **Optional (with sensible defaults):**
   - `CORS_ORIGINS`: `["https://your-app.vercel.app","http://localhost:3000"]`
   - `MODEL_NAME`: `yolo11n.pt` (default: yolo11n.pt)
   - `CONFIDENCE_THRESHOLD`: `0.25` (default: 0.25)
   - `VIDEO_MAX_SIZE_MB`: `100` (default: 100)

6. **Create Web Service**
   - Click "Create Web Service"
   - Wait for deployment (~5-10 minutes)

## Post-Deployment

### 1. Get Your API URL
After deployment, Render will provide a URL like:
```
https://skylaneai-api.onrender.com
```

### 2. Test Your API
Visit the docs endpoint:
```
https://skylaneai-api.onrender.com/docs
```

### 3. Update Frontend Environment Variables
In your Next.js app (Vercel), set:
```
NEXT_PUBLIC_API_URL=https://skylaneai-api.onrender.com
```

### 4. Update CORS Settings
In Render dashboard, update the `CORS_ORIGINS` environment variable:
```json
["https://your-app.vercel.app","http://localhost:3000"]
```

## Important Notes

### Free Tier Limitations
- ⚠️ **Spins down after 15 minutes of inactivity**
- First request after spin-down takes ~30-60 seconds
- 750 hours/month free compute time
- No custom domains (use provided .onrender.com URL)

### Model Files
- YOLO model (`yolo11n.pt`) will be downloaded on first request
- Model files are cached in the `models/` directory
- Ephemeral storage: Files persist during runtime but reset on redeploy

### Persistent Storage (If Needed Later)
For production, you may want to:
1. Store videos in external storage (S3, Cloudinary, Supabase Storage)
2. Use Redis for caching
3. Upgrade to paid plan for persistent disk

## Monitoring

### Logs
View logs in Render Dashboard:
- Dashboard → Your Service → Logs tab
- Look for startup message: `🚀 SkyLaneAI API v2.0.0 starting...`

### Health Checks
Render automatically monitors your `/` endpoint. If it returns 200 OK, service is healthy.

### Metrics
Free tier includes:
- CPU and memory usage graphs
- Request count
- Response times

## Troubleshooting

### Build Fails
- Check `requirements.txt` is valid
- Ensure Python version is 3.11
- Check build logs for specific errors

### Service Crashes
- Check if `PORT` environment variable is used correctly
- Verify all required env vars are set
- Check logs for Python errors

### CORS Errors
- Ensure frontend URL is in `CORS_ORIGINS`
- Format must be valid JSON array: `["https://app.com"]`
- Include protocol (https://)

### Model Download Issues
- First request will be slow (~30s) as model downloads
- Subsequent requests are fast (model cached)
- If persistent issues, try `yolo11n.pt` (smallest model)

## Upgrade Path

When ready for production:

1. **Paid Plan** ($7/month)
   - No spin-down
   - More CPU/RAM
   - Persistent disk

2. **Custom Domain**
   - Add your domain in Render dashboard
   - Update DNS records
   - Free SSL included

3. **Auto-Deploy**
   - Already enabled in `render.yaml`
   - Every push to `main` auto-deploys

## Next Steps

1. Deploy frontend to Vercel
2. Set up monitoring (Sentry, LogRocket)
3. Add database (Supabase)
4. Configure CI/CD for tests

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- SkyLaneAI Issues: https://github.com/yourusername/skylaneai/issues

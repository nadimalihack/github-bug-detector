# Render Deployment Fix - Python Version Issue

## Problem
Render was using Python 3.13.4 which caused pandas 2.2.0 to fail during compilation.

## Solution Applied

### 1. Python Version Configuration
Created root-level Python version files:
- `.python-version` → 3.11.2
- `runtime.txt` → python-3.11.2

### 2. Dependencies Update
- Created root-level `requirements.txt` 
- Downgraded pandas from 2.2.0 to 2.1.4 (compatible with Python 3.11.2)
- Updated `backend/requirements.txt` as well

### 3. Render Configuration
Created `render.yaml` with proper Python version specification.

## Deploy to Render

### Option 1: Using render.yaml (Recommended)
1. Commit and push these changes:
```bash
git add .python-version runtime.txt requirements.txt render.yaml backend/requirements.txt
git commit -m "Fix: Set Python 3.11.2 for Render deployment"
git push origin main
```

2. In Render Dashboard:
   - Go to your service
   - It will auto-detect `render.yaml` and redeploy

### Option 2: Manual Configuration
If render.yaml doesn't work, manually configure in Render Dashboard:

1. **Build Command:**
```bash
pip install -r requirements.txt
```

2. **Start Command:**
```bash
cd backend && uvicorn src.api:app --host 0.0.0.0 --port $PORT
```

3. **Environment Variables:**
Add these in Render Dashboard:
- `PYTHON_VERSION` = `3.11.2`
- `GITHUB_CLIENT_ID` = your_client_id
- `GITHUB_CLIENT_SECRET` = your_client_secret
- `GEMINI_API_KEY` = your_gemini_key
- `MONGODB_URI` = your_mongodb_uri
- `JWT_SECRET_KEY` = your_jwt_secret
- `FRONTEND_URL` = your_vercel_url

## Verify Deployment

After deployment, check the build logs for:
```
==> Using Python version 3.11.2 (default)
```

The pandas installation should now succeed without C++ compilation errors.

## Next Steps

1. Push changes to GitHub
2. Wait for Render to rebuild (automatic)
3. Check deployment logs
4. Test your API endpoints

## Troubleshooting

If still failing:
- Check Render logs for Python version
- Verify `runtime.txt` is in root directory
- Ensure `requirements.txt` is in root directory
- Try manual trigger: "Manual Deploy" → "Clear build cache & deploy"

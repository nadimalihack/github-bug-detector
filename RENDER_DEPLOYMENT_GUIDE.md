# 🚀 Render Deployment Guide

Complete guide to deploy your Bug Detection System on Render.com

## 📋 Prerequisites

- GitHub repository: https://github.com/gryffindowr/github-bug-detection
- Render account (free): https://render.com
- MongoDB Atlas account (free): https://www.mongodb.com/cloud/atlas
- GitHub OAuth App configured
- Gemini API keys

---

## 🎯 Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Render.com (Free Tier)          │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐  ┌─────────────────┐ │
│  │   Backend    │  │    Frontend     │ │
│  │  (Web Service)│  │  (Static Site)  │ │
│  │  Python/FastAPI│  │   React/Vite   │ │
│  └──────────────┘  └─────────────────┘ │
│         │                    │          │
└─────────┼────────────────────┼──────────┘
          │                    │
          ▼                    ▼
   ┌─────────────┐      ┌──────────┐
   │  MongoDB    │      │  GitHub  │
   │   Atlas     │      │   OAuth  │
   └─────────────┘      └──────────┘
```

---

## 📝 Step-by-Step Deployment

### Part 1: Prepare Configuration Files

#### 1.1 Create `render.yaml` (Blueprint)

Create this file in your repository root:

```yaml
services:
  # Backend Service
  - type: web
    name: bug-detection-backend
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && uvicorn src.api:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.2
      - key: GITHUB_CLIENT_ID
        sync: false
      - key: GITHUB_CLIENT_SECRET
        sync: false
      - key: OAUTH_REDIRECT_URI
        sync: false
      - key: GEMINI_API_KEY
        sync: false
      - key: GEMINI_API_KEY_2
        sync: false
      - key: GEMINI_API_KEY_3
        sync: false
      - key: MONGODB_URI
        sync: false
      - key: MONGODB_DB_NAME
        value: githubbug
      - key: JWT_SECRET_KEY
        sync: false
      - key: JWT_ALGORITHM
        value: HS256
      - key: JWT_EXPIRATION_HOURS
        value: 24
    healthCheckPath: /

  # Frontend Service
  - type: web
    name: bug-detection-frontend
    env: static
    region: oregon
    plan: free
    branch: main
    buildCommand: "cd frontend && npm install && npm run build"
    staticPublishPath: frontend/dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
```

#### 1.2 Update Backend for Production

Create `backend/render_build.sh`:

```bash
#!/usr/bin/env bash
# Render build script

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Creating necessary directories..."
mkdir -p models data src/data/users

echo "Build complete!"
```

Make it executable:
```bash
chmod +x backend/render_build.sh
```

#### 1.3 Update Frontend Environment

Create `frontend/.env.production`:

```env
VITE_API_URL=https://bug-detection-backend.onrender.com
```

Update `frontend/vite.config.js`:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        port: 3000
    },
    build: {
        outDir: 'dist',
        sourcemap: false,
        rollupOptions: {
            output: {
                manualChunks: {
                    vendor: ['react', 'react-dom', 'react-router-dom'],
                    charts: ['recharts'],
                    icons: ['react-icons']
                }
            }
        }
    }
})
```

---

### Part 2: Set Up MongoDB Atlas

#### 2.1 Create MongoDB Cluster

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up or log in
3. Click "Build a Database"
4. Choose "FREE" (M0 Sandbox)
5. Select a cloud provider and region (AWS - us-east-1 recommended)
6. Name your cluster: `bug-detection-cluster`
7. Click "Create"

#### 2.2 Configure Database Access

1. Go to "Database Access" in left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Username: `bugdetection`
5. Generate a secure password (save it!)
6. Database User Privileges: "Read and write to any database"
7. Click "Add User"

#### 2.3 Configure Network Access

1. Go to "Network Access" in left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (0.0.0.0/0)
4. Click "Confirm"

#### 2.4 Get Connection String

1. Go to "Database" in left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string:
   ```
   mongodb+srv://bugdetection:<password>@bug-detection-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password

---

### Part 3: Update GitHub OAuth App

#### 3.1 Update OAuth Callback URL

1. Go to https://github.com/settings/developers
2. Click on your OAuth App
3. Update "Authorization callback URL" to:
   ```
   https://bug-detection-frontend.onrender.com/auth/callback
   ```
4. Click "Update application"

---

### Part 4: Deploy Backend on Render

#### 4.1 Create Backend Service

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `bug-detection-backend`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.api:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

#### 4.2 Add Environment Variables

Click "Advanced" → "Add Environment Variable" and add:

```
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
OAUTH_REDIRECT_URI=https://bug-detection-frontend.onrender.com/auth/callback
GEMINI_API_KEY=your_gemini_api_key_1
GEMINI_API_KEY_2=your_gemini_api_key_2
GEMINI_API_KEY_3=your_gemini_api_key_3
MONGODB_URI=mongodb+srv://bugdetection:password@cluster.mongodb.net/
MONGODB_DB_NAME=githubbug
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
GITHUB_TOKEN=your_github_personal_access_token
```

#### 4.3 Deploy Backend

1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Note your backend URL: `https://bug-detection-backend.onrender.com`

---

### Part 5: Deploy Frontend on Render

#### 5.1 Update Frontend API URLs

Update all API calls in frontend to use environment variable:

Create `frontend/src/config.js`:

```javascript
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

Update API calls in components to use:
```javascript
import { API_URL } from '../config';

// Instead of: http://localhost:8000/endpoint
// Use: `${API_URL}/endpoint`
```

#### 5.2 Create Frontend Service

1. Go to https://dashboard.render.com
2. Click "New +" → "Static Site"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `bug-detection-frontend`
   - **Branch:** `main`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`

#### 5.3 Add Environment Variables

```
VITE_API_URL=https://bug-detection-backend.onrender.com
```

#### 5.4 Configure Redirects

Render will automatically handle SPA routing with the `routes` configuration in `render.yaml`.

#### 5.5 Deploy Frontend

1. Click "Create Static Site"
2. Wait for deployment (3-5 minutes)
3. Your app will be live at: `https://bug-detection-frontend.onrender.com`

---

### Part 6: Update CORS Settings

Update `backend/src/api.py` to allow your Render frontend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://bug-detection-frontend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push this change to trigger redeployment.

---

## 🔧 Post-Deployment Configuration

### Update All API Endpoints

Search and replace in frontend files:

```bash
# Find: http://localhost:8000
# Replace with: ${API_URL}
```

Files to update:
- `frontend/src/components/LoginPage.jsx`
- `frontend/src/components/Dashboard.jsx`
- `frontend/src/components/RepositoryList.jsx`
- `frontend/src/components/AnalyticsDashboard.jsx`
- `frontend/src/components/UserProfile.jsx`

Example:
```javascript
// Before
const response = await fetch('http://localhost:8000/auth/github');

// After
import { API_URL } from '../config';
const response = await fetch(`${API_URL}/auth/github`);
```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Backend is running: `https://bug-detection-backend.onrender.com/`
- [ ] Frontend is accessible: `https://bug-detection-frontend.onrender.com`
- [ ] GitHub OAuth login works
- [ ] Dashboard loads after login
- [ ] Repository analysis works
- [ ] MongoDB connection is successful
- [ ] Gemini AI analysis works
- [ ] All API endpoints respond correctly

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** Backend won't start
```bash
# Check logs in Render dashboard
# Common issues:
# 1. Missing environment variables
# 2. Wrong Python version
# 3. Missing dependencies
```

**Solution:**
- Verify all environment variables are set
- Check build logs for errors
- Ensure `requirements.txt` is complete

### Frontend Issues

**Problem:** API calls fail (CORS errors)
```bash
# Check browser console for CORS errors
```

**Solution:**
- Update CORS settings in backend
- Verify API_URL environment variable
- Check network tab for actual URLs being called

### MongoDB Issues

**Problem:** Database connection fails
```bash
# Error: MongoServerError: Authentication failed
```

**Solution:**
- Verify MongoDB URI is correct
- Check username and password
- Ensure IP whitelist includes 0.0.0.0/0
- Test connection string locally first

### OAuth Issues

**Problem:** OAuth redirect fails
```bash
# Error: redirect_uri_mismatch
```

**Solution:**
- Update GitHub OAuth App callback URL
- Verify OAUTH_REDIRECT_URI environment variable
- Must be exact match: `https://bug-detection-frontend.onrender.com/auth/callback`

---

## 💰 Cost Breakdown

### Free Tier Limits

**Render Free Plan:**
- ✅ 750 hours/month (enough for 1 service 24/7)
- ✅ Automatic SSL certificates
- ✅ Automatic deploys from Git
- ⚠️ Services spin down after 15 minutes of inactivity
- ⚠️ Cold start time: 30-60 seconds

**MongoDB Atlas Free Tier:**
- ✅ 512 MB storage
- ✅ Shared RAM
- ✅ No credit card required

**Total Cost:** $0/month (Free!)

### Upgrade Options

If you need better performance:
- **Render Starter:** $7/month (no spin down)
- **MongoDB M10:** $0.08/hour (~$57/month)

---

## 🚀 Custom Domain (Optional)

### Add Custom Domain to Render

1. Go to your service settings
2. Click "Custom Domains"
3. Add your domain: `bugdetection.yourdomain.com`
4. Add CNAME record to your DNS:
   ```
   CNAME bugdetection -> bug-detection-frontend.onrender.com
   ```
5. Render will automatically provision SSL certificate

---

## 📊 Monitoring

### Render Dashboard

- View logs in real-time
- Monitor CPU and memory usage
- Check deployment history
- View metrics and analytics

### Set Up Alerts

1. Go to service settings
2. Enable "Deploy Notifications"
3. Add webhook or email notifications

---

## 🔄 Continuous Deployment

Render automatically deploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Render will automatically:
# 1. Detect the push
# 2. Build the application
# 3. Deploy the new version
# 4. Zero-downtime deployment
```

---

## 📝 Environment Variables Reference

### Backend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GITHUB_CLIENT_ID` | GitHub OAuth App Client ID | `Ov23lirmZlck0lWIldmx` |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth App Secret | `7f7f52d75e8446dde...` |
| `OAUTH_REDIRECT_URI` | OAuth callback URL | `https://your-app.onrender.com/auth/callback` |
| `GEMINI_API_KEY` | Primary Gemini API key | `AIzaSyDMMW6_oCif...` |
| `GEMINI_API_KEY_2` | Backup Gemini API key | `AIzaSyDioPvBsw3c...` |
| `GEMINI_API_KEY_3` | Backup Gemini API key | `AIzaSyDs5zC-WgTK...` |
| `MONGODB_URI` | MongoDB connection string | `mongodb+srv://user:pass@cluster...` |
| `MONGODB_DB_NAME` | Database name | `githubbug` |
| `JWT_SECRET_KEY` | JWT signing secret | `your-super-secret-key` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_EXPIRATION_HOURS` | Token expiration | `24` |
| `GITHUB_TOKEN` | GitHub Personal Access Token | `ghp_xxxxxxxxxxxx` |

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://backend.onrender.com` |

---

## 🎉 Success!

Your Bug Detection System is now live on Render!

**URLs:**
- Frontend: `https://bug-detection-frontend.onrender.com`
- Backend: `https://bug-detection-backend.onrender.com`
- API Docs: `https://bug-detection-backend.onrender.com/docs`

**Next Steps:**
1. Test all features thoroughly
2. Monitor logs for any errors
3. Set up custom domain (optional)
4. Share with users!

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)

---

## 🆘 Need Help?

If you encounter issues:
1. Check Render logs
2. Review this guide
3. Check MongoDB Atlas status
4. Verify all environment variables
5. Test locally first

Good luck with your deployment! 🚀

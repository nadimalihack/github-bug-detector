# 🚀 Vercel Deployment Guide

Your frontend is now configured to work with your Render backend!

## ✅ Configuration Complete

### Backend URL
- **Render Backend:** `https://github-bug-detection.onrender.com`

### Files Configured
1. ✅ `frontend/src/config.js` - API URL configuration
2. ✅ `frontend/vercel.json` - Vercel deployment settings
3. ✅ `frontend/.env.production` - Production environment variables
4. ✅ All components updated to use `API_URL` from config

## 🚀 Deploy to Vercel

### Option 1: Vercel Dashboard (Recommended)

1. **Go to Vercel:** https://vercel.com/dashboard
2. **Click "New Project"**
3. **Import your GitHub repository:** `gryffindowr/github-bug-detection`
4. **Configure:**
   - Framework Preset: **Vite**
   - Root Directory: **`frontend`**
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

5. **Add Environment Variable:**
   ```
   Name: VITE_API_URL
   Value: https://github-bug-detection.onrender.com
   ```

6. **Click "Deploy"**

### Option 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Navigate to frontend
cd frontend

# Deploy
vercel --prod
```

## 🔧 Post-Deployment Steps

### 1. Update GitHub OAuth App

After deployment, you'll get a Vercel URL like: `https://your-app.vercel.app`

Update your GitHub OAuth App:
1. Go to: https://github.com/settings/developers
2. Click on your OAuth App
3. Update **Authorization callback URL:**
   ```
   https://your-app.vercel.app/auth/callback
   ```

### 2. Update Backend CORS

Update your backend on Render to allow your Vercel domain:

In `backend/src/api.py`, add your Vercel URL to CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-app.vercel.app",  # Add this
        "https://github-bug-detection.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then commit and push to trigger Render redeployment.

### 3. Update Backend OAuth Redirect

In your Render dashboard, update the environment variable:
```
OAUTH_REDIRECT_URI=https://your-app.vercel.app/auth/callback
```

## ✅ Verification Checklist

After deployment:
- [ ] Frontend loads at Vercel URL
- [ ] Login button works
- [ ] GitHub OAuth redirects correctly
- [ ] Dashboard loads after login
- [ ] Repository analysis works
- [ ] All API calls succeed (check browser console)

## 🎯 Your URLs

- **Frontend (Vercel):** `https://your-app.vercel.app`
- **Backend (Render):** `https://github-bug-detection.onrender.com`
- **API Docs:** `https://github-bug-detection.onrender.com/docs`

## 🔄 Continuous Deployment

Vercel automatically deploys when you push to GitHub:
```bash
git add .
git commit -m "Update frontend"
git push
```

Vercel will automatically build and deploy your changes!

## 💰 Cost

- **Vercel:** FREE (Hobby plan)
- **Render:** FREE (with limitations)
- **Total:** $0/month 🎉

## 🐛 Troubleshooting

### Build Fails
```bash
# Test locally first
cd frontend
npm install
npm run build
```

### API Calls Fail
- Check browser console for errors
- Verify `VITE_API_URL` environment variable in Vercel
- Check backend CORS settings
- Ensure backend is running on Render

### OAuth Fails
- Verify GitHub OAuth callback URL matches Vercel URL exactly
- Check backend `OAUTH_REDIRECT_URI` environment variable
- Test OAuth flow in incognito mode

## 📚 Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)
- [GitHub OAuth Apps](https://docs.github.com/en/developers/apps/building-oauth-apps)

---

**Ready to deploy!** 🚀

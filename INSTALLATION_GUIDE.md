# 🚀 Installation Guide - Bug Predictor Pro

## ✨ New Features Installed

- 🤖 **Gemini AI Integration** - Deep code analysis
- 🔐 **GitHub OAuth** - Secure authentication
- 📊 **Professional Dashboard** - Modern UI
- 🎨 **Enhanced Design** - Beautiful components
- 📈 **Analytics** - Charts and trends
- 👥 **User Management** - Profile & settings

---

## 📦 Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**New packages installed:**
- `google-generativeai` - Gemini AI integration
- `authlib` - OAuth authentication
- `python-jose[cryptography]` - JWT tokens
- `httpx` - Async HTTP client

---

## 📦 Step 2: Install Frontend Dependencies

```bash
cd frontend
npm install
```

**New packages installed:**
- `react-router-dom` - Routing
- `recharts` - Charts and graphs
- `framer-motion` - Animations
- `react-hot-toast` - Notifications
- `react-icons` - Icon library
- `zustand` - State management

---

## 🔑 Step 3: API Keys Already Configured

Your `.env` file has been updated with:

```env
# Gemini AI
GEMINI_API_KEY=AIzaSyDlHnd5CN6H-1t5kvkgIRg9xjEgJTuZFvw

# GitHub OAuth
GITHUB_CLIENT_ID=Ov23lirmZlck0lWIldmx
GITHUB_CLIENT_SECRET=7f7f52d75e8446dde9429f217e03761ca6636f7d
OAUTH_REDIRECT_URI=http://localhost:3000/auth/callback
```

✅ **All set!** Your API keys are configured.

---

## 🚀 Step 4: Start the Application

### Terminal 1 - Backend:
```bash
cd backend/src
python api.py
```

Backend runs on: `http://localhost:8000`

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Frontend runs on: `http://localhost:3000`

---

## 🎯 Step 5: Test the Features

### 1. **Login with GitHub**
- Open `http://localhost:3000`
- Click "Continue with GitHub"
- Authorize the application
- You'll be redirected to the dashboard

### 2. **Explore Dashboard**
- View your GitHub repositories
- See your analysis statistics
- Check analytics and trends

### 3. **Analyze a Repository**
- Click on any repository card
- Click "Analyze" button
- Wait for enhanced analysis (ML + Gemini AI)
- View detailed results

### 4. **View Analytics**
- Click "Analytics" in sidebar
- See risk trends over time
- View repository comparisons
- Track your progress

### 5. **Check Profile**
- Click "Profile" in sidebar
- View your GitHub info
- See recent analyses
- Check your stats

---

## 🆕 New API Endpoints

### Authentication
- `GET /auth/github` - Get OAuth URL
- `POST /auth/callback` - Handle OAuth callback
- `GET /auth/verify` - Verify JWT token

### User Management
- `GET /user/{user_id}` - Get user profile
- `GET /user/{user_id}/stats` - Get user statistics
- `GET /user/{user_id}/repositories` - Get user repos

### Gemini AI Analysis
- `POST /analyze/gemini` - Analyze code with Gemini
- `POST /analyze/gemini/repository` - Analyze multiple files
- `POST /analyze-enhanced` - Combined ML + Gemini analysis

### Analytics
- `GET /analytics/overview` - Overall analytics
- `GET /analytics/trends` - Trend data for charts

---

## 🎨 New Frontend Components

### Core Components
- `LoginPage.jsx` - GitHub OAuth login
- `Dashboard.jsx` - Main dashboard layout
- `RepositoryList.jsx` - Repository cards
- `AnalyticsDashboard.jsx` - Charts and trends
- `UserProfile.jsx` - User profile page

### State Management
- `authStore.js` - Zustand store for authentication

### Styling
- All components have matching CSS files
- Gradient backgrounds
- Smooth animations
- Responsive design

---

## 🔧 Troubleshooting

### Backend Issues

**Import errors:**
```bash
pip install --upgrade -r requirements.txt
```

**Port already in use:**
```bash
# Change port in api.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Frontend Issues

**Module not found:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
npm run build
```

### OAuth Issues

**Callback URL mismatch:**
1. Go to GitHub OAuth settings
2. Update callback URL to: `http://localhost:3000/auth/callback`
3. Make sure it matches `.env` file

**Invalid credentials:**
- Double-check Client ID and Secret in `.env`
- Regenerate OAuth app if needed

### Gemini AI Issues

**API key invalid:**
- Verify key at: https://makersuite.google.com/app/apikey
- Update in `.env` file
- Restart backend server

**Rate limits:**
- Gemini has free tier limits
- Upgrade to paid plan if needed

---

## 📊 Feature Comparison

### Before (Classic View)
- ✅ Basic bug prediction
- ✅ GitHub URL analysis
- ✅ File upload
- ✅ JSON input

### After (Pro Dashboard)
- ✅ All classic features
- 🆕 GitHub OAuth login
- 🆕 Gemini AI analysis
- 🆕 Professional dashboard
- 🆕 Analytics & trends
- 🆕 User profiles
- 🆕 Repository management
- 🆕 Enhanced UI/UX

---

## 🎯 Usage Tips

1. **First Time Setup**
   - Login with GitHub first
   - This syncs your repositories
   - Enables personalized features

2. **Analyzing Repositories**
   - Use "Analyze" button for quick ML analysis
   - Enhanced analysis includes Gemini AI (slower but more detailed)
   - Results are saved to your profile

3. **Viewing Trends**
   - Analyze multiple repos to see trends
   - Charts update automatically
   - Export data for reports

4. **Classic View**
   - Click "Classic View" button anytime
   - Use for quick analyses without login
   - Switch back to dashboard when done

---

## 🔐 Security Notes

- JWT tokens expire after 24 hours
- GitHub tokens are stored securely
- Never commit `.env` file
- Use environment variables in production

---

## 🚀 Next Steps

1. **Customize**
   - Update colors in CSS files
   - Modify dashboard layout
   - Add more charts

2. **Deploy**
   - Use Vercel for frontend
   - Use Railway/Heroku for backend
   - Update OAuth callback URLs

3. **Enhance**
   - Add more AI models
   - Integrate webhooks
   - Add team features

---

## 📞 Support

If you encounter issues:
1. Check console logs (F12)
2. Verify API keys in `.env`
3. Ensure both servers are running
4. Check network requests

---

**🎉 Enjoy your new Bug Predictor Pro!**

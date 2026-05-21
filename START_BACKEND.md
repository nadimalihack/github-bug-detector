# How to Start the Backend Server

## ✨ Easiest Way - Single Command

### Option 1: From Project Root
```cmd
python run-backend.py
```

### Option 2: From Backend Folder
```cmd
python backend/run.py
```

### Option 3: Using Batch File
```cmd
start-backend.bat
```

## 📋 All Methods

### Method 1: Simple Python Script (Recommended)
```cmd
python run-backend.py
```
✅ Works from anywhere in the project
✅ Automatically sets up paths
✅ Shows helpful startup messages

### Method 2: From Backend Directory
```cmd
cd backend
python run.py
```

### Method 3: Using uvicorn Directly
```cmd
cd backend
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

### Method 4: Using Batch File
```cmd
start-backend.bat
```
Opens in a new window

### Method 5: Direct Python Execution
```cmd
cd backend
python -m src.api
```

## 🎯 What You'll See

When the server starts successfully:
```
============================================================
🚀 Starting Github Bug Detection Backend Server
============================================================

📍 Server will be available at:
   • http://localhost:8000
   • http://127.0.0.1:8000

📚 API Documentation:
   • http://localhost:8000/docs (Swagger UI)
   • http://localhost:8000/redoc (ReDoc)

💡 Test the API:
   • Open http://localhost:8000 in your browser

⚠️  Press CTRL+C to stop the server
============================================================

INFO:     Will watch for changes in these directories: ['E:\\ai contract simplifier\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
✓ Loaded 3 Gemini API key(s) for fallback
✓ Using Gemini API key #1 (stable)
✓ Enhanced features enabled (OAuth, Gemini AI, User Management)
INFO:     Application startup complete.
```

## ✅ Verify It's Running

### Test 1: Open in Browser
Go to: http://localhost:8000

You should see:
```json
{
  "message": "Github Bug Detection API",
  "status": "running",
  "features": {
    "self_learning": true,
    "feedback_api": true,
    "code_analysis": true,
    "enhanced_features": true,
    "gemini_ai": true,
    "oauth": true,
    "user_management": true
  },
  "note": "All features enabled"
}
```

### Test 2: Using curl
```cmd
curl http://localhost:8000
```

### Test 3: Check API Docs
Open: http://localhost:8000/docs

You'll see interactive API documentation (Swagger UI)

## 🛠️ Troubleshooting

### Error: "python not found"
**Solution:**
```cmd
python --version
```
If this fails, install Python or add it to PATH.

### Error: "No module named uvicorn"
**Solution:**
```cmd
cd backend
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"
**Solution:**
```cmd
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use a different port
python run-backend.py --port 8001
```

### Error: "No module named 'src'"
**Solution:**
Make sure you're running from the correct directory:
```cmd
# If using run-backend.py, run from project root
python run-backend.py

# If using backend/run.py, run from project root
python backend/run.py
```

### Error: "Enhanced features disabled"
**Solution:**
```cmd
cd backend
pip install google-generativeai authlib python-jose[cryptography] httpx
```

## 🔄 Restart the Server

### If Running in Terminal
1. Press `CTRL+C` to stop
2. Run the start command again

### If Running in Background
```cmd
# Find the process
tasklist | findstr python

# Kill it
taskkill /IM python.exe /F

# Start again
python run-backend.py
```

## 📊 Server Features

Once running, the backend provides:

- ✅ **Bug Prediction API** - ML-based bug detection
- ✅ **GitHub Integration** - Analyze repositories
- ✅ **Gemini AI Analysis** - Deep code analysis
- ✅ **OAuth Authentication** - GitHub login
- ✅ **User Management** - Profile and stats
- ✅ **Progress Tracking** - Real-time analysis updates
- ✅ **Self-Learning** - Improves over time

## 🌐 API Endpoints

### Main Endpoints:
- `GET /` - API status
- `POST /analyze-github-url` - Analyze repository
- `GET /auth/github` - GitHub OAuth
- `POST /auth/callback` - OAuth callback
- `GET /user/{user_id}/stats` - User statistics

### Documentation:
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc documentation

## 💾 Environment Variables

Make sure `backend/.env` has:
```env
GEMINI_API_KEY=your_key_here
GEMINI_API_KEY_2=backup_key_here
GEMINI_API_KEY_3=backup_key_here
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
JWT_SECRET_KEY=your_secret_key
```

## 🚀 Quick Start Commands

### Start Backend Only:
```cmd
python run-backend.py
```

### Start Both Backend and Frontend:
```cmd
start-all.bat
```

### Check if Backend is Running:
```cmd
curl http://localhost:8000
```

## 📝 Notes

- The server runs with **auto-reload** enabled
- Changes to Python files will automatically restart the server
- Logs appear in the terminal
- Press `CTRL+C` to stop the server
- Default port is **8000**
- Accessible from **localhost** and **127.0.0.1**

## 🎉 Success!

If you see:
```
INFO:     Application startup complete.
```

Your backend is ready! 🚀

Now you can:
1. Open http://localhost:8000 to test
2. Start the frontend with `start-frontend.bat`
3. Access the full app at http://localhost:3000

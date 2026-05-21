# ✅ HOW TO RUN THE APPLICATION

## ⚠️ IMPORTANT: DO NOT RUN `python api.py` DIRECTLY!

### ❌ WRONG WAY (Will cause import errors)
```bash
cd backend/src
python api.py          # ❌ This will NOT work!
```

**Error you'll get:**
```
ImportError: attempted relative import with no known parent package
```

### ✅ CORRECT WAY

## Option 1: Use Batch Files (Easiest)

**Terminal 1 - Backend:**
```bash
start-backend.bat
```

**Terminal 2 - Frontend:**
```bash
start-frontend.bat
```

## Option 2: Manual Commands

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn src.api:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Why This Way?

### The Problem
- Python relative imports (`.predictor`, `.utils`) only work when running as a module
- Running `python api.py` directly treats it as a script, not a module
- This breaks all the relative imports

### The Solution
- Use `python -m uvicorn src.api:app` to run it as a module
- This tells Python that `src` is a package
- Relative imports work correctly

## Current Status

✅ **Backend is ALREADY RUNNING!**

```
✓ ML model loaded successfully
✓ MongoDB connected: githubbug
✓ Using Gemini 2.5 Flash model (stable)
✓ Enhanced features enabled
✓ Server running on http://127.0.0.1:8000
```

## What to Do Now

1. **Don't stop the backend** - it's already running!
2. **Start the frontend:**
   ```bash
   start-frontend.bat
   ```
   Or manually:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open browser:** http://localhost:5173

4. **Test the application:**
   - Login with GitHub
   - Analyze a repository
   - See real Gemini AI analysis!

## Troubleshooting

### "Module not found" errors
- ✅ Make sure you're in `backend/` directory (not `backend/src/`)
- ✅ Use: `python -m uvicorn src.api:app --reload`
- ❌ Don't use: `python api.py` or `python src/api.py`

### Backend won't start
```bash
# Kill any existing Python processes
taskkill /F /IM python.exe

# Start fresh
cd backend
python -m uvicorn src.api:app --reload
```

### Check if backend is running
Open browser: http://localhost:8000/docs
- If you see API documentation, it's running!
- If not, start it with the correct command above

## Quick Reference

### Start Backend
```bash
cd backend
python -m uvicorn src.api:app --reload
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Test Gemini API
```bash
cd backend
python test_gemini_api.py
```

### Check Backend Status
```bash
# Open in browser
http://localhost:8000/docs
```

## Summary

✅ **Backend is running** - Don't restart it!
✅ **Just start the frontend** - Use `start-frontend.bat`
✅ **Open browser** - http://localhost:5173
✅ **Enjoy real Gemini AI analysis!**

---

**Remember:** Always use `python -m uvicorn src.api:app --reload` from the `backend/` directory!

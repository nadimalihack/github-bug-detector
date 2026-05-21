# 📝 Quick Reference Guide

## 🚀 Quick Commands

### Start Servers
```bash
# Backend
cd backend/src && python api.py

# Frontend
cd frontend && npm run dev
```

### URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🔑 GitHub Token

**Get Token:** https://github.com/settings/tokens  
**Scopes:** `repo`, `public_repo`  
**Add to:** `backend/.env` → `GITHUB_TOKEN=ghp_xxx`

---

## 📊 Risk Scores

| Score | Color | Meaning |
|-------|-------|---------|
| 70-100% | 🔴 Red | High risk - needs attention |
| 40-69% | 🟡 Yellow | Medium risk - monitor |
| 0-39% | 🟢 Green | Low risk - stable |

---

## 🐛 Issue Severity

| Level | Icon | Examples |
|-------|------|----------|
| Critical | 🔴 | SQL injection, hardcoded passwords, eval() |
| High | 🟠 | Empty catch, bare except, try without catch |
| Medium | 🟡 | Loose equality, var usage, deprecated APIs |
| Low | 🟢 | Console.log, TODO comments, magic numbers |

---

## 🔧 Common Fixes

### Port Already in Use
```powershell
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

### Rate Limit Error
- Get GitHub token
- Add to `.env` file
- Restart backend

### Network Error
- Check internet connection
- Flush DNS: `ipconfig /flushdns`
- Try different network

### Model Not Found
```bash
cd backend
python train_from_github.py
```

---

## 📁 File Structure

```
backend/src/
├── api.py              # Main server
├── github_analyzer.py  # GitHub API
├── code_analyzer.py    # Code quality
├── predictor.py        # Risk prediction
├── trainer.py          # ML training
└── utils.py            # Helpers

frontend/src/
├── components/
│   └── BugPredictor.jsx  # Main component
├── App.jsx
└── main.jsx
```

---

## 🎯 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| POST | `/analyze-github-url` | Analyze by URL |
| POST | `/analyze-github-file` | Upload file |
| POST | `/predict` | Direct prediction |
| GET | `/demo` | Demo data |

---

## 🧪 Test Commands

```bash
# Code analyzer
python backend/test_code_analyzer.py

# GitHub integration
python backend/test_github.py

# Full pipeline
python backend/test_full_analysis.py

# With code issues
python backend/test_with_code.py
```

---

## 📦 Dependencies

### Backend
```bash
pip install fastapi uvicorn PyGithub scikit-learn pandas numpy
```

### Frontend
```bash
npm install react react-dom vite
```

---

## 🎨 UI Features

### Input Methods
1. **🔗 GitHub URL** - Paste repo URL
2. **📝 JSON Data** - Manual input
3. **📁 Upload File** - Upload JSON

### Buttons
- **Analyze Repository** - Start analysis
- **Load Demo** - See example
- **Load Sample** - Sample JSON
- **View X Code Issues** - Expand details

---

## 🔍 Code Patterns Detected

### Security
- SQL Injection
- Hardcoded passwords
- eval() usage

### Error Handling
- Empty catch blocks
- Try without catch
- Bare except (Python)

### Code Quality
- Console statements
- TODO comments
- Magic numbers
- Deprecated APIs

---

## 📈 Training Model

```bash
# Quick train (5 repos)
cd backend
python train_from_github.py

# Custom repos
# Edit train_from_github.py
# Add your repos to TRAINING_REPOS
python train_from_github.py
```

---

## 🌐 Environment Variables

```env
# Required for analysis
GITHUB_TOKEN=ghp_your_token_here

# Optional
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 💡 Tips

✅ Use GitHub token for unlimited analysis  
✅ Click "Load Demo" to see all features  
✅ Train model on your repos for better accuracy  
✅ Start with small repos (< 100 commits)  
✅ Check backend console for detailed logs  
✅ Use browser DevTools to debug frontend  

---

## 🆘 Emergency Commands

### Kill All Python Processes
```powershell
taskkill /F /IM python.exe
```

### Reset Everything
```bash
# Kill processes
taskkill /F /PID <backend_pid>
taskkill /F /PID <frontend_pid>

# Restart
cd backend/src && python api.py
cd frontend && npm run dev
```

### Fresh Install
```bash
# Backend
cd backend
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📞 Quick Links

- **GitHub Tokens:** https://github.com/settings/tokens
- **FastAPI Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:3000
- **Full Docs:** [DOCUMENTATION.md](DOCUMENTATION.md)
- **Setup Guide:** [QUICKSTART.md](QUICKSTART.md)
- **Token Setup:** [SETUP_GITHUB_TOKEN.md](SETUP_GITHUB_TOKEN.md)

---

**Need Help?** Check [DOCUMENTATION.md](DOCUMENTATION.md) for detailed guides!

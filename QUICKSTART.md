# 🚀 Quick Start Guide

## Step 1: Install Dependencies

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Step 2: Start the Servers

### Terminal 1 - Backend
```bash
cd backend/src
python api.py
```
✓ API running at http://localhost:8000

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```
✓ UI running at http://localhost:3000

## Step 3: Analyze Your First Repository

### Option A: GitHub URL (Recommended)

1. Open http://localhost:3000
2. Click **"🔗 GitHub URL"** tab
3. Enter a repository:
   - `facebook/react`
   - `microsoft/vscode`
   - `torvalds/linux`
   - Or any GitHub URL
4. Click **"Analyze Repository"**
5. Wait 10-30 seconds for analysis
6. View results with risk scores!

### Option B: Try Sample Data

1. Click **"📝 JSON Data"** tab
2. Click **"Load Sample"** button
3. Click **"Predict Bug Risk"**
4. See instant results!

### Option C: Upload File

1. Click **"📁 Upload File"** tab
2. Upload `backend/data/sample_repos.json`
3. View analysis results

## Step 4: Understand Results

### Risk Scores
- 🔴 **70-100%**: High risk - Frequent bugs, needs attention
- 🟡 **40-69%**: Medium risk - Monitor closely
- 🟢 **0-39%**: Low risk - Stable code

### What It Analyzes
- Commit messages for bug keywords
- Code change frequency
- Diff complexity
- Historical bug patterns

## Step 5: Train Custom Model (Optional)

```bash
cd backend/src
python trainer.py
```

This trains an ML model on sample data. Add your own repos to `backend/data/sample_repos.json` for better accuracy.

## 🔑 GitHub Token (For Better Results)

Without token: 60 API calls/hour
With token: 5000 API calls/hour

### Get Token:
1. Visit https://github.com/settings/tokens
2. Generate new token (classic)
3. Select `repo` scope
4. Copy token
5. Paste in UI under "Optional: GitHub Token"

## 🎯 Example Repositories to Try

- `facebook/react` - Popular frontend library
- `django/django` - Python web framework
- `nodejs/node` - JavaScript runtime
- `kubernetes/kubernetes` - Container orchestration
- Your own repositories!

## ⚡ Tips

- Start with small repos (< 1000 commits) for faster analysis
- Use GitHub token for private repos
- Check `backend/data/sample_repos.json` for data format
- Train custom model with your team's repos for best results

## 🐛 Troubleshooting

**Backend won't start?**
- Check Python version (3.8+)
- Run `pip install -r requirements.txt` again

**Frontend won't start?**
- Check Node version (16+)
- Run `npm install` again
- Try `npm run dev -- --host`

**GitHub analysis fails?**
- Check internet connection
- Verify repo URL format
- Try with GitHub token
- Check rate limit: http://localhost:8000/github/rate-limit

**No results showing?**
- Open browser console (F12)
- Check if backend is running
- Verify CORS is enabled

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- See [GITHUB_SETUP.md](backend/GITHUB_SETUP.md) for token setup
- Check [backend/README.md](backend/README.md) for API details
- Explore [frontend/README.md](frontend/README.md) for UI info

Happy bug hunting! 🐛🔍

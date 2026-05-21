# 🐛 Bug Prediction System - Complete Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Architecture](#architecture)
4. [Features](#features)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage Guide](#usage-guide)
8. [API Reference](#api-reference)
9. [Code Analysis](#code-analysis)
10. [ML Model Training](#ml-model-training)
11. [Troubleshooting](#troubleshooting)
12. [Development](#development)

---

## 🎯 Overview

An AI-powered system that analyzes GitHub repositories to predict which files are most likely to contain bugs. It combines:

- **Static Code Analysis**: Detects security vulnerabilities and code smells
- **Historical Analysis**: Examines commit patterns and bug frequency
- **Machine Learning**: Trains models on repository data for predictions
- **Beautiful UI**: React-based interface with detailed visualizations

### Key Capabilities

✅ Analyze any GitHub repository (public/private)  
✅ Detect 15+ types of code issues (SQL injection, hardcoded passwords, etc.)  
✅ Assign risk scores (0-100%) to each file  
✅ Provide fix suggestions and impact explanations  
✅ Train custom ML models on your data  
✅ Support for JavaScript, Python, Java, C++, Go, Ruby, PHP  

---

## ⚡ Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Internet connection

### 5-Minute Setup

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Install frontend dependencies
cd ../frontend
npm install

# 3. Start backend (Terminal 1)
cd ../backend/src
python api.py

# 4. Start frontend (Terminal 2)
cd ../../frontend
npm run dev

# 5. Open browser
# http://localhost:3000
```

### First Analysis

1. Click "Load Demo" to see features
2. Or get GitHub token: https://github.com/settings/tokens
3. Paste token in UI
4. Enter repository URL
5. Click "Analyze Repository"

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  - User Interface                                        │
│  - 3 Input Methods (URL/JSON/File)                      │
│  - Results Visualization                                 │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP/REST
┌────────────────▼────────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  API Layer (api.py)                              │  │
│  │  - /analyze-github-url                           │  │
│  │  - /analyze-github-file                          │  │
│  │  - /predict                                      │  │
│  │  - /demo                                         │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────▼───────────────────────────────────┐  │
│  │  GitHub Analyzer (github_analyzer.py)           │  │
│  │  - Fetch commits, diffs, issues                 │  │
│  │  - Code quality analysis                        │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────▼───────────────────────────────────┐  │
│  │  Code Analyzer (code_analyzer.py)               │  │
│  │  - Pattern matching (regex)                     │  │
│  │  - Security vulnerability detection             │  │
│  │  - Code smell identification                    │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────▼───────────────────────────────────┐  │
│  │  Bug Predictor (predictor.py)                   │  │
│  │  - Risk score calculation                       │  │
│  │  - ML model predictions                         │  │
│  │  - Result aggregation                           │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│              External Services                           │
│  - GitHub API (PyGithub)                                │
│  - ML Models (scikit-learn)                             │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- FastAPI - Web framework
- PyGithub - GitHub API client
- scikit-learn - Machine learning
- pandas/numpy - Data processing
- python-dotenv - Environment management

**Frontend:**
- React 18 - UI library
- Vite - Build tool
- Pure CSS - Styling (no frameworks)

---

## 🎨 Features

### 1. GitHub Repository Analysis

**Input Methods:**
- 🔗 **URL**: Paste GitHub URL or `owner/repo`
- 📝 **JSON**: Manual data input with sample loader
- 📁 **File**: Upload JSON file with commit data

**What Gets Analyzed:**
- Commit messages (bug keywords)
- Code diffs (changes made)
- File change frequency
- Code complexity metrics
- Issue tracking data
- Code quality issues

### 2. Code Quality Detection

**🔴 Critical Issues:**
- SQL Injection vulnerabilities
- Hardcoded passwords/secrets
- eval() usage (arbitrary code execution)

**🟠 High Severity:**
- Empty catch blocks
- Try blocks without catch
- Bare except clauses (Python)
- Mutable default arguments (Python)

**🟡 Medium Severity:**
- Loose equality (== vs ===)
- var usage (use let/const)
- Deprecated API usage
- Null checks without strict equality

**🟢 Low Severity:**
- Console.log statements
- TODO/FIXME comments
- Magic numbers

### 3. Risk Scoring

Each file receives:
- **Risk Score**: 0-100% (higher = more risky)
- **Reason**: Explanation of the score
- **Code Issues**: Count by severity
- **Detailed Issues**: Line-by-line analysis

**Risk Factors:**
- Bug-related commit frequency
- Code change complexity
- Historical bug patterns
- Code quality issues detected

### 4. Machine Learning

**Training:**
- Collects data from GitHub repos
- Extracts features (bug keywords, complexity, frequency)
- Trains RandomForest classifier
- Saves model for predictions

**Prediction:**
- Uses trained model when available
- Falls back to rule-based system
- Combines ML + code analysis

---

## 📦 Installation

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your GitHub token
# GITHUB_TOKEN=ghp_your_token_here

# Test installation
python test_code_analyzer.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Test build
npm run build
```

---

## ⚙️ Configuration

### Environment Variables

Create `backend/.env`:

```env
# GitHub OAuth (optional)
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback

# GitHub Personal Access Token (recommended)
GITHUB_TOKEN=ghp_your_token_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### GitHub Token Setup

1. Visit: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes:
   - ✅ `repo` (for private repos)
   - ✅ `public_repo` (for public repos)
4. Copy token (starts with `ghp_`)
5. Add to `.env` file

**Benefits:**
- 60 → 5,000 requests/hour
- Access private repositories
- No rate limit errors

---

## 📖 Usage Guide

### Analyzing a Repository

#### Method 1: GitHub URL (Recommended)

```bash
# 1. Start servers
cd backend/src && python api.py
cd frontend && npm run dev

# 2. Open http://localhost:3000
# 3. Click "🔗 GitHub URL" tab
# 4. Enter: facebook/react
# 5. (Optional) Add GitHub token
# 6. Click "Analyze Repository"
```

#### Method 2: JSON Data

```json
{
  "repository_name": "owner/repo",
  "commits": [
    {
      "hash": "abc123",
      "message": "Fixed bug in auth",
      "diff": "- old code\n+ new code",
      "files_changed": ["auth.js"]
    }
  ],
  "issues": [
    {"commit_hash": "abc123", "type": "bug"}
  ]
}
```

#### Method 3: File Upload

Upload a JSON file with the above format.

### Understanding Results

**Repository Overview:**
```
demo/vulnerable-app
🔤 JavaScript  ⭐ 42  🔱 15
Overall Risk: 73%
```

**File Analysis:**
```
database.js - 85% Risk
"High bug frequency (12/20 commits) | 2 critical code issues"

🔴 2 Critical  🟠 5 High

▼ View 7 Code Issues

  🔴 Critical                    Line 42
  Potential SQL injection vulnerability
  
  const query = "SELECT * FROM users WHERE id = '" + userId + "'";
  
  Impact: Attackers can execute arbitrary SQL, steal or delete data
  Fix: Use parameterized queries or prepared statements
```

---

## 🔌 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### GET /
Health check

**Response:**
```json
{
  "message": "Bug Prediction API",
  "status": "running"
}
```

#### POST /analyze-github-url
Analyze repository by URL

**Request:**
```json
{
  "repo_url": "owner/repo",
  "max_commits": 100,
  "access_token": "ghp_xxx"  // optional
}
```

**Response:**
```json
{
  "repository_name": "owner/repo",
  "overall_repository_risk": 0.73,
  "modules": [
    {
      "file": "auth.js",
      "risk_score": 0.85,
      "reason": "High bug frequency...",
      "critical_issues": 2,
      "high_issues": 5,
      "detailed_issues": [...]
    }
  ],
  "metadata": {
    "stars": 1234,
    "forks": 567,
    "language": "JavaScript"
  }
}
```

#### POST /analyze-github-file
Upload JSON file

**Request:** multipart/form-data with file

**Response:** Same as /analyze-github-url

#### POST /predict
Direct prediction from JSON

**Request:** Repository JSON data

**Response:** Prediction results

#### GET /demo
Get demo analysis (for testing)

**Response:** Sample analysis with code issues

---

## 🔍 Code Analysis

### Detection Patterns

The system uses regex patterns to detect issues:

```python
# SQL Injection
pattern = r'(SELECT|INSERT|UPDATE|DELETE).*\+.*["\']'

# Hardcoded Password
pattern = r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']'

# eval() Usage
pattern = r'\beval\s*\('

# Empty Catch
pattern = r'catch\s*\([^)]*\)\s*\{\s*\}'
```

### Supported Languages

- **JavaScript/TypeScript**: var usage, ==, console.log
- **Python**: bare except, mutable defaults
- **Java**: deprecated APIs
- **C/C++**: memory issues
- **Go**: error handling
- **Ruby**: deprecated syntax
- **PHP**: security issues

### Adding Custom Rules

Edit `backend/src/code_analyzer.py`:

```python
self.error_patterns['your_rule'] = {
    'pattern': r'your_regex_pattern',
    'severity': 'critical',  # critical/high/medium/low
    'message': 'Description of the issue',
    'fix': 'How to fix it',
    'impact': 'Why it matters'
}
```

---

## 🤖 ML Model Training

### Quick Training

```bash
cd backend
python train_from_github.py
```

This trains on 5 popular repositories.

### Custom Training

Edit `backend/train_from_github.py`:

```python
TRAINING_REPOS = [
    "your-org/repo1",
    "your-org/repo2",
    "your-org/repo3"
]
```

Then run:
```bash
python train_from_github.py
```

### Training Process

1. **Data Collection**: Fetches commits from GitHub
2. **Feature Extraction**: Analyzes bug keywords, complexity
3. **Model Training**: RandomForest classifier
4. **Evaluation**: Accuracy, precision, recall
5. **Model Saving**: Saves to `models/bug_predictor.pkl`

### Using Trained Model

Restart the API server:
```bash
cd backend/src
python api.py
```

You'll see: `✓ ML model loaded successfully`

---

## 🐛 Troubleshooting

### Network Error: "Failed to resolve api.github.com"

**Cause:** DNS/network connectivity issue

**Solutions:**
1. Check internet connection
2. Try different network/WiFi
3. Disable VPN if active
4. Flush DNS cache:
   ```powershell
   ipconfig /flushdns
   ```
5. Use Google DNS (8.8.8.8, 8.8.4.4)
6. Check firewall settings

### Rate Limit Exceeded

**Cause:** 60 requests/hour limit without token

**Solution:** Get GitHub token (see Configuration)

### Port Already in Use

**Cause:** Server already running

**Solution:**
```powershell
# Find process
netstat -ano | findstr :8000

# Kill it (replace PID)
taskkill /F /PID <PID>

# Or use helper script
cd backend
.\kill_and_restart.bat
```

### Model Not Found

**Cause:** No trained model

**Solution:**
```bash
cd backend
python train_from_github.py
```

Or use rule-based prediction (works without model)

### Frontend Not Showing Issues

**Cause:** Repository has no detectable issues

**Solution:** Click "Load Demo" to see feature

### CORS Errors

**Cause:** Backend not running or wrong port

**Solution:**
1. Verify backend is running: http://localhost:8000
2. Check frontend API URLs match backend port
3. Restart both servers

---

## 👨‍💻 Development

### Project Structure

```
├── backend/
│   ├── src/
│   │   ├── api.py              # FastAPI server
│   │   ├── github_analyzer.py  # GitHub integration
│   │   ├── code_analyzer.py    # Code quality analysis
│   │   ├── predictor.py        # Risk prediction
│   │   ├── trainer.py          # ML model training
│   │   └── utils.py            # Helper functions
│   ├── data/
│   │   └── sample_repos.json   # Training data
│   ├── models/                 # Trained models
│   ├── tests/                  # Test scripts
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── BugPredictor.jsx
│   │   │   └── BugPredictor.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
└── docs/                       # Documentation
```

### Running Tests

```bash
# Backend tests
cd backend
python test_code_analyzer.py
python test_github.py
python test_with_code.py
python test_full_analysis.py

# Frontend (no tests yet)
cd frontend
npm run build
```

### Adding Features

1. **New Code Pattern:**
   - Edit `backend/src/code_analyzer.py`
   - Add pattern to `error_patterns`
   - Test with `test_code_analyzer.py`

2. **New API Endpoint:**
   - Edit `backend/src/api.py`
   - Add route with `@app.get()` or `@app.post()`
   - Restart server

3. **New UI Feature:**
   - Edit `frontend/src/components/BugPredictor.jsx`
   - Add CSS to `BugPredictor.css`
   - Frontend auto-reloads

### Code Style

**Python:**
- PEP 8 style guide
- Type hints recommended
- Docstrings for functions

**JavaScript:**
- ES6+ syntax
- Functional components
- Descriptive variable names

---

## 📊 Performance

### Benchmarks

- **Small repo** (< 100 commits): 5-10 seconds
- **Medium repo** (100-1000 commits): 30-60 seconds
- **Large repo** (1000+ commits): 2-5 minutes

### Optimization Tips

1. Limit commits: `max_commits=50`
2. Use GitHub token (faster API)
3. Train model on relevant repos
4. Cache results (future feature)

---

## 🔒 Security

### Best Practices

✅ Never commit tokens to Git  
✅ Use `.env` files (in `.gitignore`)  
✅ Regenerate exposed tokens  
✅ Use minimal required scopes  
✅ Set token expiration dates  
✅ Review code before deployment  

### Data Privacy

- No data stored permanently
- GitHub tokens not logged
- Analysis done in real-time
- No external data sharing

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🤝 Contributing

Contributions welcome! Areas to improve:

- [ ] More language support
- [ ] Better ML models
- [ ] Performance optimization
- [ ] UI enhancements
- [ ] Test coverage
- [ ] Documentation

---

## 📞 Support

**Issues:** Check Troubleshooting section  
**Questions:** Read documentation  
**Bugs:** Create GitHub issue  

---

## 🎉 Credits

Built with:
- Python & FastAPI
- React & Vite
- PyGithub
- scikit-learn

---

**Happy Bug Hunting! 🐛🔍✨**

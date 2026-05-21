# 🚀 Push Code to GitHub Repository

## Repository
https://github.com/gryffindowr/github-bug-detection

## Steps to Push

### 1. Initialize Git (if not already done)
```bash
git init
```

### 2. Add Remote Repository
```bash
git remote add origin https://github.com/gryffindowr/github-bug-detection.git
```

Or if remote already exists:
```bash
git remote set-url origin https://github.com/gryffindowr/github-bug-detection.git
```

### 3. Check Git Status
```bash
git status
```

### 4. Add All Files (except those in .gitignore)
```bash
git add .
```

### 5. Commit Changes
```bash
git commit -m "Initial commit: Complete Bug Detection System with OAuth, Dashboard, and Responsive Design"
```

### 6. Push to GitHub
```bash
git branch -M main
git push -u origin main
```

If you encounter issues with existing content:
```bash
git push -u origin main --force
```

## What's Excluded (.gitignore)

✅ **Excluded from repository:**
- `.env` files (contains sensitive API keys and secrets)
- `node_modules/` (frontend dependencies)
- `__pycache__/` (Python cache)
- `venv/` or `env/` (Python virtual environment)
- `.vscode/` and `.idea/` (IDE settings)
- Log files
- Build outputs
- OS-specific files

✅ **Included in repository:**
- All source code
- Configuration files
- Documentation
- `.env.example` (template for environment variables)
- Requirements and dependencies lists

## Important Notes

### Sensitive Data Protection
The `.env` file contains:
- GitHub OAuth Client ID and Secret
- Gemini API Keys
- MongoDB connection string
- JWT Secret Key

**Never commit the `.env` file!** Instead, use `.env.example` as a template.

### After Cloning
When someone clones the repository, they need to:
1. Copy `.env.example` to `.env`
2. Fill in their own API keys and secrets
3. Install dependencies:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   npm install
   ```

## Verify Before Pushing

Check that `.env` is not staged:
```bash
git status
```

Should NOT see `backend/.env` in the list of files to be committed.

## Quick Push Commands

```bash
# One-liner to push everything
git add . && git commit -m "Update: Latest changes" && git push
```

## Troubleshooting

### If .env was accidentally committed:
```bash
# Remove from git but keep local file
git rm --cached backend/.env
git commit -m "Remove .env from repository"
git push
```

### If you need to force push:
```bash
git push -u origin main --force
```

⚠️ **Warning:** Force push will overwrite remote repository history!

## Success! 🎉

Once pushed, your repository will be available at:
https://github.com/gryffindowr/github-bug-detection

Others can clone it with:
```bash
git clone https://github.com/gryffindowr/github-bug-detection.git
```

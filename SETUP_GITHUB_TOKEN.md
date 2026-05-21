# GitHub Token Setup Guide

## Why You Need a Token

Without a token:
- ❌ 60 API requests/hour
- ❌ Rate limit errors
- ❌ Can't analyze repos

With a token:
- ✅ 5,000 API requests/hour
- ✅ Access private repos
- ✅ Analyze unlimited repos

## Get Your Token (2 minutes)

### Step 1: Go to GitHub Settings
Visit: https://github.com/settings/tokens

Or navigate:
1. Click your profile picture (top right)
2. Settings
3. Developer settings (bottom left)
4. Personal access tokens
5. Tokens (classic)

### Step 2: Generate Token
1. Click **"Generate new token (classic)"**
2. Note: `Bug Predictor`
3. Expiration: `90 days` (or your preference)
4. Select scopes:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **public_repo** (Access public repositories)
5. Click **"Generate token"**

### Step 3: Copy Token
- Copy the token (starts with `ghp_...`)
- **IMPORTANT**: Save it somewhere - you won't see it again!

## Use Your Token

### Option 1: In the UI (Temporary)
1. Open http://localhost:3000
2. Go to "🔗 GitHub URL" tab
3. Expand "Optional: GitHub Token"
4. Paste your token
5. Analyze any repository!

### Option 2: Environment Variable (Permanent)

Create `backend/.env` file:

```env
GITHUB_TOKEN=ghp_your_token_here
```

Restart the backend:
```bash
cd backend/src
python api.py
```

Now all requests use your token automatically!

## Train ML Model with Real Data

Once you have a token, train the model:

```bash
cd backend
python train_from_github.py
```

This will:
1. Fetch data from 5 popular repositories
2. Analyze commits and code issues
3. Train an ML model
4. Save it for future predictions

## Verify It Works

Test with your token:

```bash
# Set token temporarily
$env:GITHUB_TOKEN="ghp_your_token_here"

# Test analysis
cd backend
python test_github.py
```

## Security Tips

- ✅ Never commit tokens to Git
- ✅ Use `.env` files (already in `.gitignore`)
- ✅ Regenerate tokens if exposed
- ✅ Use minimal required scopes
- ✅ Set expiration dates

## Troubleshooting

**"Rate limit exceeded"**
- You need a token
- Or wait for rate limit reset (check: http://localhost:8000/github/rate-limit)

**"Token invalid"**
- Check token is correct (starts with `ghp_`)
- Verify token hasn't expired
- Ensure `repo` scope is selected

**"Repository not found"**
- Check repository URL is correct
- For private repos, ensure token has `repo` scope
- Verify repository exists

## Next Steps

1. ✅ Get your token
2. ✅ Add to `.env` file
3. ✅ Train ML model: `python train_from_github.py`
4. ✅ Restart backend
5. ✅ Analyze any repository!

Happy bug hunting! 🐛🔍

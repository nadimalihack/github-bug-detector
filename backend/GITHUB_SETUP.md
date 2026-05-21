# GitHub Integration Setup

## Quick Start (No Token Required)

The system works without a token for public repositories, but with limited API calls (60/hour).

## Using GitHub Personal Access Token (Recommended)

For private repos and higher rate limits (5000/hour):

### 1. Create GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Bug Predictor"
4. Select scopes:
   - ✅ `repo` (for private repositories)
   - ✅ `public_repo` (for public repositories)
5. Click "Generate token"
6. Copy the token (starts with `ghp_`)

### 2. Use Token in Frontend

Paste your token in the "Optional: GitHub Token" field when analyzing a repository.

### 3. Or Set Environment Variable (Backend)

Create `backend/.env` file:

```env
GITHUB_TOKEN=ghp_your_token_here
```

## OAuth Integration (Future Enhancement)

For full OAuth flow with GitHub login:

1. Create GitHub OAuth App: https://github.com/settings/developers
2. Set Authorization callback URL: `http://localhost:3000/auth/callback`
3. Add credentials to `.env`:
   ```env
   GITHUB_CLIENT_ID=your_client_id
   GITHUB_CLIENT_SECRET=your_client_secret
   ```

## Rate Limits

- **Without token**: 60 requests/hour
- **With token**: 5,000 requests/hour
- **OAuth**: 5,000 requests/hour per user

## Supported Repository Formats

- `https://github.com/owner/repo`
- `github.com/owner/repo`
- `owner/repo`

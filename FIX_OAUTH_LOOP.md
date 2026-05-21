# 🔧 Fix OAuth Login Loop Issue

## Problem
After clicking "Continue with GitHub" and authorizing, the app returns to the login page instead of opening the dashboard.

## Root Causes

### 1. **GitHub OAuth App Redirect URI Mismatch**
The redirect URI configured in your GitHub OAuth App must EXACTLY match the one in your `.env` file.

### 2. **Port Mismatch**
Frontend and backend must be on the correct ports.

### 3. **OAuth Callback Not Processing**
The callback might be failing silently.

## Solution Steps

### Step 1: Verify GitHub OAuth App Settings

1. Go to: https://github.com/settings/developers
2. Click on your OAuth App (or create one if needed)
3. Check these settings:

```
Application name: Bug Detection System (or your choice)
Homepage URL: http://localhost:3000
Authorization callback URL: http://localhost:3000/auth/callback
```

**CRITICAL:** The callback URL must be EXACTLY `http://localhost:3000/auth/callback`

### Step 2: Verify Backend .env File

Check `backend/.env`:

```env
GITHUB_CLIENT_ID=Ov23liSAdkTrGKhKJYcT
GITHUB_CLIENT_SECRET=7f7f52d75e8446dde9429f217e03761ca6636f7d
OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback
```

**Make sure:**
- Client ID matches GitHub OAuth App
- Client Secret matches GitHub OAuth App
- Redirect URI is EXACTLY `http://localhost:3000/auth/callback`

### Step 3: Verify Frontend Port

Check `frontend/vite.config.js`:

```javascript
export default defineConfig({
    plugins: [react()],
    server: {
        port: 3000  // Must be 3000
    }
})
```

### Step 4: Clear Browser Data

**IMPORTANT:** Clear all cached data:

1. Open DevTools (F12)
2. Go to Application tab
3. Clear Storage:
   - Local Storage → Clear all
   - Session Storage → Clear all
   - Cookies → Clear all
4. Close DevTools
5. Close browser completely
6. Reopen browser

### Step 5: Restart Servers

```bash
# Terminal 1 - Stop and restart backend
cd backend
# Press Ctrl+C to stop
python run.py

# Terminal 2 - Stop and restart frontend
cd frontend
# Press Ctrl+C to stop
npm run dev
```

### Step 6: Test with Debug Tool

1. Open the debug tool: `test-oauth-debug.html` in your browser
2. Click "Test Backend" - should show ✅
3. Click "Test /auth/github" - should show authorization URL
4. Check that redirect_uri in the URL is correct

### Step 7: Test OAuth Flow

1. Go to http://localhost:3000
2. Click "Login"
3. Click "Continue with GitHub"
4. **Watch the browser console (F12 → Console)**
5. Authorize on GitHub
6. **Check console logs after redirect**

Expected console logs:
```
🔍 Initial check - OAuth code: true Authenticated: false Classic: false
🔑 OAuth code detected in URL, showing login page to process
🔄 Processing OAuth callback with code: ...
✅ Auth callback successful, user: [username]
📝 Calling login with user: [username]
✅ Auth store updated, user authenticated
✅ Authentication detected, navigating to dashboard
```

## Common Issues & Fixes

### Issue 1: "Enhanced features not available (503)"

**Solution:**
```bash
cd backend
pip install google-generativeai authlib python-jose[cryptography] httpx
python run.py
```

### Issue 2: "Bad credentials" or "Authentication failed"

**Causes:**
- Wrong Client ID or Secret
- OAuth App not configured correctly on GitHub

**Solution:**
1. Go to GitHub OAuth Apps settings
2. Regenerate Client Secret
3. Update `backend/.env` with new secret
4. Restart backend

### Issue 3: "Redirect URI mismatch"

**Solution:**
1. Check GitHub OAuth App callback URL
2. Must be: `http://localhost:3000/auth/callback`
3. Update if different
4. Restart backend

### Issue 4: Stays on login page, no errors

**Solution:**
1. Open browser console (F12)
2. Look for errors in Console tab
3. Check Network tab for failed requests
4. Clear browser cache and try again

### Issue 5: "CORS error"

**Solution:**
Backend should have CORS enabled. Check `backend/src/api.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Debug Checklist

Use this checklist to verify everything:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] GitHub OAuth App callback URL is `http://localhost:3000/auth/callback`
- [ ] `.env` file has correct Client ID and Secret
- [ ] `.env` file has correct Redirect URI
- [ ] Browser cache cleared
- [ ] LocalStorage cleared
- [ ] SessionStorage cleared
- [ ] Enhanced features installed (`pip install ...`)
- [ ] No errors in browser console
- [ ] No errors in backend terminal

## Testing Script

Run this in browser console after clicking "Continue with GitHub":

```javascript
// Check if OAuth code is present
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');
console.log('OAuth code:', code ? 'Present ✅' : 'Missing ❌');

// Check localStorage
const authStorage = localStorage.getItem('auth-storage');
console.log('Auth storage:', authStorage ? 'Present ✅' : 'Missing ❌');

// Check if authenticated
if (authStorage) {
    const parsed = JSON.parse(authStorage);
    console.log('Is authenticated:', parsed.state?.isAuthenticated ? 'Yes ✅' : 'No ❌');
    console.log('User:', parsed.state?.user?.login || 'Not set');
}

// Check sessionStorage
const processing = sessionStorage.getItem('oauth_processing');
console.log('OAuth processing flag:', processing || 'Not set');
```

## Manual Test

If automatic flow doesn't work, test manually:

1. Open `test-oauth-debug.html` in browser
2. Click "Test Backend" → Should be ✅
3. Click "Test /auth/github" → Should show authorization URL
4. Copy the authorization URL
5. Open it in new tab
6. Authorize on GitHub
7. After redirect, click "Test Callback" in debug tool
8. Should show ✅ and save to localStorage
9. Reload your app → Should show dashboard

## Still Not Working?

If you've tried everything above and it still doesn't work:

1. **Check backend logs** - Look for errors in the terminal running `python run.py`
2. **Check browser console** - Look for JavaScript errors
3. **Check Network tab** - Look for failed HTTP requests
4. **Try incognito mode** - Rules out browser extension issues
5. **Check firewall** - Make sure ports 3000 and 8000 are not blocked

## Success Indicators

You'll know it's working when:

✅ Spinner shows when clicking "Continue with GitHub"
✅ Redirects to GitHub authorization page
✅ After authorization, redirects back to your app
✅ Console shows authentication flow logs
✅ Dashboard opens automatically
✅ User avatar and name appear in header
✅ URL is clean (no `?code=...`)

## Quick Fix Command

Run this to reset everything:

```bash
# Stop all servers (Ctrl+C in both terminals)

# Backend
cd backend
pip install google-generativeai authlib python-jose[cryptography] httpx
python run.py

# Frontend (new terminal)
cd frontend
npm run dev

# Browser
# 1. Press F12
# 2. Application → Clear Storage → Clear site data
# 3. Close browser
# 4. Reopen and go to http://localhost:3000
```

## Need More Help?

Open `test-oauth-debug.html` and run all tests. Share the output to diagnose the issue.

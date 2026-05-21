# Troubleshoot OAuth Dashboard Issue

## Problem
After GitHub OAuth login, not able to visit the dashboard.

## Diagnostic Steps

### Step 1: Run Diagnostic Script

Open browser console (F12) and paste the contents of `diagnose-oauth.js` or run:

```javascript
// Quick diagnostic
const auth = JSON.parse(localStorage.getItem('auth-storage') || '{}');
console.log('isAuthenticated:', auth.state?.isAuthenticated);
console.log('user:', auth.state?.user?.login);
console.log('Should show:', auth.state?.isAuthenticated ? 'DASHBOARD' : 'CLASSIC VIEW');
```

### Step 2: Check Console Logs

After OAuth callback, you should see:
```
🔑 OAuth code detected, processing...
🔄 Processing OAuth callback with code: abc123...
✅ Auth callback successful, user: your-username
✅ Auth store updated
🔄 Reloading to show dashboard...
```

Then after reload:
```
🔍 App render - isAuthenticated: true showDashboard: false
✅ Rendering Dashboard (user is authenticated)
```

### Step 3: Check What You're Seeing

**If you see:**
- 🏠 Classic View → Auth failed or not saved
- 🔐 Login Page → Stuck in login state
- 📊 Dashboard → Success! ✅

## Common Issues & Solutions

### Issue 1: Auth State Not Saved

**Symptoms:**
- OAuth completes
- Page reloads
- Still shows classic view
- Console shows: `isAuthenticated: false`

**Solution:**
```javascript
// Check if backend auth worked
fetch('http://localhost:8000/auth/callback?code=test', {method: 'POST'})
  .then(r => r.json())
  .then(d => console.log('Backend response:', d))
  .catch(e => console.log('Backend error:', e))
```

**If backend fails:**
1. Check backend is running: `http://localhost:8000`
2. Check `.env` has GitHub OAuth credentials
3. Check GitHub OAuth app callback URL

### Issue 2: Auth Saved But Dashboard Not Showing

**Symptoms:**
- Console shows: `isAuthenticated: true`
- But still seeing classic view or login page
- Console shows: `🏠 Rendering Classic View` (wrong!)

**Solution:**
```javascript
// Force re-render
const auth = JSON.parse(localStorage.getItem('auth-storage'));
console.log('Auth state:', auth);

// If isAuthenticated is true but wrong view showing:
location.reload(true); // Hard reload
```

**If still not working:**
```javascript
// Clear and re-login
localStorage.clear();
sessionStorage.clear();
location.reload();
// Then login again
```

### Issue 3: OAuth Processing Flag Stuck

**Symptoms:**
- Can't login again
- Console shows: `oauth_processing: true`
- OAuth callback doesn't run

**Solution:**
```javascript
sessionStorage.clear();
location.reload();
```

### Issue 4: Page Doesn't Reload After Login

**Symptoms:**
- See toast: "Successfully logged in! Redirecting..."
- But page doesn't reload
- Stuck on login page with `?code=...` in URL

**Solution:**
```javascript
// Manually trigger reload
window.location.href = '/';
```

**Or check console for errors:**
- JavaScript errors blocking reload
- Network errors
- Browser blocking reload

### Issue 5: Zustand Store Not Persisting

**Symptoms:**
- Login works
- Auth saved to localStorage
- But `isAuthenticated` is false after reload

**Check:**
```javascript
// Check if Zustand is reading from localStorage
const stored = localStorage.getItem('auth-storage');
const parsed = JSON.parse(stored);
console.log('Stored:', parsed);

// Check if useAuthStore is working
import useAuthStore from './store/authStore';
const { isAuthenticated } = useAuthStore.getState();
console.log('Store:', isAuthenticated);
```

**Solution:**
```javascript
// Clear and start fresh
localStorage.removeItem('auth-storage');
sessionStorage.clear();
location.reload();
```

## Step-by-Step Debug Process

### 1. Clear Everything
```javascript
localStorage.clear();
sessionStorage.clear();
console.log('✅ Cleared');
```

### 2. Start Fresh
```
location.reload();
```

### 3. Login
- Click "Login for Dashboard"
- Click "Continue with GitHub"
- Authorize

### 4. Watch Console
You should see in order:
```
🔑 OAuth code detected, processing...
🔄 Processing OAuth callback with code: ...
✅ Auth callback successful, user: ...
✅ Auth store updated
🔄 Reloading to show dashboard...
[PAGE RELOADS]
🔍 App render - isAuthenticated: true showDashboard: false
✅ Rendering Dashboard (user is authenticated)
```

### 5. If It Fails

**Check where it fails:**

**Fails at "OAuth code detected"?**
- OAuth callback URL might be wrong
- Check GitHub OAuth app settings

**Fails at "Auth callback successful"?**
- Backend error
- Check backend logs
- Check `.env` file

**Fails at "Reloading"?**
- JavaScript error
- Check browser console for errors

**Reloads but shows wrong view?**
- Zustand store issue
- Check localStorage has correct data
- Try hard refresh: Ctrl+Shift+R

## Manual Test

### Test 1: Check Auth Store
```javascript
const auth = JSON.parse(localStorage.getItem('auth-storage'));
console.log('Full auth object:', auth);
console.log('isAuthenticated:', auth?.state?.isAuthenticated);
console.log('user:', auth?.state?.user);
console.log('token:', auth?.state?.token ? 'present' : 'missing');
console.log('githubToken:', auth?.state?.githubToken ? 'present' : 'missing');
```

### Test 2: Manually Set Auth (for testing)
```javascript
// WARNING: This is just for testing!
const testAuth = {
    state: {
        isAuthenticated: true,
        user: { login: 'testuser', id: 123 },
        token: 'test-token',
        githubToken: 'test-gh-token'
    },
    version: 0
};
localStorage.setItem('auth-storage', JSON.stringify(testAuth));
location.reload();
// Should show dashboard
```

### Test 3: Check Backend
```bash
# In terminal
curl http://localhost:8000/
# Should return JSON with features

curl http://localhost:8000/auth/github
# Should return authorization_url
```

## Quick Fixes

### Fix 1: Nuclear Option
```javascript
// Clear everything and start completely fresh
localStorage.clear();
sessionStorage.clear();
document.cookie.split(";").forEach(c => {
    document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
});
location.href = '/';
```

### Fix 2: Force Dashboard (if auth is correct)
```javascript
// If isAuthenticated is true but dashboard not showing
const auth = JSON.parse(localStorage.getItem('auth-storage'));
if (auth?.state?.isAuthenticated) {
    console.log('Auth is correct, forcing reload...');
    location.reload(true);
}
```

### Fix 3: Re-save Auth
```javascript
// If auth data looks corrupted
const auth = JSON.parse(localStorage.getItem('auth-storage'));
if (auth) {
    // Re-save with correct structure
    localStorage.setItem('auth-storage', JSON.stringify(auth));
    location.reload();
}
```

## Files to Check

1. **frontend/src/App.jsx** - Routing logic
2. **frontend/src/components/LoginPage.jsx** - OAuth callback
3. **frontend/src/store/authStore.js** - Zustand store
4. **backend/src/api.py** - Auth callback endpoint
5. **backend/.env** - GitHub OAuth credentials

## Expected localStorage Structure

```json
{
  "state": {
    "user": {
      "login": "username",
      "id": 12345,
      "avatar_url": "https://...",
      "name": "Full Name"
    },
    "token": "eyJ...",
    "githubToken": "gho_...",
    "isAuthenticated": true
  },
  "version": 0
}
```

## Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] GitHub OAuth app configured
- [ ] Callback URL is `http://localhost:3000`
- [ ] `.env` has correct credentials
- [ ] Browser storage cleared before test
- [ ] Console shows all expected logs
- [ ] localStorage has auth data
- [ ] `isAuthenticated` is `true`
- [ ] Dashboard appears after login

## Still Not Working?

1. **Check browser console** for any errors
2. **Check backend terminal** for errors
3. **Check network tab** (F12 → Network) for failed requests
4. **Try different browser** to rule out browser-specific issues
5. **Check GitHub OAuth app** settings match exactly

## Get Help

Run this and share the output:
```javascript
console.log('=== OAUTH DEBUG INFO ===');
console.log('URL:', window.location.href);
console.log('Auth:', localStorage.getItem('auth-storage'));
console.log('Session:', sessionStorage.getItem('oauth_processing'));
console.log('Backend:', await fetch('http://localhost:8000/').then(r => r.ok));
console.log('=======================');
```

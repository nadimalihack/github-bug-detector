# 🔧 Fix GitHub Token Issues

## Error: "Bad credentials" or "Not Found"

You're seeing this error because:
1. Your GitHub token is invalid, expired, or missing
2. The repository doesn't exist or is private

## Solution

### Option 1: Log Out and Log In Again (Recommended)

1. **Log Out**:
   - Click your avatar in the top right
   - Click "Logout"

2. **Log In Again**:
   - Click "Login with GitHub"
   - Authorize the app
   - Your new token will be saved automatically

### Option 2: Check Repository Access

The repository `gryffindowr/Three60onward` might be:
- **Private**: You need to be logged in with the correct account
- **Deleted**: The repository no longer exists
- **Renamed**: The repository name has changed

**To verify:**
1. Go to: https://github.com/gryffindowr/Three60onward
2. Check if you can see it
3. If not, try a different repository

### Option 3: Use a Public Repository for Testing

Try analyzing a public repository first:
- `facebook/react`
- `microsoft/vscode`
- `torvalds/linux`

This will help confirm if the issue is with authentication or the specific repository.

## Common Issues

### Issue 1: Token Expired
**Symptom**: "Bad credentials" error
**Solution**: Log out and log in again

### Issue 2: Repository Not Found
**Symptom**: "Not Found" (404) error
**Solution**: 
- Check repository name spelling
- Verify repository exists
- Make sure you have access (if private)

### Issue 3: Rate Limit Exceeded
**Symptom**: "API rate limit exceeded"
**Solution**: 
- Wait 15-60 minutes
- Log in with GitHub OAuth (higher rate limits)

## How to Check Your Token

### In Browser Console (F12):
```javascript
const auth = JSON.parse(localStorage.getItem('auth-storage'));
console.log('GitHub Token:', auth?.state?.githubToken ? 'Present' : 'Missing');
console.log('User:', auth?.state?.user?.username);
```

If token is missing or user is null, log out and log in again.

## Testing Your Fix

1. **Log out and log in again**
2. **Try analyzing a public repository**:
   - Go to "Repositories" tab
   - Find a public repository
   - Click "Analyze"

3. **If it works**, try your private repository again

## Still Having Issues?

### Check Backend Logs
Look for these messages in backend console:
```
✗ GitHub API error: Bad credentials
✗ GitHub API error: Not Found
```

### Check Frontend Logs
Open browser console (F12) and look for:
```
Analysis error: ...
```

### Verify OAuth Setup
Make sure your GitHub OAuth app is configured:
1. Go to: https://github.com/settings/developers
2. Check your OAuth app settings
3. Verify callback URL: `http://localhost:3000/auth/callback`

## Quick Fix Commands

### Clear All Data and Start Fresh
```javascript
// In browser console (F12)
localStorage.clear();
location.reload();
```

Then log in again.

## Repository-Specific Issues

### Private Repository
If `Three60onward` is private:
1. Make sure you're logged in with the correct GitHub account
2. Verify you have access to the repository
3. Check repository settings → Collaborators

### Repository Doesn't Exist
If the repository was deleted or renamed:
1. Check the repository URL
2. Try a different repository
3. Contact the repository owner

## Success Indicators

You'll know it's fixed when:
✅ No "Bad credentials" error
✅ No "Not Found" error
✅ Analysis completes successfully
✅ Results appear in modal

## Need More Help?

1. Check if repository exists: https://github.com/gryffindowr/Three60onward
2. Try a public repository first
3. Log out and log in again
4. Check backend console for detailed errors

---

**Quick Fix**: Log out → Log in → Try again! 🚀

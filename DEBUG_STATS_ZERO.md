## Debugging: Stats Showing Zero

### Quick Diagnosis

Run this command to check your current stats:
```bash
cd backend
python check_user_stats.py
```

This will show:
- MongoDB connection status
- All users in local storage
- Their analysis counts and repositories
- Current stats values

### Common Causes & Solutions

#### 1. No Analyses Have Been Performed Yet
**Symptom**: Stats show 0 across the board
**Solution**: Analyze at least one repository
- Go to "Repositories" tab
- Click "Analyze" on any repository
- Wait for analysis to complete
- Stats should update within 5-10 seconds

#### 2. User ID Not Being Sent
**Symptom**: Analysis completes but stats don't update
**Check**: Open browser console (F12) and look for:
```
Analyzing repository: ... for user: undefined
```

**Solution**: 
1. Check if you're logged in (avatar should show in header)
2. Check localStorage: `localStorage.getItem('user')`
3. If user is null, log out and log back in

#### 3. MongoDB Not Connected
**Symptom**: Backend logs show "MongoDB not connected"
**Check**: Look for this in backend console:
```
✗ MongoDB connection failed: ...
```

**Solution**:
1. Check `backend/.env` file has valid MongoDB URI:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
   MONGODB_DB_NAME=githubbug
   ```
2. If you don't have MongoDB, that's OK! The app will use local files
3. Restart the backend after fixing .env

#### 4. Analysis Failing Silently
**Symptom**: "Analyze" button completes but no success message
**Check**: Browser console for errors

**Solution**:
1. Check if repository is empty (no commits)
2. Check if GitHub token is valid
3. Try analyzing a different repository

#### 5. Data Saved But Not Retrieved
**Symptom**: Backend logs show "Analysis saved" but stats still 0
**Check**: Run `python backend/check_user_stats.py`

**Solution**:
1. Check if user file exists: `backend/data/users/{user_id}.json`
2. Open the file and verify `analysis_count` > 0
3. If file exists but stats are 0, there's a retrieval issue

### Step-by-Step Debugging

#### Step 1: Check Backend Status
```bash
curl http://localhost:8000/
```

Should return:
```json
{
  "message": "Bug Prediction API",
  "status": "running",
  "features": {
    "enhanced_features": true,
    "user_management": true
  }
}
```

#### Step 2: Check Your User ID
In browser console (F12):
```javascript
const user = JSON.parse(localStorage.getItem('user'));
console.log('User ID:', user?.id);
console.log('Username:', user?.username);
```

#### Step 3: Manually Check Stats
```bash
curl http://localhost:8000/user/YOUR_USER_ID/stats
```

Replace YOUR_USER_ID with your actual user ID from Step 2.

#### Step 4: Analyze a Repository
1. Click "Analyze" on any repository
2. Watch browser console for:
   ```
   Analyzing repository: owner/repo for user: 123456
   Analysis complete: {...}
   ```
3. Watch backend console for:
   ```
   ✓ Analysis saved to MongoDB for user 123456
   OR
   ✓ Analysis saved locally for user 123456
   ```

#### Step 5: Verify Data Was Saved
```bash
cd backend
python check_user_stats.py
```

Look for your user ID and check if:
- Analysis Count > 0
- Repositories list has entries
- Stats show correct values

#### Step 6: Force Refresh Frontend
1. In browser, open DevTools (F12)
2. Go to Application tab
3. Clear localStorage
4. Refresh page
5. Log in again
6. Check if stats appear

### Manual Fix: Create Test Data

If you want to test with fake data:

```bash
cd backend
python test_stats_flow.py
```

This creates a test user with 2 analyses. Then check:
```bash
python check_user_stats.py
```

### Verify Real-Time Updates

1. Open Dashboard
2. Open browser console (F12)
3. You should see every 5 seconds:
   ```
   Fetching stats for user: 123456
   Stats received: {total_analyses: 2, ...}
   ```

If you don't see these messages:
- Auto-refresh might not be working
- Check for JavaScript errors in console

### Check Data Files

#### Local Storage Location
```
backend/data/users/{user_id}.json
```

Example content:
```json
{
  "id": "123456",
  "username": "yourname",
  "analysis_count": 2,
  "repositories": [
    {
      "name": "owner/repo1",
      "risk_score": 0.65,
      "analyzed_at": "2025-11-13T10:30:00"
    }
  ]
}
```

#### MongoDB Data
If using MongoDB, check with:
```bash
cd backend
python -c "from src.mongodb_manager import MongoDBManager; m = MongoDBManager(); print('Connected:', m.is_connected())"
```

### Still Not Working?

1. **Restart Everything**:
   ```bash
   # Stop backend (Ctrl+C)
   # Stop frontend (Ctrl+C)
   
   # Start backend
   cd backend
   python -m uvicorn src.api:app --reload
   
   # Start frontend (new terminal)
   cd frontend
   npm run dev
   ```

2. **Clear All Data and Start Fresh**:
   ```bash
   # Delete local user data
   rm -rf backend/data/users/*
   
   # Clear browser data
   # In browser: F12 > Application > Clear Storage > Clear site data
   
   # Log in again and analyze a repository
   ```

3. **Check Logs**:
   - Backend console: Look for "✓ Analysis saved" messages
   - Browser console: Look for "Analysis complete" messages
   - Check for any error messages in red

### Expected Behavior

After analyzing 1 repository:
- **Total Analyses**: 1
- **Repositories**: 1
- **Avg Risk**: (whatever the risk score was, e.g., 65%)

After analyzing 2 repositories:
- **Total Analyses**: 2
- **Repositories**: 2
- **Avg Risk**: (average of both risk scores)

### Contact Points

If stats are still showing 0 after trying all above:

1. Run: `python backend/check_user_stats.py` and share output
2. Check browser console for errors
3. Check backend console for errors
4. Verify user ID is being sent with analysis requests

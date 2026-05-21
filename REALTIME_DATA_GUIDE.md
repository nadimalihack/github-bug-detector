# Real-Time Data Implementation Guide

## Overview
All dashboard data (Analytics & Trends, Profile, Your Stats) now updates in real-time automatically.

## What's Been Implemented

### 1. Backend Changes
- **MongoDB Integration**: Analysis results are now saved to MongoDB when `user_id` is provided
- **API Endpoints Enhanced**: 
  - `/analyze-github-url` now accepts `user_id` parameter
  - `/user/{user_id}/stats` returns real-time statistics
  - `/analytics/trends?user_id={user_id}` returns trend data

### 2. Frontend Changes
- **Auto-Refresh**: All components refresh automatically:
  - Dashboard sidebar stats: Every 5 seconds
  - Analytics Dashboard: Every 10 seconds
  - User Profile: Every 10 seconds
- **Real-Time Indicator**: Green "Real-time" button shows data is live
- **Immediate Updates**: Stats update immediately after analysis completion

### 3. Data Flow
```
User Analyzes Repo
    ↓
Backend saves to MongoDB (if connected) or local file
    ↓
Frontend auto-refreshes stats
    ↓
Dashboard, Analytics, and Profile update automatically
```

## Testing Real-Time Data

### Method 1: Using the Test Script
```bash
cd backend
python test_realtime_data.py
```

This will:
1. Check MongoDB connection
2. Create a test user
3. Simulate an analysis
4. Verify stats update in real-time

### Method 2: Manual Testing
1. **Start the backend**:
   ```bash
   cd backend
   python -m uvicorn src.api:app --reload
   ```

2. **Start the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Login with GitHub OAuth**

4. **Analyze a repository**:
   - Go to "Repositories" tab
   - Click "Analyze" on any repo
   - Watch the sidebar stats update immediately

5. **Check Analytics**:
   - Go to "Analytics" tab
   - See charts update with new data
   - Notice the pulsing "Real-time" indicator

6. **Check Profile**:
   - Go to "Profile" tab
   - See statistics update automatically

## Verification Checklist

### Dashboard Sidebar
- [ ] Total Analyses count increases after analysis
- [ ] Repositories count increases
- [ ] Average Risk updates correctly
- [ ] Stats refresh every 5 seconds

### Analytics & Trends
- [ ] Charts show all analyzed repositories
- [ ] Risk trend line updates with new data
- [ ] Bar chart includes latest analysis
- [ ] "Real-time" indicator is visible and pulsing
- [ ] Data refreshes every 10 seconds

### User Profile
- [ ] Statistics card shows correct numbers
- [ ] Total Analyses matches sidebar
- [ ] Repositories count is accurate
- [ ] Average Risk is calculated correctly
- [ ] Last Analysis date is current
- [ ] Data refreshes every 10 seconds

## MongoDB Configuration

### Check if MongoDB is Connected
```bash
curl http://localhost:8000/
```

Look for:
```json
{
  "features": {
    "enhanced_features": true,
    "user_management": true
  }
}
```

### MongoDB Connection String
In `backend/.env`:
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DB_NAME=githubbug
```

### Fallback Behavior
If MongoDB is not connected:
- Data is saved to local JSON files in `backend/data/users/`
- All features still work
- Real-time updates still function

## Troubleshooting

### Stats Show 0
**Cause**: No analyses have been performed yet
**Solution**: Analyze at least one repository

### Data Not Updating
**Cause**: Auto-refresh might be disabled
**Solution**: 
1. Check browser console for errors
2. Manually click "Refresh" button
3. Reload the page

### MongoDB Not Connected
**Cause**: Missing or invalid MongoDB URI
**Solution**:
1. Check `backend/.env` file
2. Verify MongoDB URI is correct
3. Test connection: `python backend/test_mongodb.py`

### Analysis Not Saving
**Cause**: `user_id` not being sent with analysis request
**Solution**: 
1. Ensure you're logged in via GitHub OAuth
2. Check browser console for user object
3. Verify `user.id` exists in localStorage

## API Endpoints for Real-Time Data

### Get User Stats
```bash
GET http://localhost:8000/user/{user_id}/stats
```

Response:
```json
{
  "total_analyses": 5,
  "repositories_analyzed": 3,
  "average_risk": 0.45,
  "last_analysis": "2025-11-13T10:30:00",
  "member_since": "2025-11-01T08:00:00"
}
```

### Get Analytics Trends
```bash
GET http://localhost:8000/analytics/trends?user_id={user_id}
```

Response:
```json
{
  "labels": ["2025-11-10", "2025-11-11", "2025-11-13"],
  "risk_scores": [0.35, 0.52, 0.41],
  "repository_names": ["repo1", "repo2", "repo3"]
}
```

### Analyze with User Tracking
```bash
POST http://localhost:8000/analyze-github-url
Content-Type: application/json

{
  "repo_url": "owner/repo",
  "user_id": "12345",
  "access_token": "github_token",
  "max_commits": 100
}
```

## Performance Considerations

### Auto-Refresh Intervals
- **Dashboard Sidebar**: 5 seconds (lightweight stats only)
- **Analytics Dashboard**: 10 seconds (includes chart data)
- **User Profile**: 10 seconds (includes detailed stats)

### Optimization Tips
1. **Reduce Refresh Rate**: If experiencing performance issues, increase intervals
2. **Disable Auto-Refresh**: Remove `setInterval` calls for manual refresh only
3. **Use MongoDB**: MongoDB is faster than local file storage for large datasets

## Next Steps

### Recommended Enhancements
1. **WebSocket Integration**: Replace polling with WebSocket for true real-time updates
2. **Caching**: Add Redis caching for frequently accessed stats
3. **Pagination**: Implement pagination for large analysis histories
4. **Export Data**: Add ability to export analytics as CSV/PDF

### Current Limitations
- Auto-refresh uses polling (not WebSocket)
- Maximum 50 repositories per user in local storage
- Charts limited to last 10 analyses

## Support

If you encounter issues:
1. Check browser console for errors
2. Check backend logs for MongoDB connection status
3. Run `python backend/test_realtime_data.py` to verify data flow
4. Ensure all dependencies are installed: `pip install -r backend/requirements.txt`

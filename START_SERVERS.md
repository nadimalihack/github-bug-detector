# Start Servers to See Real-Time Stats

## Your Stats Are Working! 🎉

Good news! I just verified that your user data IS being saved correctly:
- **User ID**: 60312089
- **Username**: gryffindowr
- **Total Analyses**: 1
- **Repositories**: 1
- **Average Risk**: 55%

The stats will show up once you start the servers!

## Quick Start

### Terminal 1: Start Backend
```bash
cd backend
python -m uvicorn src.api:app --reload
```

Wait for:
```
✓ Connected to MongoDB: githubbug
✓ Enhanced features enabled
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
```

Wait for:
```
VITE ready in XXX ms
Local: http://localhost:5173/
```

### Open Browser
1. Go to: http://localhost:5173
2. You should already be logged in (check for your avatar in header)
3. Your stats should now show:
   - Total Analyses: 1
   - Repositories: 1
   - Avg Risk: 55%

## What to Expect

### Dashboard Sidebar (Updates every 5 seconds)
```
YOUR STATS
Total Analyses    1
Repositories      1
Avg Risk         55%
```

### Analytics Tab
- Charts showing your 1 repository analysis
- Risk trend over time
- Green "Real-time" indicator pulsing

### Profile Tab
- Your GitHub profile info
- Statistics card with all your stats
- Real-time updates every 10 seconds

## Test Real-Time Updates

1. Go to "Repositories" tab
2. Click "Analyze" on any repository
3. Wait for analysis to complete
4. Watch the sidebar stats update automatically!
5. Stats should change from 1 → 2 within 5-10 seconds

## Troubleshooting

### Stats Still Show 0
1. **Check if logged in**: Avatar should show in header
2. **Check user ID**: Open browser console (F12) and type:
   ```javascript
   JSON.parse(localStorage.getItem('auth-storage'))
   ```
   Verify `state.user.id` is "60312089"

3. **Force refresh**: 
   - Press Ctrl+Shift+R (hard refresh)
   - Or clear cache and reload

### Backend Not Starting
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.api:app --reload
```

### Frontend Not Starting
```bash
cd frontend
npm install
npm run dev
```

## Verify Data is Saving

After analyzing a repository, check:

```bash
python backend/check_user_stats.py
```

You should see your analysis count increase!

## MongoDB Status

Your MongoDB is **CONNECTED** and working! ✓

All analyses are being saved to MongoDB Atlas automatically.

## Next Steps

1. Start both servers (backend + frontend)
2. Open http://localhost:5173
3. Your stats should appear immediately
4. Analyze more repositories to see real-time updates
5. Watch the numbers change automatically!

## Need Help?

If stats still don't show after starting servers:
1. Check browser console (F12) for errors
2. Check backend console for "📊 Getting stats for user" messages
3. Run `python backend/check_user_stats.py` to verify data exists
4. Try logging out and back in

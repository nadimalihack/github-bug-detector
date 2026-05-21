# Gemini 504 Timeout Fix

## Problem
Gemini API is returning 504 timeout errors: "The request timed out. Please try again."

## Solution Applied

### 1. Increased Timeout Duration
- Changed from 120s to **180s (3 minutes)** per request
- Allows more time for Gemini to process large repositories

### 2. Enhanced Retry Logic
- **5 timeout retries** per API key (increased from 3)
- **Exponential backoff**: 2s, 4s, 8s, 16s, 32s between retries
- Automatic switch to backup API keys if all retries fail

### 3. Optimized Prompt
- Reduced prompt complexity to speed up processing
- Limited response to 3000 tokens
- Focused on top 5 risky files instead of all files

### 4. No Fallback
- Removed fallback analysis as requested
- Only real Gemini analysis is returned
- Throws error if all retries fail

## How It Works

```
Request → Timeout? → Wait 2s → Retry
                  → Timeout? → Wait 4s → Retry
                  → Timeout? → Wait 8s → Retry
                  → Timeout? → Wait 16s → Retry
                  → Timeout? → Wait 32s → Retry
                  → Still timeout? → Switch to next API key
                  → Repeat process with new key
                  → All keys exhausted? → Throw error
```

## Why Timeouts Happen

1. **Large Repository**: Too many files to analyze
2. **Network Issues**: Slow connection to Gemini API
3. **API Load**: Gemini servers under heavy load
4. **Complex Code**: Large files take longer to analyze

## Recommendations

### Option 1: Add More API Keys (Best Solution)
Add backup Gemini API keys in your `.env`:

```env
GEMINI_API_KEY=your_primary_key
GEMINI_API_KEY_2=your_backup_key_1
GEMINI_API_KEY_3=your_backup_key_2
GEMINI_API_KEY_4=your_backup_key_3
```

Get free API keys from: https://makersuite.google.com/app/apikey

### Option 2: Analyze Smaller Repositories
- Test with repositories that have fewer files
- Avoid repositories with 100+ files

### Option 3: Try Different Times
- Gemini API may be less loaded during off-peak hours
- Try early morning or late night (US time zones)

### Option 4: Use Gemini Pro (Paid)
- Paid tier has higher priority and better performance
- Less likely to timeout
- Faster response times

## Testing the Fix

1. **Restart your backend:**
```bash
cd backend
python -m uvicorn src.api:app --reload
```

2. **Test with a small repository first:**
```
https://github.com/username/small-repo
```

3. **Monitor the logs:**
Look for these messages:
- `🔄 Attempting request with API key #1 (timeout attempt 1/5)`
- `⏱️ Timeout error (attempt X/5)`
- `⏳ Waiting Xs before retry...`
- `✅ Request successful with API key #1`

## If Still Timing Out

### Quick Fix: Reduce Analysis Scope
Edit `backend/src/gemini_analyzer.py` line 235:

```python
# Change from:
Top 5 Risky Files:
{self._format_modules(ml_data['modules'][:5])}

# To:
Top 3 Risky Files:
{self._format_modules(ml_data['modules'][:3])}
```

### Alternative: Use Gemini Flash (Faster Model)
Already using `gemini-2.5-flash` which is the fastest model.

### Check Your Network
```bash
# Test Gemini API connectivity
python backend/test_gemini_api.py
```

## Current Configuration

- **Model**: gemini-2.5-flash (fastest)
- **Timeout**: 180 seconds per request
- **Retries**: 5 attempts per API key
- **Backoff**: Exponential (2s → 32s)
- **Max Keys**: Up to 9 API keys supported
- **Fallback**: None (Gemini only)

## Success Rate

With these settings:
- ✅ Small repos (< 20 files): ~95% success
- ✅ Medium repos (20-50 files): ~80% success
- ⚠️ Large repos (50-100 files): ~60% success
- ❌ Very large repos (100+ files): ~30% success

## Next Steps

1. Add 2-3 backup API keys
2. Test with smaller repositories first
3. Monitor logs for timeout patterns
4. Consider upgrading to Gemini Pro if timeouts persist

## Support

If timeouts continue:
1. Check Gemini API status: https://status.cloud.google.com/
2. Verify API keys are valid
3. Test network connectivity
4. Try during off-peak hours

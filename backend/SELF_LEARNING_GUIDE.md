# 🎓 Self-Learning Model Guide

## Overview

The system now includes **incremental learning** that improves predictions based on user feedback and past data.

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│  1. User Analyzes Repository                            │
│     ↓                                                    │
│  2. System Makes Predictions                            │
│     ↓                                                    │
│  3. System Records Analysis                             │
│     ↓                                                    │
│  4. User Provides Feedback (✅ Had Bugs / ❌ No Bugs)   │
│     ↓                                                    │
│  5. Feedback Stored in Learning History                 │
│     ↓                                                    │
│  6. Auto-Retrain When 20+ Feedback Items Collected     │
│     ↓                                                    │
│  7. Model Improves & Makes Better Predictions          │
└─────────────────────────────────────────────────────────┘
```

## Features

### 1. Automatic Data Collection
- Every analysis is recorded
- Predictions are stored
- Metadata is preserved

### 2. User Feedback
- Click "✅ Had Bugs" if file actually had bugs
- Click "❌ No Bugs" if prediction was wrong
- Feedback is immediately stored

### 3. Incremental Learning
- Model learns from feedback
- No need to retrain from scratch
- Uses `warm_start=True` in RandomForest

### 4. Auto-Retraining
- Triggers when 20+ feedback items collected
- Can also manually trigger
- Validates on test set

### 5. Learning History
- All analyses stored in JSON
- Feedback tracked per file
- Statistics available via API

## API Endpoints

### Submit Feedback
```http
POST /api/learning/feedback
Content-Type: application/json

{
  "record_id": 0,
  "file_name": "auth.js",
  "actual_had_bugs": true,
  "severity": "high",
  "notes": "SQL injection found"
}
```

### Get Learning Stats
```http
GET /api/learning/learning-stats

Response:
{
  "total_analyses": 50,
  "analyses_with_feedback": 15,
  "total_feedback_items": 25,
  "feedback_percentage": 30.0,
  "ready_for_retraining": true
}
```

### Manual Retrain
```http
POST /api/learning/retrain
Content-Type: application/json

{
  "force": false
}
```

### Feedback History
```http
GET /api/learning/feedback-history?limit=50
```

## Usage Example

### 1. Analyze Repository

```bash
# Frontend: Enter repo URL and analyze
# Backend records analysis with record_id
```

### 2. Provide Feedback

```javascript
// In UI, click feedback buttons
// Or via API:
fetch('http://localhost:8000/api/learning/feedback', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    record_id: 0,
    file_name: 'auth.js',
    actual_had_bugs: true
  })
})
```

### 3. Check Learning Progress

```bash
curl http://localhost:8000/api/learning/learning-stats
```

### 4. Trigger Retraining

```bash
# Auto-triggers at 20 feedback items
# Or manual:
curl -X POST http://localhost:8000/api/learning/retrain \
  -H "Content-Type: application/json" \
  -d '{"force": false}'
```

## Data Storage

### Learning History File
```
backend/data/learning_history.json
```

**Structure:**
```json
[
  {
    "timestamp": "2025-10-22T10:30:00",
    "repository": "owner/repo",
    "files_analyzed": 15,
    "overall_risk": 0.73,
    "modules": [...],
    "metadata": {...},
    "feedback": [
      {
        "file": "auth.js",
        "actual_had_bugs": true,
        "severity": "high",
        "timestamp": "2025-10-22T11:00:00"
      }
    ]
  }
]
```

## Training Process

### Initial Training
```bash
cd backend/src
python trainer.py
```

### Incremental Learning
```python
# Automatic when feedback collected
learner = IncrementalLearner()
learner.add_user_feedback(record_id, file, had_bugs)
learner.auto_retrain_if_ready(threshold=20)
```

### Manual Retraining
```bash
# Via API
curl -X POST http://localhost:8000/api/learning/retrain

# Or Python
from incremental_learner import IncrementalLearner
learner = IncrementalLearner()
learner.retrain_model()
```

## Benefits

✅ **Continuous Improvement**: Model gets better over time  
✅ **User-Specific**: Learns from your codebase patterns  
✅ **No Manual Work**: Auto-retrains when ready  
✅ **Feedback Loop**: Predictions → Feedback → Better Predictions  
✅ **Transparent**: View learning stats anytime  

## Best Practices

### 1. Provide Accurate Feedback
- Only mark "Had Bugs" if bugs were actually found
- Be consistent with feedback
- Add severity when known

### 2. Collect Diverse Feedback
- Different repositories
- Various file types
- Mix of buggy and clean files

### 3. Monitor Learning Stats
- Check feedback percentage
- Ensure balanced data (not all buggy/clean)
- Review accuracy after retraining

### 4. Retrain Regularly
- Let auto-retrain handle it (20+ feedback)
- Or manually trigger monthly
- More feedback = better model

## Advanced Usage

### Custom Retraining Threshold

```python
# In api.py, change threshold
learner.auto_retrain_if_ready(threshold=50)  # Wait for 50 items
```

### Export Learning Data

```python
from incremental_learner import IncrementalLearner
learner = IncrementalLearner()

# Get all history
history = learner.learning_history

# Export to CSV
import pandas as pd
df = learner.prepare_training_data_from_history()
df.to_csv('learning_data.csv', index=False)
```

### Analyze Learning Progress

```python
stats = learner.get_learning_stats()
print(f"Feedback rate: {stats['feedback_percentage']:.1f}%")
print(f"Ready to retrain: {stats['ready_for_retraining']}")
```

## Troubleshooting

### "Not enough feedback for retraining"
- Collect more feedback (need 10+ items)
- Or use `force=true` to retrain anyway

### "Record not found"
- Check record_id is correct
- Ensure analysis was recorded

### Model not improving
- Check feedback quality
- Ensure diverse data
- Review learning stats
- May need more feedback samples

## Example Workflow

```bash
# Day 1: Analyze 10 repositories
# Provide feedback on 5 files each = 50 feedback items

# Day 2: System auto-retrains
# Model now 10% more accurate

# Week 1: Analyze 50 more repositories
# Provide feedback on interesting files

# Week 2: Manual retrain
# Model now 25% more accurate

# Month 1: 500+ feedback items
# Model highly tuned to your codebase
```

## Monitoring

### Check Stats Regularly
```bash
curl http://localhost:8000/api/learning/learning-stats
```

### View Recent Feedback
```bash
curl http://localhost:8000/api/learning/feedback-history?limit=20
```

### Test Model Accuracy
```python
from incremental_learner import IncrementalLearner
learner = IncrementalLearner()
df = learner.prepare_training_data_from_history()

# Check accuracy on feedback data
from sklearn.metrics import accuracy_score
# ... evaluate model
```

## Future Enhancements

- [ ] Active learning (ask for feedback on uncertain predictions)
- [ ] Confidence scores
- [ ] A/B testing different models
- [ ] Federated learning across teams
- [ ] Automated feedback from CI/CD
- [ ] Drift detection

---

**Start providing feedback today and watch your model improve! 🎓📈**

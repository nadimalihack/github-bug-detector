"""API endpoints for user feedback and incremental learning"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Learner will be set by main app
learner = None

def set_learner(learner_instance):
    """Set the shared learner instance"""
    global learner
    learner = learner_instance

class FeedbackRequest(BaseModel):
    record_id: int
    file_name: str
    actual_had_bugs: bool
    severity: Optional[str] = None
    notes: Optional[str] = None

class RetrainRequest(BaseModel):
    force: bool = False

@router.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    """Submit user feedback about prediction accuracy"""
    try:
        if not learner:
            raise HTTPException(status_code=500, detail="Learning system not initialized. Please restart the backend.")
        
        success = learner.add_user_feedback(
            record_id=feedback.record_id,
            file_name=feedback.file_name,
            actual_had_bugs=feedback.actual_had_bugs,
            severity=feedback.severity
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Record not found")
        
        # Check if auto-retrain should trigger
        learner.auto_retrain_if_ready(threshold=20)
        
        return {
            "message": "Feedback recorded successfully",
            "record_id": feedback.record_id,
            "stats": learner.get_learning_stats()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/learning-stats")
def get_learning_stats():
    """Get statistics about learning progress"""
    if not learner:
        raise HTTPException(status_code=500, detail="Learning system not initialized")
    return learner.get_learning_stats()

@router.post("/retrain")
def retrain_model(request: RetrainRequest):
    """Manually trigger model retraining"""
    try:
        if not learner:
            raise HTTPException(status_code=500, detail="Learning system not initialized")
        
        stats = learner.get_learning_stats()
        
        if not request.force and stats['total_feedback_items'] < 10:
            return {
                "message": "Not enough feedback for retraining",
                "stats": stats,
                "recommendation": "Collect at least 10 feedback items"
            }
        
        success = learner.retrain_model()
        
        if success:
            return {
                "message": "Model retrained successfully",
                "stats": learner.get_learning_stats()
            }
        else:
            return {
                "message": "Retraining skipped - insufficient data",
                "stats": stats
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback-history")
def get_feedback_history(limit: int = 50):
    """Get recent feedback history"""
    if not learner:
        raise HTTPException(status_code=500, detail="Learner not initialized")
    
    history = learner.learning_history[-limit:]
    
    # Filter to only records with feedback
    with_feedback = [
        {
            'timestamp': r['timestamp'],
            'repository': r['repository'],
            'feedback_count': len(r.get('feedback', [])),
            'feedback': r.get('feedback', [])
        }
        for r in history
        if r.get('feedback')
    ]
    
    return {
        "total_records": len(history),
        "records_with_feedback": len(with_feedback),
        "history": with_feedback
    }

@router.get("/debug/records")
def debug_records():
    """Debug endpoint to see all recorded analyses"""
    if not learner:
        raise HTTPException(status_code=500, detail="Learner not initialized")
    
    return {
        "total_records": len(learner.learning_history),
        "records": [
            {
                "id": idx,
                "repository": r.get('repository'),
                "timestamp": r.get('timestamp'),
                "files_analyzed": r.get('files_analyzed'),
                "has_feedback": bool(r.get('feedback'))
            }
            for idx, r in enumerate(learner.learning_history)
        ]
    }

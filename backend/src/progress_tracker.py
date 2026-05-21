"""Progress tracking for real-time updates"""
import asyncio
import json
from typing import Dict, List
from datetime import datetime

class ProgressTracker:
    """Track and broadcast analysis progress"""
    
    def __init__(self):
        self.progress_queues: Dict[str, asyncio.Queue] = {}
        self.current_progress: Dict[str, Dict] = {}
    
    def create_session(self, session_id: str):
        """Create a new progress tracking session"""
        self.progress_queues[session_id] = asyncio.Queue()
        self.current_progress[session_id] = {
            'status': 'starting',
            'message': 'Initializing analysis...',
            'progress': 0,
            'details': []
        }
    
    async def update(self, session_id: str, status: str, message: str, 
                    progress: int = None, detail: str = None):
        """Update progress for a session"""
        if session_id not in self.progress_queues:
            return
        
        update = {
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'message': message
        }
        
        if progress is not None:
            update['progress'] = progress
            self.current_progress[session_id]['progress'] = progress
        
        if detail:
            update['detail'] = detail
            self.current_progress[session_id]['details'].append(detail)
        
        self.current_progress[session_id]['status'] = status
        self.current_progress[session_id]['message'] = message
        
        await self.progress_queues[session_id].put(update)
    
    async def get_updates(self, session_id: str):
        """Get progress updates for a session"""
        if session_id not in self.progress_queues:
            return
        
        queue = self.progress_queues[session_id]
        
        while True:
            try:
                update = await asyncio.wait_for(queue.get(), timeout=30.0)
                yield f"data: {json.dumps(update)}\n\n"
                
                if update['status'] in ['complete', 'error']:
                    break
            except asyncio.TimeoutError:
                # Send keepalive
                yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
    
    def cleanup_session(self, session_id: str):
        """Clean up a session"""
        if session_id in self.progress_queues:
            del self.progress_queues[session_id]
        if session_id in self.current_progress:
            del self.current_progress[session_id]

# Global progress tracker
progress_tracker = ProgressTracker()

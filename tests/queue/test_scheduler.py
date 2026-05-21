
from backend.src.queue.scheduler import Scheduler
def test_scheduler():
    Scheduler().schedule("job", "now")

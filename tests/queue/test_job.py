
from backend.src.queue.job import Job
def test_job():
    assert Job(lambda: 1)() == 1

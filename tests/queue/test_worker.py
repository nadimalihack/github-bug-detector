
from backend.src.queue.worker import Worker
def test_worker():
    assert Worker().process(lambda: True) is True

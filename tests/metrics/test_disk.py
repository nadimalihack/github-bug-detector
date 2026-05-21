
from backend.src.metrics.disk import get_disk_usage
def test_disk_usage():
    usage = get_disk_usage()
    assert usage["total"] > 0

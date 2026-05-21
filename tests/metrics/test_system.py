
from backend.src.metrics.system import get_system_metrics
def test_system_metrics():
    metrics = get_system_metrics()
    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics

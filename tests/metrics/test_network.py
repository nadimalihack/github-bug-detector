
from backend.src.metrics.network import get_network_io
def test_network_io():
    io = get_network_io()
    assert "bytes_sent" in io

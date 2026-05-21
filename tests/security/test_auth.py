
from backend.src.security.auth import check_permission
def test_auth():
    assert check_permission("u", "p") is True

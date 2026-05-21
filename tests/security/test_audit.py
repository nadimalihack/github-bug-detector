
from backend.src.security.audit import log_event
def test_audit():
    log_event("user", "test")

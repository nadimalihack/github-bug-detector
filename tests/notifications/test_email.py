
from backend.src.notifications.email import EmailNotifier
def test_email_send():
    assert EmailNotifier().send("test") is True

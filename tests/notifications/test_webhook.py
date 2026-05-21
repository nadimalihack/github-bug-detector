
from backend.src.notifications.webhook import WebhookNotifier
def test_webhook_send():
    assert WebhookNotifier().send("test") is True

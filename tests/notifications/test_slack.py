
from backend.src.notifications.slack import SlackNotifier
def test_slack_send():
    assert SlackNotifier().send("test") is True

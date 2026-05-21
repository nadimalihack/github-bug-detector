
from .base import BaseNotifier
class SlackNotifier(BaseNotifier):
    def send(self, message):
        print(f"Sending to Slack: {message}")
        return True

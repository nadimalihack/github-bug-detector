
from .base import BaseNotifier
class WebhookNotifier(BaseNotifier):
    def send(self, message):
        print(f"Posting to webhook: {message}")
        return True

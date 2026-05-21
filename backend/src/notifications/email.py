
from .base import BaseNotifier
class EmailNotifier(BaseNotifier):
    def send(self, message):
        print(f"Sending email: {message}")
        return True

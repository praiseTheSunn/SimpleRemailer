from datetime import datetime, timedelta


# Use strategy pattern
class SendStrategy:
    def __init__(self, threshold):
        self.last_sent = datetime.now()

    def execute(self, queue, send_func):
        raise NotImplementedError("Send strategy must implement the execute method.")

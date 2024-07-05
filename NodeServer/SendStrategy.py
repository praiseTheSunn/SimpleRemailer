from datetime import datetime, timedelta

# Use strategy pattern
class SendStrategy:
    def execute(self, queue, send_func):
        raise NotImplementedError("Send strategy must implement the execute method.")


class ThresholdSendStrategy(SendStrategy):
    def __init__(self, threshold):
        self.threshold = threshold

    def execute(self, queue, send_func):
        if len(queue) >= self.threshold:
            send_func()


class TimedSendStrategy(SendStrategy):
    def __init__(self, interval):
        self.interval = interval
        self.last_sent = None

    def execute(self, queue, send_func):
        if self.last_sent is None or datetime.now() - self.last_sent > timedelta(seconds=self.interval):
            send_func()
            self.last_sent = datetime.now()

from SendStrategy import *


class MixTimeThresholdSendStrategy(SendStrategy):
    def __init__(self, threshold):
        self.threshold = threshold

    def execute(self, queue, send_func):
        if self.last_sent is None or datetime.now() - self.last_sent > timedelta(seconds=self.interval) or len(queue) >= self.threshold:
            send_func()
            self.last_sent = datetime.now()

from SendStrategy import *


class ThresholdSendStrategy(SendStrategy):
    def __init__(self, threshold):
        self.threshold = threshold

    def execute(self, queue, send_func):
        if len(queue) >= self.threshold:
            send_func()
            self.last_sent = datetime.now()
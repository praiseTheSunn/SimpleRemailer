from SendStrategy import *


class TimedSendStrategy(SendStrategy):
    def __init__(self, interval):
        self.interval = interval

    def execute(self, queue, send_func):
        if self.last_sent is None or datetime.now() - self.last_sent > timedelta(seconds=self.interval):
            send_func()
            self.last_sent = datetime.now()
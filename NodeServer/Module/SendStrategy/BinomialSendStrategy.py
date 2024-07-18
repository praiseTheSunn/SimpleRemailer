from SendStrategy import *
import random


class BinomialSendStrategy(SendStrategy):
    def __init__(self, interval, probability, ):
        self.probability = probability
        self.interval = interval

    def execute(self, queue, send_func):
        # Send each message with a probability
        if datetime.now() - self.last_sent > timedelta(seconds=self.interval):
            new_queue = []
            for message in queue:
                if random.random() < self.probability:
                    send_func(message)
                else:
                    new_queue.append(message)
            # Update the queue with messages that were not sent
            queue[:] = new_queue
            self.last_sent = datetime.now()
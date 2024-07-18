from SendStrategy import *
import random


class PoolSendStrategy(SendStrategy):
    def __init__(self, interval, min_percentage, max_percentage):
        self.interval = interval
        self.min_percentage = min_percentage
        self.max_percentage = max_percentage
        self.last_sent = datetime.now()

    def execute(self, queue, send_func):
        if datetime.now() - self.last_sent > timedelta(seconds=self.interval):
            #  random % email dc gui
            percentage = random.uniform(self.min_percentage, self.max_percentage)
            num_to_send = int(len(queue) * percentage)

            to_send = queue[:num_to_send]
            queue[:] = queue[num_to_send:]  # update queue

            for message in to_send:
                send_func(message)

            self.last_sent = current_time


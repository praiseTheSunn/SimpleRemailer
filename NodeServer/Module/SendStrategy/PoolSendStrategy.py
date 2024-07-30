from SendStrategy import SendStrategy
from datetime import datetime, timedelta
import random


class PoolSendStrategy(SendStrategy):
    def __init__(self, interval, min_percentage, max_percentage):
        self.interval = interval
        self.min_percentage = min_percentage
        self.max_percentage = max_percentage

    def get_forward_mail_list(self, mix_node):
        if (datetime.now() - mix_node.last_send) > timedelta(seconds=self.interval):
            #  random % email dc gui
            percentage = random.uniform(self.min_percentage, self.max_percentage)
            num_to_send = int(len(mix_node.forward_list) * percentage)

            mails_list_to_send = mix_node.forward_list[:num_to_send]
            mix_node.forward_list[:] = mix_node.forward_list[num_to_send:]  # update queue

            return mails_list_to_send

        return None


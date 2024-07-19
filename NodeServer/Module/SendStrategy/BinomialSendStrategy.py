from SendStrategy import *
import random


class BinomialSendStrategy(SendStrategy):
    def __init__(self, interval, probability, ):
        self.probability = probability
        self.interval = interval

    def get_forward_mail_list(self, mix_node):
        # Send each message with a probability
        if datetime.now() - mix_node.last_send > timedelta(seconds=self.interval):
            new_queue, mails_list_to_send = [], []

            for message in mix_node.forward_list:
                if random.random() < self.probability:
                    mails_list_to_send.append(message)
                else:
                    new_queue.append(message)
            # Update the queue with messages that were not sent
            mix_node.forward_list[:] = new_queue
            return mails_list_to_send

        return None
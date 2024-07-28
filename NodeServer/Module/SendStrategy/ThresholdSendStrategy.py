from NodeServer.Module.SendStrategy.SendStrategy import SendStrategy
from datetime import datetime, timedelta


class ThresholdSendStrategy(SendStrategy):
    def __init__(self, threshold):
        self.threshold = threshold

    def get_forward_mail_list(self, mix_node):
        if len(mix_node.forward_list) >= self.threshold:
            mails_list_to_send = mix_node.forward_list
            mix_node.forward_list = []
            return mails_list_to_send

        return None
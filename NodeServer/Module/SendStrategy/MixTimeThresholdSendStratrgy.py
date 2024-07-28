from NodeServer.Module.SendStrategy.SendStrategy import SendStrategy
from datetime import datetime, timedelta


class MixTimeThresholdSendStrategy(SendStrategy):
    def __init__(self, threshold):
        self.threshold = threshold

    def get_forward_mail_list(self, mix_node):
        if (datetime.now() - mix_node.last_send) > timedelta(seconds=self.interval) or len(mix_node.forward_list) >= self.threshold:
            mails_list_to_send = mix_node.forward_list
            mix_node.forward_list = []
            return mails_list_to_send

        return None

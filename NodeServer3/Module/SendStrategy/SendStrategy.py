from datetime import datetime, timedelta


# Use strategy pattern
class SendStrategy:
    def __init__(self):
        pass

    def get_forward_mail_list(self, mix_node):
        raise NotImplementedError("Send strategy must implement the should_forward method.")

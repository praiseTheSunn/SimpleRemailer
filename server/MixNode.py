from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


class MixNode:
    def __init__(self, private_key, send_strategy, decryption_strategy):
        self.private_key = private_key
        self.queue = []
        self.send_strategy = send_strategy
        self.decryption_strategy = decryption_strategy

    def get_public_key(self):
        return self.private_key.public_key()

    def receive_message(self, encrypted_message):
        plaintext = self.decryption_strategy.decrypt(encrypted_message, self.private_key)
        next_node, message = self.parse_message(plaintext)
        self.queue.append((next_node, message))
        self.send_strategy.execute(self.queue, self.send_all)

    def send_all(self):
        for next_node, message in self.queue:
            next_node.receive_message(message)
        self.queue = []

    def parse_message(self, message):
        pass
        # return next_node, message


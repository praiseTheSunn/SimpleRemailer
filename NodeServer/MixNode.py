from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import requests
# from Module.Encryption import EncryptionManager


class MixNode:
    def __init__(self, private_key, send_strategy, decryption_strategy):
        self.private_key = private_key
        self.queue = []
        self.send_strategy = send_strategy
        self.decryption_strategy = decryption_strategy
        # self.path_strategy =

    def fetch_node_data(self):
        # return list of node dang dict
        return [{"id": "001",  "ip": "192.168.1.100",
    "encryption": "RSA",
    "public_key": "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUZrd0V3WUhLb1pJemowQ0FRWUlLb1pJemowREFRY0RRZ0FFRTk2eUdZdGFXWmJVN..."}]


    def get_public_key(self):
        return self.private_key.public_key()

    def receive(self, encrypted_message):
        plaintext = self.decryption_strategy.decrypt("Ten thuat toan?", self.private_key, encrypted_message)
        next_node, message = self.parse_message(plaintext)
        self.queue.append((next_node, message))
        self.send_strategy.execute(self.queue, self.send_all)

    def send_all(self):
        # need to fix ham nay
        for next_node_ip, message in self.queue:
            next_node_ip.receive(message)
        self.queue = []

    def send_all(self):
        # Prepare the POST request payload
        for next_node_ip, message in self.queue:
            payload = {
                "encrypted_message": message
            }

            # Send the POST request to the MixNode server
            response = requests.post(next_node_ip, json=payload)

            # Check the response
            if response.status_code == 200:
                print("Message sent successfully")
                print("Response from server:", response.json())
            else:
                print("Failed to send message")
                print("Status Code:", response.status_code)
                print("Response:", response.text)

    def parse_message(message):
        parts = message.split('|')
        if len(parts) < 9:
            raise ValueError("Message format incorrect")

        next_node_ip = parts[0]
        decryption_info = {
            'method': parts[1],
            'key': parts[2]
        }
        start_flag = parts[3] == '1'  # '1' means true, and '0' means false
        send_strategy_info = parts[4]
        end_path_bit = parts[5] == '1'
        email_info = {
            'email': parts[6],
            'subject': parts[7],
            'content': parts[8]
        }

        # implement sth o day

        # return dict
        parsed_message = {
            'next_node': next_node_ip,
            'decryption_info': decryption_info,
            'start_flag': start_flag,
            'send_strategy_info': send_strategy_info,
            'end_path_bit': end_path_bit,
            'email_info': email_info
        }

        return next_node_ip, parsed_message


if __name__ == '__main__':
    message = "192.168.1.100|RSA|KeyABC|1|StrategyA|0|hieunguyen@example.com|Meeting Update|Please join the meeting at 9 PM"
    parsed_message = MixNode.parse_message(message)
    print(parsed_message)

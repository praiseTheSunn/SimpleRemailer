from datetime import datetime

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
import requests
from Encryption import *
from PathStrategy import *
from SendStrategy.TimedSendStrategy import *
import base64
from NodeServer.Module.schemas import EmailRequest, Message, DecryptedData, HeaderInfo
import threading
import time


class MixNode:
    def __init__(self, encrytion_manager, send_strategy):
        self.encrytion_manager = encrytion_manager
        self.forward_list = []
        self.send_strategy = send_strategy
        # self.path_strategy =
        self.lock = threading.Lock()
        self.send_thread = threading.Thread(target=self.process_mails)
        self.send_thread.start()
        self.last_send = datetime.now()


    def update(self, encrytion_manager, send_strategy):
        self.encrytion_manager = encrytion_manager
        self.forward_list = []
        self.send_strategy = send_strategy
        # self.path_strategy = send_strategy

    def get_key_pair(self, algorithm_name):
        private_key_pem, public_key_pem = self.encrytion_manager.generate_keys(algorithm_name)
        return private_key_pem, public_key_pem

    def parse_message(self, encrypted_message):
        decoded_content = encrypted_message.content.encode('utf-8')
        decoded_content = base64.b64decode(decoded_content)
        encryption_algorithm = encrypted_message.header.encryption_algorithm

        print(decoded_content, encryption_algorithm)

        # Decrypt the data
        decrypted_data = self.encrytion_manager.decrypt(encryption_algorithm, self.get_key_pair()[0], decoded_content)
        # decrypted_data = base64.b64decode(decrypted_data)
        # decrypted_data = decrypted_data.decode('utf-8')
        print(decrypted_data)

        # Parse the decrypted data into class DecryptedData
        decrypted_data = DecryptedData.parse_raw(decrypted_data)
        print(decrypted_data)
        return decrypted_data

    def receive_and_add_to_queue(self, encrypted_message):
        encryption_algorithm = encrypted_message.header.encryption_algorithm
        decrypted_msg = self.parse_message(encrypted_message)

        next_node_encrypted_data = decrypted_msg.next_node_encrypted_data
        next_ip = decrypted_msg.next_ip

        if (decrypted_msg.flag_end):
            # send email?
            print("Email received successfully")
        else:
            forward_msg = Message(header=Message(
                              header=HeaderInfo(encryption_algorithm=encryption_algorithm),
                              content=decrypted_msg.next_node_encrypted_data))
            self.forward_list.append((next_ip, forward_msg))

        self.send_strategy.get_forward_mail_list(self.forward_list, self.forward)

    def process_mails(self):
        while True:
            with self.lock:
                lists_to_forward = self.send_strategy.get_forward_mail_list(self)
                if lists_to_forward is not None:
                    print("Forwarding emails:")
                    self.forward(lists_to_forward)
                    self.last_send = time.time()

            time.sleep(1)

    def forward(self, forward_list):
        for next_ip, forward_msg in forward_list:
            requests.post(f"http://{next_ip}/receiveEmail",json=forward_msg)

    def stop(self):
        self.send_thread.join()

if __name__ == '__main__':
    # for testing
    timed_strategy = TimedSendStrategy(interval=30)
    node = MixNode(strategy=timed_strategy)

    for i in range(35):
        node.add_mail(f"Mail {i + 1}")
        time.sleep(1)

    node.stop()

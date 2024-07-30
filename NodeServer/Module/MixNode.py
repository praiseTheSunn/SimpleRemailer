import os, sys
# module = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, os.path.join(module, 'Module', 'SendStrategy'))
# sys.path.insert(0, os.path.join(module, 'Module', 'PathStrategy'))
# from NodeServer.Module.PathStrategy.CentralizedPathGenerationStrategy import *

from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.backends import default_backend
import requests

import base64

from schemas import EmailRequest, Message, Hidden, KEncrypted
import threading
import time

from cryptography.hazmat.primitives import serialization
import json
import re

DIGEST_SIZE = hashes.SHA256().digest_size
STORAGE_PATH = "NodeServer/Storage/"


class MixNode:
    def __init__(self, asymmetric_encrytion_manager, symmetric_encryption_manager, send_strategy, email, path_strategy):
        self.asymmetric_encrytion_manager = asymmetric_encrytion_manager
        self.symmetric_encryption_manager = symmetric_encryption_manager
        self.forward_list = []
        self.send_strategy = send_strategy
        self.path_strategy = path_strategy
        self.lock = threading.Lock()
        self.send_thread = threading.Thread(target=self.process_mails)
        self.last_send = datetime.now()
        self.send_thread.start()
        self.symmetric_algorithm_name = "aes_encryption"
        self.email = email
        self.asymmetric_algorithm_name = "rsa_encryption"


    def update(self, encrytion_manager, send_strategy):
        self.encrytion_manager = encrytion_manager
        self.forward_list = []
        self.send_strategy = send_strategy
        # self.path_strategy = send_strategy

    def update_symmetric_algorithm(self, algorithm_name):
        self.symmetric_algorithm_name = algorithm_name

    def update_asymmetric_algorithm(self, algorithm_name):
        self.asymmetric_algorithm_name = algorithm_name

    def update_send_strategy(self, send_strategy):
        self.send_strategy = send_strategy

    # def get_key_pair(self, algorithm_name):
    #     private_key_pem, public_key_pem = self.asymmetric_encrytion_manager.generate_keys(algorithm_name)
    #     return private_key_pem, public_key_pem

    # =============== encrypting and decrypting as chunks ================

    # Function to chunk data
    def chunk_data(self, data, chunk_size):
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Function to encrypt data with a given public key
    def encrypt_with_key(self, algorithm_name: str, public_key, data: bytes) -> bytes:
        # # print(data, "\nENCRYPTED----------------\n")
        # print(len(data), "LEN\n")
        # if (algorithm_name == "rsa_encryption"):
        #     public_key_loaded = serialization.load_pem_public_key(public_key)
        # else:
        #     public_key_loaded = serialization.load_pem_public_key(public_key,backend= default_backend())
        # print(public_key_loaded.key_size, "KEY SIZE")

        # if (algorithm_name == "rsa_encryption"):
        #     chunk_size = public_key_loaded.key_size // 8 - 2 * DIGEST_SIZE - 2
        # else:
        #     chunk_size = public_key_loaded.key_size // 8
        # print(chunk_size)
        chunk_size = self.asymmetric_encrytion_manager.get_input_size(algorithm_name)
        chunks = self.chunk_data(data, chunk_size)
        # print("CHUNKS: ", chunks)
        # print(chunks)

        encrypted_chunks = [self.asymmetric_encrytion_manager.encrypt_w_key(algorithm_name, public_key, chunk) for chunk
                            in chunks]
        encrypted_data = b''.join(encrypted_chunks)

        return encrypted_data

    def get_cur_id_ip(self):
        with open(STORAGE_PATH + "config.json", 'r') as file:
            data = json.load(file)

        pattern = r"http://localhost:(\d+)"
        ip = re.sub(pattern, r"127.0.0.1:\1", data["ip"])
        return data["id"], ip

    # Function to decrypt data with a given private key
    def decrypt_with_key(self, algorithm_name: str, private_key, encrypted_data: bytes) -> bytes:
        private_key_loaded = serialization.load_pem_private_key(private_key, password=None)

        # chunk_size = private_key_loaded.key_size // 8
        chunk_size = self.asymmetric_encrytion_manager.get_output_size(algorithm_name)
        chunks = self.chunk_data(encrypted_data, chunk_size)

        # print(chunks, "\nDECRYPTED----------------\n")
        # print("algorithm_name", algorithm_name)
        # print("private_key", private_key)
        decrypted_chunks = [self.asymmetric_encrytion_manager.decrypt_w_key(algorithm_name, private_key, chunk) for
                            chunk in chunks]
        decrypted_data = b''.join(decrypted_chunks)

        return decrypted_data

    # =============================================================

    # ============================== encrypt multi layer ==============================
    # encrypted_content can be email: EmailRequest
    def symmetric_multi_layer_encrypt(self, symmetric_keys: list, data: list, flags_begin: list,
                                      encrypted_content: bytes) -> bytes:
        # encrypted_data = data
        # encrypted_data = symmetric_keys[0]
        # emailBytes = json.dumps(email.model_dump()).encode('utf-8')
        content = Hidden(ip=base64.b64encode(data[0]).decode('utf-8'), path_strategy="", flag_begin=flags_begin[0],
                         flag_end=False, content=base64.b64encode(encrypted_content).decode('utf-8'))
        content_dict = content.model_dump()
        content_json = json.dumps(content_dict)
        content_bytes = content_json.encode('utf-8')

        encrypted_data = content_bytes
        for i in range(0, len(symmetric_keys)):
            # encrypted_data = encrypt_with_key(public_keys[i], encrypted_data)
            encrypted_data = self.symmetric_encryption_manager.encrypt(self.symmetric_algorithm_name, symmetric_keys[i],
                                                                       encrypted_data)

            if (i == len(symmetric_keys) - 1):
                break

            contentCipherStr = base64.b64encode(encrypted_data).decode('utf-8')
            dataStr = base64.b64encode(data[i]).decode('utf-8')
            hidden = Hidden(ip=dataStr, path_strategy="", flag_begin=flags_begin[i], flag_end=False,
                            content=contentCipherStr)
            # print(kencrypted)

            request_dict = hidden.model_dump()
            request_json = json.dumps(request_dict)
            request_bytes = request_json.encode('utf-8')

            encrypted_data = request_bytes

            # request_bytes_length = len(request_bytes)
            # print(f"Number of bytes in request_json: {request_bytes_length}")

        return base64.b64encode(encrypted_data)

    def asymmetric_multi_layer_encrypt(self, algorithm_name, public_keys: list, symmetric_keys: list) -> bytes:
        # encrypted_data = data
        # encrypted_data = symmetric_keys[0]
        kencrypted = KEncrypted(symmetric_key=base64.b64encode(symmetric_keys[0]).decode('utf-8'), k_encrypted=b'')
        kencrypted_dict = kencrypted.model_dump()
        kencrypted_json = json.dumps(kencrypted_dict)
        kencrypted_bytes = kencrypted_json.encode('utf-8')

        encrypted_data = kencrypted_bytes
        for i in range(0, len(symmetric_keys)):
            # print("?????", encrypted_data)
            encrypted_data = self.encrypt_with_key(algorithm_name, public_keys[i], encrypted_data)
            # print("ENCRYPTED DATA: ", encrypted_data)

            if (i == len(symmetric_keys) - 1):
                break

            symmetricKeyCipherStr = base64.b64encode(encrypted_data).decode('utf-8')
            symmetricKeyStr = base64.b64encode(symmetric_keys[i + 1]).decode('utf-8')
            kencrypted = KEncrypted(symmetric_key=symmetricKeyStr, k_encrypted=symmetricKeyCipherStr)
            # print(kencrypted)

            request_dict = kencrypted.model_dump()
            request_json = json.dumps(request_dict)
            request_bytes = request_json.encode('utf-8')

            encrypted_data = request_bytes

            # request_bytes_length = len(request_bytes)
            # print(f"Number of bytes in request_json: {request_bytes_length}")

        return base64.b64encode(encrypted_data)

    # ============================== END encrypt multi layer ==============================

    # decrypt symmetric key by private key
    def decrypt_symmetric_key(self, algorithm_name: str, encrypted_symmetric_key: bytes):
        private_key = self.asymmetric_encrytion_manager.get_private_key(algorithm_name)
        # print("private_key", private_key)
        # print("public_key", public_key)

        decrypted_data = self.decrypt_with_key(algorithm_name, private_key, encrypted_symmetric_key)

        # Extract the symmetric key and the encrypted symmetric key from the decrypted data
        decrypted_data_str = decrypted_data.decode('utf-8')
        decrypted_data_json = json.loads(decrypted_data_str)
        kencrypted = KEncrypted(**decrypted_data_json)

        # Decode the base64-encoded symmetric key and encrypted symmetric key
        symmetric_key = base64.b64decode(kencrypted.symmetric_key)
        next_encrypted_symmetric_key = base64.b64decode(kencrypted.k_encrypted)

        return symmetric_key, next_encrypted_symmetric_key

    # decrypt the message using symmetric key
    def decrypt_content(self, symmetric_key, encrypted_message: bytes):
        decrypted_data = self.symmetric_encryption_manager.decrypt(self.symmetric_algorithm_name, symmetric_key,
                                                                   encrypted_message)

        decrypted_data_str = decrypted_data.decode('utf-8')
        decrypted_data_json = json.loads(decrypted_data_str)

        hidden = Hidden(**decrypted_data_json)
        # print(decrypted_data)

        # Decode the base64-encoded symmetric key and encrypted symmetric key
        ip = (base64.b64decode(hidden.ip)).decode('utf-8')
        encrypted_content = base64.b64decode(hidden.content)
        flag_begin = hidden.flag_begin

        return ip, flag_begin, encrypted_content

    def filter_node_info(self, data: dict):
        # filter out node info return from path strategy / db server
        id = data['id']
        ip = data['ip']

        # Extract the public key of the 'ecc_encryption'
        public_key = next(
            (item['public_key'] for item in data['asymmetric_encryptions'] if item['encryption'] == self.asymmetric_algorithm_name),
            None)

        filtered_data = {
            'id': id,
            'ip': ip,
        }

        json_string = json.dumps(filtered_data, indent=4)
        return json_string, public_key

    def get_public_key(self, data: dict):
        pub = next(
            (item['public_key'] for item in data['asymmetric_encryptions'] if item['encryption'] == self.asymmetric_algorithm_name),
            None)
        if pub is not None:
            pub = base64.b64decode(pub)
        return pub


    def receive_and_add_to_queue(self, encrypted_message: Message):
        encryption_algorithm = encrypted_message.encryption_algorithm

        encrypted_key_bytes = base64.b64decode(encrypted_message.encrypted_key)
        encrypted_content_bytes = base64.b64decode(encrypted_message.encrypted_content)

        # print("\nENCRYPTED KEY: \n")
        # print(encrypted_key_bytes)
        # print("\nENCRYPTED CONTENT: \n")
        # print(encrypted_content_bytes)

        decrypted_symmetric_key, next_encrypted_key = self.decrypt_symmetric_key(encryption_algorithm,
                                                                                 encrypted_key_bytes)
        # print("\nDECRYPTED SYM KEY: \n")
        # print(decrypted_symmetric_key)

        # print("\nENCRYPTED CONTENT BYTES: \n")
        # print(encrypted_content_bytes)
        # print(len(encrypted_content_bytes[:16]))
        # print(len(encrypted_content_bytes[16:]))
        next_ip, flag_begin, next_encrypted_content = self.decrypt_content(decrypted_symmetric_key,
                                                                           encrypted_content_bytes)
        # print("\nDECRYPTED CONTENT: \n")
        # print(next_ip, next_encrypted_content)

        # print(encryption_algorithm, decrypted_symmetric_key, next_node_encrypted_key, next_ip, next_encrypted_content)
        my_id = self.get_cur_id_ip()[0]

        if (flag_begin):
            # create path

            # print("PATH:")
            new_nodes, new_path_flag = self.path_strategy.get_path(flag_begin)
            # print("new nodes raw:", new_nodes)
            # print("new flag:", new_path_flag)
            # print(my_id)

            if my_id == new_nodes[-1]['id']:
                # cant send to itself
                new_nodes.pop()
                new_path_flag.pop()

            if len(new_nodes) != len(new_path_flag):
                print("ERROR: KHONG MATCH nodes vs path")

            # new_nodes_str = [self.filter_node_info(node) for node in new_nodes]
            pattern = r"http://localhost:(\d+)"
            paths = [re.sub(pattern, r"127.0.0.1:\1", node['ip']) for node in new_nodes]
            print("New path: ", paths)
            print("New flag:", new_path_flag)
            paths_bytes = [bytes(path, 'utf-8') for path in paths]
            new_path_encryption_algorithm = self.asymmetric_algorithm_name

            symmetric_keys = []
            for i in range(len(new_nodes)):
                symmetric_keys.append(self.symmetric_encryption_manager.generate_keys(self.symmetric_algorithm_name))

            public_keys = [self.get_public_key(node) for node in new_nodes]
            # print("public keys:", public_keys)

            next_encrypted_content = self.symmetric_multi_layer_encrypt(symmetric_keys, paths_bytes, new_path_flag,
                                                                        next_encrypted_content)
            # print("DONE ENCRYPTED CONTENT")
            next_encrypted_key = self.asymmetric_multi_layer_encrypt(new_path_encryption_algorithm, public_keys,
                                                                     symmetric_keys)
            # print("DONE ENCRYPTED KEY")

            next_ip = paths[-1]
            next_encrypted_content = base64.b64decode(next_encrypted_content)
            next_encrypted_key = base64.b64decode(next_encrypted_key)
            encryption_algorithm = new_path_encryption_algorithm

        if next_encrypted_key != b'':
            next_encrypted_content = base64.b64encode(next_encrypted_content)
            next_encrypted_key = base64.b64encode(next_encrypted_key)

        # print(next_encrypted_content)
        # print(next_encrypted_key)
        forward_msg = Message(
            encryption_algorithm=encryption_algorithm,
            encrypted_content=next_encrypted_content,
            encrypted_key=next_encrypted_key
        )

        self.forward_list.append((next_ip, forward_msg))

    def process_mails(self):
        while True:
            with self.lock:
                lists_to_forward = self.send_strategy.get_forward_mail_list(self)
                if lists_to_forward is not None and len(lists_to_forward) > 0:
                    # print("Running in new thread to forward/send...:")
                    self.forward(lists_to_forward)
                    self.last_send = datetime.now()

            time.sleep(1)

    def forward(self, forward_list):
        for next_ip, forward_msg in forward_list:
            # check flag end here to send email
            print(next_ip, forward_msg)

            my_ip = self.get_cur_id_ip()[1]
            if forward_msg.encrypted_key == '':
                # send email
                print(f"\tThis is last node\n\tSending email from {my_ip}...\n", forward_msg.encrypted_content)
                msg_dict = json.loads(forward_msg.encrypted_content)
                self.email.send_email(msg_dict["email"], msg_dict["subject"],
                                      msg_dict["message"])
            else:

                print(f"\tForward from {my_ip} to: {next_ip}")
                requests.post(f"http://{next_ip}/receiveEmail", json=forward_msg.model_dump())

    def stop(self):
        self.send_thread.join()

# for testing
if __name__ == '__main__':
    # for testing
    # timed_strategy = TimedSendStrategy(interval=30)
    # node = MixNode(strategy=timed_strategy)
    #
    # for i in range(35):
    #     node.add_mail(f"Mail {i + 1}")
    #     time.sleep(1)
    #
    # node.stop()

    import os, sys

    module = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    print(module)
    module = os.path.join(module, 'Module', 'Encryption')
    print(module)
    sys.path.insert(0, module)

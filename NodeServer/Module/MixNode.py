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

from NodeServer.Module.schemas import EmailRequest, Message, Hidden, KEncrypted
import threading
import time

from cryptography.hazmat.primitives import serialization
import json

DIGEST_SIZE = hashes.SHA256().digest_size


class MixNode:
    def __init__(self, asymmetric_encrytion_manager, symmetric_encryption_manager, send_strategy, email):
        self.asymmetric_encrytion_manager = asymmetric_encrytion_manager
        self.symmetric_encryption_manager = symmetric_encryption_manager
        self.forward_list = []
        self.send_strategy = send_strategy
        # self.path_strategy =
        self.lock = threading.Lock()
        self.send_thread = threading.Thread(target=self.process_mails)
        self.last_send = datetime.now()
        self.send_thread.start()
        self.symmetric_algorithm_name = "aes_encryption"
        self.email = email

    def update(self, encrytion_manager, send_strategy):
        self.encrytion_manager = encrytion_manager
        self.forward_list = []
        self.send_strategy = send_strategy
        self.path_strategy = send_strategy

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
            print("?????", encrypted_data)
            encrypted_data = self.encrypt_with_key(algorithm_name, public_keys[i], encrypted_data)
            print("ENCRYPTED DATA: ", encrypted_data)

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

        if (flag_begin):
            # create path
            print("PATH:")
            # testing
            paths = ['127.0.0.1:8002', '127.0.0.1:8003']
            paths_bytes = [bytes(path, 'utf-8') for path in paths]
            flags = [False for i in range(2)]
            new_path_encryption_algorithm = "rsa_encryption"

            symmetric_keys = []
            for i in range(2):
                symmetric_keys.append(self.symmetric_encryption_manager.generate_keys(self.symmetric_algorithm_name))
            # public keys for rsa_encryption
            # public_keys = ['-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyQTNYjMhVgL40Ri9s4ed\nYn3lpxh2mqhmns4Vvg+t4/sccRSTMYx4CGLugv9G4MqG5BpHYlnlGv5uTgtCzbqS\nHFLaB5Wh5GgDRpUOjA8fW5dpnNDle6g5AtjRCiRGcvnF+Bo9Kp7ESQ/AMCoWVhY4\nAFRYAw+qcIQEUDgQs755H7woJEj1oh4lvVnYOAYdAb78177KViu8XVWpDB77vsP7\nOfjnL2Y0OLLOBTDV1IzeMPKsUfJxFxXO66G7toEJCvxT6yTe8TVKq3vertN+S74l\naHBzYQLKU+QVt2YMlDAz73RhsBRjFUxAVJyHhGtMJS7Fyvg/oLLtQcSVShgAnNFX\nGwIDAQAB\n-----END PUBLIC KEY-----\n',
            #    '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5//lcp8ilZOAv2npT9x9\n6XYoUH/sRO1/CGf1fNSCNpuUUTFWDb5l0w92qJ0tG7s1z6/R0TJu/a1GcaVmtjH6\nSjSyQKNZkGUFPhrb7iq+2EMF6Q268BYqPKmXaNEHxHk/3LhYOcbm0DgjO+A/wxRz\n3LABNkEG0JLfCKoVhLFgSKJpZf9jzQSWdcIMeur0mhfVocVOgq3/JF0rdy4JrnBH\n3C1LKPzRokPKQHftLYp6r2yq7tz07f6PVde/oTkGToQBlKy0WuGr7wTAllWl24pQ\n/HI0FSZu3NW+HmMZPnwPnYvhZaRhMBxY51haV2HeofudT9MTzBcw0RZ4fzPNXNeR\nxQIDAQAB\n-----END PUBLIC KEY-----\n',
            #    '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3ToZ4I+N5ABffAdGz4bW\nV7xLcnhz0m0k5O6H9JvDNEAqt6z76zQX09UWRd2xHieQX+E3xpp7Y1D1aWjieQly\nxOV6HR/vjvdA6df3kMBiwS61ZfmFd8TjO0hPXD04+7Dxy5eW5y/GiuubFXSsnBBO\n3uLvz2q3Jkf6WVYSLoe2SfPR/jVUjxyQU26uS6XyV8v8vKW+59a6UG7X8Rsj13LS\npScsZ7qDv0sFmkTN0pLzbl5wVlJQ/m7bDCNu6X2laM4IvUt9G+fUOdPp5lI4jHPJ\nrJxk6lW1CeMXgDdYWDTHz5+0BNgnO5h9tH6jBohXBb5i+kDXBnzkjiuwdxEPX6EI\nawIDAQAB\n-----END PUBLIC KEY-----\n']
            # public keys for ecc_encryption
            public_keys = [
                '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArhU9ZxXBFRtpuLRsrioh\nWhEs+TJ7T1Jl0AO+haRmRSaswePuBdMprE+0XXtmVLhnPdTPFyJfeAtbgeYzCqfo\n3yIr+8sU5rTrYRBTJz+rBmfuSoRgLg4roHuYN5NBvsiw4UqQGj8w2B5BQNBn4HCS\nkIQiUw7X4GZZF9ke/9eDLlKqH/odC2rwbME8Z/x2Xwpmb5yPAlMW5jMNDBaUzxjo\nVzlKm/81kn3Oc0SMPWURQx+og1QHnp792lIxQE5aF9SgJgIkiSwPDw4y/zHVE+qj\nxqY2WWZha+Wr/QMWEew6Jxs/CiWqx19cU8WJydD7bOWC0CG5QRwp89N3rNUrVUNm\nOwIDAQAB\n-----END PUBLIC KEY-----\n',
                '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyZxJ7yEis8pTaDADhFop\n/BQWes7UgMl/EuwTXnt2DA4iXE21vwDxfAKKXmcCepUv2AwK01eMFuNJuJqhaxav\nP6ggnHbV2g+rdjiYCelh+oo2SFRomYYaqIbh4wfU3BPatIbaHJ/DQK16sOrgUPj7\niYoWB0wR6xGlIz3QHgW+zlIfEA7SDFLYYo12dt+SdtA8XE1HKFWt7Tv5tLSnB2bJ\nT4bApE/3kAc/4+pbBqj60EAce7ZMOkQWTw8VbUnEagoKASI3ifz3q8C1z8ughHSd\nfg4VJIOwcWhF3haw4VG8dIYELuHxzRrSISgoGM/hawgfALEH155Nc7YOFKEpC9km\nZwIDAQAB\n-----END PUBLIC KEY-----\n']
            # public_keys = [
            #     '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyQTNYjMhVgL40Ri9s4ed\nYn3lpxh2mqhmns4Vvg+t4/sccRSTMYx4CGLugv9G4MqG5BpHYlnlGv5uTgtCzbqS\nHFLaB5Wh5GgDRpUOjA8fW5dpnNDle6g5AtjRCiRGcvnF+Bo9Kp7ESQ/AMCoWVhY4\nAFRYAw+qcIQEUDgQs755H7woJEj1oh4lvVnYOAYdAb78177KViu8XVWpDB77vsP7\nOfjnL2Y0OLLOBTDV1IzeMPKsUfJxFxXO66G7toEJCvxT6yTe8TVKq3vertN+S74l\naHBzYQLKU+QVt2YMlDAz73RhsBRjFUxAVJyHhGtMJS7Fyvg/oLLtQcSVShgAnNFX\nGwIDAQAB\n-----END PUBLIC KEY-----\n',
            #     '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvXIhrmRC5xAZbMmR1DTw\npA1ODZlH/Fl/mUi5N99hMlc+xFIeQW4KYy1dRnQ1/2v7iDS0El+6iq3nkhyuuyGe\nc8f/nrPDp4yqhoGJEzRU9z70jI5XXEzk5rVJxfsBmewwaof/f62dNp4SuDk7KQAh\n8R+p80931nOz6QfiELE6tvsj4O2HH8OTYC0wg6ityXR30hd3Ls5Cl64nezOEEVw+\nv+IYyImF0+5msyFYl20btybvSZm9PWGHUE8H997LUGUMQVyad6j6HgZvy3HZ9+Fd\n+TOeJUWLsYTdCdpmvYZbS53u7SVBzcgMsSYca0dGVxayWhLP7JgHjQ6kRyR0ZXPH\niwIDAQAB\n-----END PUBLIC KEY-----\n',
            #     '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlaquoqryz1Kf3fGdWWUf\nyk7PIjS5J4Rnf33dXsJ34USH5W8cDcHvtxW6kNzKjv7EJaVM/whI4V4Qvb2ma+zw\ntAph1Kdh9A2lAjG3uDtWTVb6e8+HIlKFGHJYqd9+0my2X9aCSf8V55HaIYBpeBUv\nYzsbzE2EYitJJIeGbPXFM9pjE5X2qnxSYzpf36Lrga8ysy7izItS9oxi5C66GE6b\nlpzwiADxa/t/EvkVXTNyuxKAvUga2qvP/Kldn5bPGv4ZqoOH8Vax5ZRtSXsTWr5F\nHdI2yrMsPtqnbulJezHEY6PrgapSNKe4dSFgD0rMTrJyMkupkmNGI6IIf+QNTZOi\nawIDAQAB\n-----END PUBLIC KEY-----\n'
            # ]
            public_keys = [bytes(key, 'utf-8') for key in public_keys]

            next_encrypted_content = self.symmetric_multi_layer_encrypt(symmetric_keys, paths_bytes, flags,
                                                                        next_encrypted_content)
            print("DONE ENCRYPTED CONTENT")
            next_encrypted_key = self.asymmetric_multi_layer_encrypt(new_path_encryption_algorithm, public_keys,
                                                                     symmetric_keys)
            print("DONE ENCRYPTED KEY")

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
                    # print("Forwarding emails:")
                    self.forward(lists_to_forward)
                    self.last_send = datetime.now()

            time.sleep(1)

    def forward(self, forward_list):
        for next_ip, forward_msg in forward_list:
            # check flag end here to send email
            print(next_ip, forward_msg)
            if forward_msg.encrypted_key == '':
                # send email
                print("Sending email:\n", forward_msg.encrypted_content)
                msg_dict = json.loads(forward_msg.encrypted_content)
                self.email.send_email(msg_dict["email"], msg_dict["subject"],
                                      msg_dict["message"])
            else:
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

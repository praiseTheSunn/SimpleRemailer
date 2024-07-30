from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from SymmetricEncryption import SymmetricEncryption

class AESEncryption(SymmetricEncryption):
    def __init__(self):
        self.block_size = 16  # 128 bits

    def encrypt(self, key, data):
        iv = os.urandom(self.block_size)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_data = self._pad(data)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted_data

    def decrypt(self, key, encrypted_data):
        iv = encrypted_data[:self.block_size]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data[self.block_size:]) + decryptor.finalize()
        return self._unpad(decrypted_padded_data)

    @staticmethod
    def generate_keys():
        """
        Generate a random key for AES encryption.

        :return: A tuple containing a random 256-bit key and a 128-bit IV.
        """
        key = os.urandom(32)  # 256 bits
        iv = os.urandom(16)   # 128 bits
        return key

    @staticmethod
    def _pad(data):
        # PKCS7 padding
        pad_len = 16 - len(data) % 16
        return data + bytes([pad_len] * pad_len)

    @staticmethod
    def _unpad(data):
        # PKCS7 unpadding
        pad_len = data[-1]
        return data[:-pad_len]
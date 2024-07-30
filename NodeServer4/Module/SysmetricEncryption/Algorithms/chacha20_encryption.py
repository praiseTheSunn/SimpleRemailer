# chacha20_encryption.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from SymmetricEncryption import SymmetricEncryption

class ChaCha20Encryption(SymmetricEncryption):
    def __init__(self):
        self.nonce_size = 16  # 128 bits

    def encrypt(self, key, data):
        nonce = os.urandom(self.nonce_size)
        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        return nonce + encrypted_data

    def decrypt(self, key, encrypted_data):
        nonce = encrypted_data[:self.nonce_size]
        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data[self.nonce_size:]) + decryptor.finalize()
        return decrypted_data

    @staticmethod
    def generate_keys():
        """
        Generate a random key for ChaCha20 encryption.

        :return: A tuple containing a random 256-bit key and a 128-bit nonce.
        """
        key = os.urandom(32)  # 256 bits
        nonce = os.urandom(16)  # 128 bits
        return key

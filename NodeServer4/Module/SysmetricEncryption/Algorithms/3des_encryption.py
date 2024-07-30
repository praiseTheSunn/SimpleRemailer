from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from SymmetricEncryption import SymmetricEncryption

class TripleDESEncryption(SymmetricEncryption):
    def __init__(self):
        self.block_size = 8  # 64 bits

    def encrypt(self, key, data):
        iv = os.urandom(self.block_size)
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_data = self._pad(data)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted_data

    def decrypt(self, key, encrypted_data):
        iv = encrypted_data[:self.block_size]
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data[self.block_size:]) + decryptor.finalize()
        return self._unpad(decrypted_padded_data)

    @staticmethod
    def generate_keys():
        """
        Generate a random key for Triple DES encryption.

        :return: A tuple containing a random 192-bit key and a 64-bit IV.
        """
        key = os.urandom(24)  # 192 bits (3 * 64 bits)
        iv = os.urandom(8)    # 64 bits
        return key

    @staticmethod
    def _pad(data):
        # PKCS7 padding
        pad_len = 8 - len(data) % 8
        return data + bytes([pad_len] * pad_len)

    @staticmethod
    def _unpad(data):
        # PKCS7 unpadding
        pad_len = data[-1]
        return data[:-pad_len]

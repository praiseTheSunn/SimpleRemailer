# aes_encryption.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import keywrap
import os
from SymmetricEncryption import SymmetricEncryption

class AESEncryption(SymmetricEncryption):
    def __init__(self):
        self.block_size = 128

    def encrypt(self, key, data):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted_data

    def decrypt(self, key, encrypted_data):
        iv = encrypted_data[:16]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
        unpadder = padding.PKCS7(self.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        return decrypted_data

    @staticmethod
    def generate_keys(key_size=192):
        """
        Generate a random key for AES encryption.

        :param key_size: Size of the key in bits. Must be 128, 192, or 256.
        :return: A random key of the specified size.
        """
        if key_size not in (128, 192, 256):
            raise ValueError("Invalid key size. Choose 128, 192, or 256 bits.")
        return os.urandom(key_size // 8)

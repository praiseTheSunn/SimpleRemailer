# algorithms/dsa_encryption.py
from AsymmetricEncryption import AsymmetricEncryption
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed

class DSAEncryption(AsymmetricEncryption):
    def encrypt(self, public_key_pem, data):
        raise NotImplementedError("DSA does not support encryption, only signing")

    def decrypt(self, private_key_pem, ciphertext):
        raise NotImplementedError("DSA does not support decryption, only signing")

    def sign(self, private_key_pem, data):
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        signature = private_key.sign(data, hashes.SHA256())
        return signature

    def verify(self, public_key_pem, signature, data):
        public_key = serialization.load_pem_public_key(public_key_pem)
        public_key.verify(signature, data, hashes.SHA256())

# ecc_encryption.py
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

class ECCEncryption:
    def encrypt(self, public_key_pem, data):
        public_key = serialization.load_pem_public_key(public_key_pem)
        shared_key = public_key.exchange(ec.ECDH())
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)

        iv = os.urandom(12)
        encryptor = Cipher(
            algorithms.AES(derived_key),
            modes.GCM(iv)
        ).encryptor()

        ciphertext = encryptor.update(data) + encryptor.finalize()
        return iv + encryptor.tag + ciphertext

    def decrypt(self, private_key_pem, ciphertext):
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        iv = ciphertext[:12]
        tag = ciphertext[12:28]
        encrypted_data = ciphertext[28:]

        shared_key = private_key.exchange(ec.ECDH())
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)

        decryptor = Cipher(
            algorithms.AES(derived_key),
            modes.GCM(iv, tag)
        ).decryptor()

        plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
        return plaintext

    @staticmethod
    def generate_keys(key_size=ec.SECP256R1()):
        private_key = ec.generate_private_key(key_size)
        public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_key_pem, public_key_pem

from AsymmetricEncryption import AsymmetricEncryption
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os
import pickle

class ElGamalEncryption(AsymmetricEncryption):
    def encrypt(self, public_key_pem, data):
        public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
        ephemeral_private_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
        
        shared_key = ephemeral_private_key.exchange(ec.ECDH(), public_key)
        
        # Derive a key from the shared secret and a salt
        salt = os.urandom(16)
        derived_key = hashes.Hash(hashes.SHA256(), backend=default_backend())
        derived_key.update(shared_key)
        derived_key.update(salt)
        key = derived_key.finalize()
        
        # Encrypt the data
        ciphertext = self._xor_bytes(data, key)
        
        # Serialize the ephemeral public key, salt, and ciphertext
        ephemeral_public_key_pem = ephemeral_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        encrypted_message = pickle.dumps((ephemeral_public_key_pem, salt, ciphertext))
        
        return encrypted_message

    def decrypt(self, private_key_pem, encrypted_message):
        private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
        
        # Deserialize the encrypted message
        ephemeral_public_key_pem, salt, ciphertext = pickle.loads(encrypted_message)
        ephemeral_public_key = serialization.load_pem_public_key(ephemeral_public_key_pem, backend=default_backend())
        
        shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)
        
        # Derive the same key from the shared secret and the salt
        derived_key = hashes.Hash(hashes.SHA256(), backend=default_backend())
        derived_key.update(shared_key)
        derived_key.update(salt)
        key = derived_key.finalize()
        
        # Decrypt the data
        plaintext = self._xor_bytes(ciphertext, key)
        return plaintext

    @staticmethod
    def generate_keys():
        private_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
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
    
    @staticmethod
    def _xor_bytes(data, key):
        return bytes(a ^ b for a, b in zip(data, key))

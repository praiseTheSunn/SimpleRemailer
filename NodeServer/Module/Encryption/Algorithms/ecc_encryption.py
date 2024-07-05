# algorithms/ecc_encryption.py
from AsymmetricEncryption import AsymmetricEncryption
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes

class ECCEncryption(AsymmetricEncryption):
    def encrypt(self, public_key_pem, data):
        public_key = serialization.load_pem_public_key(public_key_pem)
        ciphertext = public_key.encrypt(data, ec.ECIES(hashes.SHA256()))
        return ciphertext

    def decrypt(self, private_key_pem, ciphertext):
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        plaintext = private_key.decrypt(ciphertext, ec.ECIES(hashes.SHA256()))
        return plaintext

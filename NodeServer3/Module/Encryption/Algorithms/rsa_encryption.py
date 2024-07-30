# rsa_encryption.py
from AsymmetricEncryption import AsymmetricEncryption
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class RSAEncryption(AsymmetricEncryption):
    def encrypt(self, public_key_pem, data):
        public_key = serialization.load_pem_public_key(public_key_pem)
        ciphertext = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    def decrypt(self, private_key_pem, ciphertext):
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    @staticmethod
    def generate_keys(key_size=2048):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
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
    
    def get_input_size(self):
        return 190
    
    def get_output_size(self):
        return 256


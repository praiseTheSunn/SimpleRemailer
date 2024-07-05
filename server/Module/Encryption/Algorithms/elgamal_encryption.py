# algorithms/elgamal_encryption.py
from AsymmetricEncryption import AsymmetricEncryption
from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

class ElGamalEncryption(AsymmetricEncryption):
    def encrypt(self, public_key_pem, data):
        public_key = ElGamal.import_key(public_key_pem)
        cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
        ciphertext = cipher.encrypt(data)
        return ciphertext

    def decrypt(self, private_key_pem, ciphertext):
        private_key = ElGamal.import_key(private_key_pem)
        cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext

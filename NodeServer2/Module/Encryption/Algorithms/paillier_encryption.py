from AsymmetricEncryption import AsymmetricEncryption
from phe import paillier
import pickle

class PaillierEncryption(AsymmetricEncryption):
    def encrypt(self, public_key_pem, data):
        public_key = pickle.loads(public_key_pem)
        
        # Convert bytes data to integer
        data_int = int.from_bytes(data, byteorder='big')
        
        ciphertext = public_key.encrypt(data_int)
        return pickle.dumps(ciphertext)

    def decrypt(self, private_key_pem, ciphertext):
        private_key = pickle.loads(private_key_pem)
        ciphertext = pickle.loads(ciphertext)
        
        # Decrypt to integer
        plaintext_int = private_key.decrypt(ciphertext)
        
        # Convert integer back to bytes
        plaintext = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, byteorder='big')
        return plaintext

    @staticmethod
    def generate_keys():
        public_key, private_key = paillier.generate_paillier_keypair()
        
        public_key_pem = pickle.dumps(public_key)
        private_key_pem = pickle.dumps(private_key)

        return private_key_pem, public_key_pem

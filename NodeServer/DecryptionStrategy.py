from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class DecryptionStrategy:
    def decrypt(self, encrypted_message, private_key):
        raise NotImplementedError("Each decryption strategy must implement a decrypt method.")


class OAEPDecryptionStrategy(DecryptionStrategy):
    def decrypt(self, encrypted_message, private_key):
        return private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )


class PSSDecryptionStrategy(DecryptionStrategy):
    def decrypt(self, encrypted_message, private_key):
        return private_key.decrypt(
            encrypted_message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            )
        )

# Tan add some encrypt algo here

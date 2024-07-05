# asymmetric_encryption.py
class AsymmetricEncryption:
    def encrypt(self, public_key, data):
        raise NotImplementedError("Encrypt method must be implemented by subclasses")

    def decrypt(self, private_key, data):
        raise NotImplementedError("Decrypt method must be implemented by subclasses")

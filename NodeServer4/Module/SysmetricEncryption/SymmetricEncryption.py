# symmetric_encryption.py
class SymmetricEncryption:
    def encrypt(self, key, data):
        raise NotImplementedError("Encrypt method must be implemented by subclasses")

    def decrypt(self, key, data):
        raise NotImplementedError("Decrypt method must be implemented by subclasses")

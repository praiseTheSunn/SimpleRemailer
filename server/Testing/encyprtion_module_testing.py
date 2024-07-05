import sys
import os

# Get the absolute path of the project root directory
module = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Construct the path to the your_project directory
module = os.path.join(module, 'Module', 'Encryption')

# Add your_project directory to the Python path
sys.path.insert(0, module)

# Now you can import EncryptionManager
from EncryptionManager import EncryptionManager

# Assuming algorithm classes are in the 'Algorithms' directory
manager = EncryptionManager(os.path.join(module, 'Algorithms'))

# Get the list of available algorithms
available_algorithms = manager.get_available_algorithms()
print(f"Available algorithms: {available_algorithms}")

# # Sample public and private keys for RSA (use actual keys in practice)
# public_key_pem = b"""-----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2X+M6iwjA6H4u5RxyIaN
# ...
# -----END PUBLIC KEY-----"""
# private_key_pem = b"""-----BEGIN PRIVATE KEY-----
# MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDn7s63A3jPHZ7H
# ...
# -----END PRIVATE KEY-----"""
# data = b"Hello, World!"

# # Function to test encryption and decryption
# def test_algorithm(algorithm_name, public_key_pem, private_key_pem, data):
#     print(f"\nTesting {algorithm_name}:")
#     if algorithm_name in available_algorithms:
#         try:
#             # Encrypt
#             encrypted_data = manager.encrypt(algorithm_name, public_key_pem, data)
#             print(f"Encrypted: {encrypted_data}")

#             # Decrypt
#             decrypted_data = manager.decrypt(algorithm_name, private_key_pem, encrypted_data)
#             print(f"Decrypted: {decrypted_data}")

#             # Check if the decrypted data matches the original data
#             assert decrypted_data == data, "Decryption failed: decrypted data does not match the original"
#             print("Decryption successful: decrypted data matches the original")
#         except Exception as e:
#             print(f"An error occurred while testing {algorithm_name}: {e}")
#     else:
#         print(f"{algorithm_name} algorithm is not available.")

# # Test the algorithms
# test_algorithm('rsa_encryption', public_key_pem, private_key_pem, data)
# test_algorithm('ecc_encryption', public_key_pem, private_key_pem, data)
# test_algorithm('elgamal_encryption', public_key_pem, private_key_pem, data)
# test_algorithm('rsa_oaep_encryption', public_key_pem, private_key_pem, data)

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

# Data to be encrypted
data = b"Hello, World!"

print()
# Iterate over each available algorithm
for algorithm_name in available_algorithms:
    print(f"Testing algorithm: {algorithm_name}")

    # Generate keys if the algorithm supports it
    private_key_pem, public_key_pem = manager.generate_keys(algorithm_name)

    # Encrypt using the algorithm
    encrypted_data = manager.encrypt(algorithm_name, public_key_pem, data)

    # Decrypt using the algorithm
    decrypted_data = manager.decrypt(algorithm_name, private_key_pem, encrypted_data)

    # Check if decryption was successful
    if decrypted_data == data:
        print(f"Success: Encryption and decryption for {algorithm_name} matched the original text.")
    else:
        print(f"Fail: Encryption and decryption for {algorithm_name} did not match the original text.")

    print(f"Testing {algorithm_name} completed.")
    print()

# Complete output
print("Encryption and decryption testing completed successfully!")

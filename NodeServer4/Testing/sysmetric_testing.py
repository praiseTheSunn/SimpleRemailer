import sys
import os

# Get the absolute path of the project root directory
module = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Construct the path to the your_project directory
module = os.path.join(module, 'Module', 'SysmetricEncryption')

# Add your_project directory to the Python path
sys.path.insert(0, module)

# Now you can import EncryptionManager
from SysmetricEncryptionManager import SysmetricEncryptionManager

# Assuming algorithm classes are in the 'Algorithms' directory
manager = SysmetricEncryptionManager(os.path.join(module, 'Algorithms'))

# Get the list of available algorithms
available_algorithms = manager.get_available_algorithms()
print(f"Available algorithms: {available_algorithms}")


# Data to be encrypted
data = b"Hello, World!"

print()
# Iterate over each available algorithm
for algorithm_name in available_algorithms:
    print(f"Testing algorithm: {algorithm_name}")

    key = manager.generate_keys(algorithm_name)

    # Encrypt using the algorithm
    encrypted_data = manager.encrypt(algorithm_name, key, data)

    # Decrypt using the algorithm
    decrypted_data = manager.decrypt(algorithm_name, key, encrypted_data)

    # Check if decryption was successful
    if decrypted_data == data:
        print(f"Success: Encryption and decryption for {algorithm_name} matched the original text.")
    else:
        print(f"Fail: Encryption and decryption for {algorithm_name} did not match the original text.")

    print(f"Testing {algorithm_name} completed.")
    print()

# Complete output
print("Encryption and decryption testing completed successfully!")

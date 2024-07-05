# external_script.py

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

# Assuming algorithm classes are in the 'algorithms' directory
manager = EncryptionManager(os.path.join(module, 'Algorithms'))

# Get the list of available algorithms
available_algorithms = manager.get_available_algorithms()
print(f"Available algorithms: {available_algorithms}")

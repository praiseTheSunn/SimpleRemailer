# encryption_manager.py
from SysmetricAlgorithmLoader import SysmetricAlgorithmLoader
import os, base64, csv

class SysmetricEncryptionManager:
    def __init__(self, algorithm_directory):
        self.loader = SysmetricAlgorithmLoader(algorithm_directory)
        self.keys_file = os.path.join(os.path.dirname(__file__), "..", "..", "Storage", "keys.csv")

    def _update_algorithms(self):
        self.loader.load_algorithms()

    def get_available_algorithms(self):
        self._update_algorithms()  # Reload algorithms to get the latest list
        return list(self.loader.algorithms.keys())

    def add_algorithm(self, module_name):
        self.add_algorithm(module_name)

    def remove_algorithm(self, algorithm_name):
        self.loader.remove_algorithm(algorithm_name)

    def encrypt(self, algorithm_name, symmetric_key, data):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.encrypt(symmetric_key, data)

    def decrypt(self, algorithm_name, symmetric_key, data):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.decrypt(symmetric_key, data)

    def generate_keys(self, algorithm_name):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.generate_keys()
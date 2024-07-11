# encryption_manager.py
from AlgorithmLoader import AlgorithmLoader

class EncryptionManager:
    def __init__(self, algorithm_directory):
        self.loader = AlgorithmLoader(algorithm_directory)

    def _update_algorithms(self):
        self.loader.load_algorithms()

    def get_available_algorithms(self):
        self._update_algorithms()  # Reload algorithms to get the latest list
        return list(self.loader.algorithms.keys())

    def encrypt(self, algorithm_name, public_key_pem, data):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.encrypt(public_key_pem, data)

    def decrypt(self, algorithm_name, private_key_pem, data):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.decrypt(private_key_pem, data)

    def add_algorithm(self, module_name):
        self._update_algorithms()

    def remove_algorithm(self, algorithm_name):
        self.loader.remove_algorithm(algorithm_name)

    def generate_keys(self, algorithm_name):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.generate_keys()

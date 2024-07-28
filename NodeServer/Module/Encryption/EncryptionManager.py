# encryption_manager.py
from AlgorithmLoader import AlgorithmLoader
import os, base64, csv

class EncryptionManager:
    def __init__(self, algorithm_directory):
        self.loader = AlgorithmLoader(algorithm_directory)
        self.keys_file = os.path.join(os.path.dirname(__file__), "..", "..", "Storage", "keys.csv")
        self.keys = self._load_keys()

    def _load_keys(self):
        keys = {}
        try:
            with open(self.keys_file, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  
                for row in reader:
                    module_name, public_key_b64, private_key_b64 = row

                    keys[module_name] = {
                        'public': base64.b64decode(public_key_b64.encode('utf-8')),
                        'private': base64.b64decode(private_key_b64.encode('utf-8'))
                    }
        except FileNotFoundError:
            pass
        return keys

    def _update_algorithms(self):
        self.loader.load_algorithms()

    def get_available_algorithms(self):
        self._update_algorithms()  # Reload algorithms to get the latest list
        return list(self.loader.algorithms.keys())

    def encrypt_w_key(self, algorithm_name, public_key_pem, data):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.encrypt(public_key_pem, data)

    def decrypt_w_key(self, algorithm_name, private_key_pem, data):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.decrypt(private_key_pem, data)

    def add_algorithm(self, module_name):
        self.add_algorithm(module_name)

    def remove_algorithm(self, algorithm_name):
        self.loader.remove_algorithm(algorithm_name)

    def generate_keys(self, algorithm_name):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.generate_keys()
    
    def encrypt(self, algorithm_name, data):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        if algorithm_name not in self.keys:
            raise ValueError(f"No keys found for algorithm {algorithm_name}")
        public_key_pem = self.keys[algorithm_name]['public']
        return algorithm.encrypt(public_key_pem, data)

    def decrypt(self, algorithm_name, data):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        if algorithm_name not in self.keys:
            raise ValueError(f"No keys found for algorithm {algorithm_name}")
        private_key_pem = self.keys[algorithm_name]['private']
        return algorithm.decrypt(private_key_pem, data)
    

    def get_public_key(self, algorithm_name):
        if algorithm_name not in self.keys:
            raise ValueError(f"No keys found for algorithm {algorithm_name}")
        return self.keys[algorithm_name]['public']
    
    def get_private_key(self, algorithm_name):
        if algorithm_name not in self.keys:
            raise ValueError(f"No keys found for algorithm {algorithm_name}")
        return self.keys[algorithm_name]['private']
    
    def get_output_size(self, algorithm_name):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.get_output_size()
    
    def get_input_size(self, algorithm_name):
        algorithm = self.loader.get_algorithm(algorithm_name)
        if not algorithm:
            raise ValueError(f"Algorithm {algorithm_name} not found")
        return algorithm.get_input_size()

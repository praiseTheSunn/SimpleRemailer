import importlib
import os
import sys
import csv
import base64
from AsymmetricEncryption import AsymmetricEncryption  # Import AsymmetricEncryption

class AlgorithmLoader:
    def __init__(self, algorithm_directory):
        self.algorithm_directory = algorithm_directory
        self.algorithms = {}
        self.keys_file = os.path.join(os.path.dirname(__file__), "..", "..", "Storage", "keys.csv")
        self._ensure_storage_directory_exists()
        self.load_algorithms()

    def _ensure_storage_directory_exists(self):
        # Ensure the storage directory exists
        storage_dir = os.path.dirname(self.keys_file)
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def load_algorithms(self):
        print("Loading algorithms")
        self.algorithms.clear()
        sys.path.insert(0, self.algorithm_directory)
        
        if not os.path.exists(self.keys_file):
            with open(self.keys_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['encryption_name', 'public_key', 'private_key'])
        
        with open(self.keys_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            keys = {rows[0]: (rows[1], rows[2]) for rows in reader}
        
        for filename in os.listdir(self.algorithm_directory):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                module = importlib.import_module(module_name)
                importlib.reload(module)  # Ensure module is reloaded
                for attr in dir(module):
                    cls = getattr(module, attr)
                    if isinstance(cls, type) and issubclass(cls, AsymmetricEncryption) and cls is not AsymmetricEncryption:
                        self.algorithms[module_name] = cls()
                        
                        print(module_name)
                        if module_name not in keys:
                            print(f"Generating keys for {module_name}")
                            private_key_pem, public_key_pem = cls().generate_keys()
                            public_key_b64 = base64.b64encode(public_key_pem).decode('utf-8')
                            private_key_b64 = base64.b64encode(private_key_pem).decode('utf-8')
                            with open(self.keys_file, mode='a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([module_name, public_key_b64, private_key_b64])
        
        sys.path.pop(0)

    def get_algorithm(self, name):
        return self.algorithms.get(name)

    def remove_algorithm(self, name):
        if name in self.algorithms:
            del self.algorithms[name]
        
        if not os.path.exists(self.keys_file):
            return
        
        with open(self.keys_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            keys = [row for row in reader if row[0] != name]
        
        with open(self.keys_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['encryption_name', 'public_key', 'private_key'])
            writer.writerows(keys)

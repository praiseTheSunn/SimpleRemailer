import importlib
import base64, json, csv, sys, os
from AsymmetricEncryption import AsymmetricEncryption 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "Utils")) 
from APICaller import APICaller 



module = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, module)
from logging_config import logger

config_file = os.path.join(os.path.dirname(__file__), "..", "..", "Storage", "config.json")
with open(config_file, 'r') as file:
    data = json.load(file)
ID = data["id"]


class AlgorithmLoader:
    def __init__(self, algorithm_directory):
        self.algorithm_directory = algorithm_directory
        self.algorithms = {}
        self.keys_file = os.path.join(os.path.dirname(__file__), "..", "..", "Storage", "keys.csv")
        self.config_file = os.path.join(os.path.dirname(__file__), "..", "..", "Storage", "config.json")

        with open(self.config_file, 'r') as file:
            data = json.load(file)

        self.api_caller = APICaller(base_url=data["database_ip"])
        self.password = data["password"]
        self.id = data["id"]
        self.ip = data["ip"]

        self._ensure_storage_directory_exists()
        self.load_algorithms()

    def _ensure_storage_directory_exists(self):
        # Ensure the storage directory exists
        storage_dir = os.path.dirname(self.keys_file)
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def load_algorithms(self):
        # print("Loading algorithms")
        sys.path.insert(0, self.algorithm_directory)
        
        if not os.path.exists(self.keys_file):
            with open(self.keys_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['encryption_name', 'public_key', 'private_key'])
        
        with open(self.keys_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            keys = {rows[0]: (rows[1], rows[2]) for rows in reader}
        
        # print(keys)

        # List of current algorithms in the directory
        current_algorithms = set()

        for filename in os.listdir(self.algorithm_directory):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                current_algorithms.add(module_name)
                module = importlib.import_module(module_name)
                importlib.reload(module)  # Ensure module is reloaded
                for attr in dir(module):
                    cls = getattr(module, attr)
                    if isinstance(cls, type) and issubclass(cls, AsymmetricEncryption) and cls is not AsymmetricEncryption:
                        self.add_algorithm(module_name, cls, keys)
        
        # Remove algorms that are in the keys file but not in the current directory
        for algorithm in list(keys.keys()):
            if algorithm not in current_algorithms:
                # print(algorithm)
                self.remove_algorithm(algorithm)
        
        sys.path.pop(0)

    def add_algorithm(self, module_name, cls, keys):

        # Add the algorithm to the dictionary
        self.algorithms[module_name] = cls()
        
        # Write to the keys file if the algorithm is not already in it
        if module_name not in keys:
            private_key_pem, public_key_pem = cls().generate_keys()
            public_key_b64 = base64.b64encode(public_key_pem).decode('utf-8')
            private_key_b64 = base64.b64encode(private_key_pem).decode('utf-8')
            with open(self.keys_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([module_name, public_key_b64, private_key_b64])

            

            data = {
                "id": self.id,
                "ip": self.ip,
                "encryption": module_name,
                "public_key": public_key_b64,
                "password": self.password,
            }

            print(data)
            logger.info(f"MIX_NODE{ID}: Generate aymmetric key")

            self.api_caller.post("encryption/update_encryption", data)    

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

        # Send api to remove this encryption in database server
        data = {
            "id": self.id,
            "ip": self.ip,  
            "encryption": name,
            "password": self.password,
        }

        self.api_caller.post("encryption/remove_encryption/", data)

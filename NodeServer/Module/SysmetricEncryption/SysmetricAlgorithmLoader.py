import importlib
import base64, json, csv, sys, os
from SymmetricEncryption import SymmetricEncryption 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "Utils")) 
from APICaller import APICaller 

class SysmetricAlgorithmLoader:
    def __init__(self, algorithm_directory):
        self.algorithm_directory = algorithm_directory
        self.algorithms = {}
        
        self.config_file = os.path.join(os.path.dirname(__file__), "..", "..", "Storage", "config.json")

        with open(self.config_file, 'r') as file:
            data = json.load(file)

        self.api_caller = APICaller(base_url=data["database_ip"])
        self.id = data["id"]
        self.ip = data["ip"]
        self.load_algorithms()

    def load_algorithms(self):
        print("Loading algorithms")
        sys.path.insert(0, self.algorithm_directory)
        
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
                    if isinstance(cls, type) and issubclass(cls, SymmetricEncryption) and cls is not SymmetricEncryption:
                        self.add_algorithm(module_name, cls)
        
        # Remove algorms that are in the keys file but not in the current directory
        # for algorithm in list(keys.keys()):
        #     if algorithm not in current_algorithms:
        #         # print(algorithm)
        #         self.remove_algorithm(algorithm)
        
        sys.path.pop(0)

    def add_algorithm(self, module_name, cls):
        # Add the algorithm to the dictionary
        self.algorithms[module_name] = cls()
        
            # data = {
            #     "id": self.id,
            #     "ip": self.ip,
            #     "encryption": module_name,
            #     "public_key": public_key_b64,
            # }

            # self.api_caller.post("encryption/update_encryption", data)    

    def get_algorithm(self, name):
        return self.algorithms.get(name)

    def remove_algorithm(self, name):
        if name in self.algorithms:
            del self.algorithms[name]
        
        # Send api to remove this encryption in database server
        # data = {
        #     "id": self.id,
        #     "ip": self.ip,  
        #     "encryption": name
        # }

        # self.api_caller.post("encryption/remove_encryption/", data)

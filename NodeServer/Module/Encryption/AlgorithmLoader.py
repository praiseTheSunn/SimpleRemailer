# dynamic_loader.py
import importlib
import os
import sys
from AsymmetricEncryption import AsymmetricEncryption  # Import AsymmetricEncryption

class AlgorithmLoader:
    def __init__(self, algorithm_directory):
        self.algorithm_directory = algorithm_directory
        self.algorithms = {}
        self.load_algorithms()

    def load_algorithms(self):
        self.algorithms.clear()
        sys.path


class AlgorithmLoader:
    def __init__(self, algorithm_directory):
        self.algorithm_directory = algorithm_directory
        self.algorithms = {}
        self.load_algorithms()

    def load_algorithms(self):
        self.algorithms.clear()
        sys.path.insert(0, self.algorithm_directory)
        for filename in os.listdir(self.algorithm_directory):
            # print(filename)
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                module = importlib.import_module(module_name)
                # print(module_name)
                importlib.reload(module)  # Ensure module is reloaded
                for attr in dir(module):
                    cls = getattr(module, attr)
                    if isinstance(cls, type) and issubclass(cls, AsymmetricEncryption) and cls is not AsymmetricEncryption:
                        self.algorithms[module_name] = cls()
        # print(self.algorithms)
        sys.path.pop(0)

    def get_algorithm(self, name):
        return self.algorithms.get(name)

    def remove_algorithm(self, name):
        if name in self.algorithms:
            del self.algorithms[name]

from abc import ABC, abstractmethod
import random


class PathStrategy(ABC):
    def __init__(self, nodes):
        self.nodes = nodes

    @abstractmethod
    def generate_path(self, path_length):
        pass


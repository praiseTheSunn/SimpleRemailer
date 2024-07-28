from abc import ABC, abstractmethod
import random


class PathStrategy(ABC):
    def __init__(self, all_nodes):
        self.all_nodes = all_nodes

    @abstractmethod
    def get_path(self, nodes_list, path_str):
        pass


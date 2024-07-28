from PathStrategy import *


class RandomPathStrategy(PathStrategy):
    def get_path(self, path_length):
        if len(self.all_nodes) < path_length:
            raise ValueError("Not enough nodes to form the path")
        return random.sample(self.all_nodes, path_length)



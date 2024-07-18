from PathStrategy import *


class RandomPathStrategy(PathStrategy):
    def generate_path(self, path_length):
        if len(self.nodes) < path_length:
            raise ValueError("Not enough nodes to form the path")
        return random.sample(self.nodes, path_length)



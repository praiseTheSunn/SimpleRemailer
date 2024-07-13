from PathStrategy import *


class HighSecurityPathStrategy(PathStrategy):
    def generate_path(self, path_length):
        secure_nodes = [node for node in self.nodes if 'secure' in node.get('tags', [])]
        if len(secure_nodes) < path_length:
            raise ValueError("Not enough secure nodes to form the path")
        return random.sample(secure_nodes, path_length)
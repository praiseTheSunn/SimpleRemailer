from PathStrategy import *


class LowestLatencyPathStrategy(PathStrategy):
    def generate_path(self, path_length):
        if len(self.nodes) < path_length:
            raise ValueError("Not enough nodes to form the path")
        sorted_nodes = sorted(self.nodes, key=lambda x: x.get('latency', float('inf')))
        return sorted_nodes[:path_length]
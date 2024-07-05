from abc import ABC, abstractmethod
from typing import List

# Define the strategy interface
class PathStrategy(ABC):
    @abstractmethod
    def determine_path(self) -> List[str]:
        pass

# Implement specific strategies
class FullPathStrategy(PathStrategy):
    def determine_path(self) -> List[str]:
        # Placeholder logic for determining the full path
        return ["start", "node1", "node2", "end"]

class PartialPathStrategy(PathStrategy):
    def __init__(self, i: int):
        self.i = i

    def determine_path(self) -> List[str]:
        # Placeholder logic for determining the path up to node i
        return ["start"] + [f"node{n}" for n in range(1, self.i + 1)]

# PathDeterminator class using the strategy pattern
class PathDeterminator:
    def __init__(self, strategy: PathStrategy):
        self.strategy = strategy

    def determine_path(self) -> List[str]:
        return self.strategy.determine_path()
    
    def set_strategy(self, strategy: PathStrategy):
        self._strategy = strategy

# Usage example
if __name__ == "__main__":
    # Use FullPathStrategy
    full_path_determinator = PathDeterminator(FullPathStrategy())
    print(full_path_determinator.determine_path())  # Output: ['start', 'node1', 'node2', 'end']

    # Use PartialPathStrategy
    partial_path_determinator = PathDeterminator(PartialPathStrategy(2))
    print(partial_path_determinator.determine_path())  # Output: ['start', 'node1', 'node2']

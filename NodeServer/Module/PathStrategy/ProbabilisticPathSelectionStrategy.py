from PathStrategy import *


class ProbabilisticPathGenerationStrategy(PathStrategy):

    def generate_path(self, new_path_percentage=25):
        path_length = random.randint(2, min(len(self.all_nodes), 5))
        bool_array = random.choices([True, False], weights=[new_path_percentage, 100-new_path_percentage], k=path_length)
        return random.sample(self.all_nodes, path_length), bool_array

    def get_path(self, path_flag):
        self.update_list_nodes()
        new_node, new_path = [], []
        if path_flag:
            new_node, new_path = self.generate_path()

        return new_node, new_path


# for testing
if __name__ == '__main__':
    all_nodes = ['Node1', 'Node2', 'Node3', 'Node4', 'Node5', 'Node6', 'Node7']
    cur_nodes = ['Node1', 'Node2', 'Node3', 'Node4']
    path_str = "1000"

    path_generator = ProbabilisticPathGenerationStrategy(all_nodes)
    # new_path, path_string = path_generator.generate_path(new_path_percentage=10)
    # print("Generated Path:", new_path)
    # print("Path String:", path_string)

    #---

    new_nodes_list, new_path_str = path_generator.get_path(cur_nodes, path_str)
    print(new_nodes_list)
    print(new_path_str)
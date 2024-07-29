from PathStrategy import *


class CentralizedPathGenerationStrategy(PathStrategy):
    def generate_path(self):
        path_length = random.randint(1, 5)
        array = [0] * path_length
        string_array = ''.join(str(num) for num in array)
        return random.sample(self.all_nodes, path_length), string_array

    def get_path(self, cur_nodes_list, path_str):
        if path_str[0] == "1":
            new_node, new_path = self.generate_path()

            # push front cur nodes
            cur_nodes_list.pop(0)
            cur_nodes_list = new_node + cur_nodes_list

            # push_front path str
            path_str = new_path + path_str[1:]

        elif path_str[0] == "0":
            path_str = path_str[1:]
            cur_nodes_list.pop(0)

        return cur_nodes_list, path_str


# for testing
if __name__ == '__main__':
    all_nodes = ['Node1', 'Node2', 'Node3', 'Node4', 'Node5', 'Node6', 'Node7']
    cur_nodes = ['Node1', 'Node2', 'Node3', 'Node4']
    path_str = "1000"

    path_generator = ProbabilisticPathSelectionStrategy(all_nodes)
    # new_path, path_string = path_generator.generate_path(new_path_percentage=10)
    # print("Generated Path:", new_path)
    # print("Path String:", path_string)

    #---

    new_nodes_list, new_path_str = path_generator.get_path(cur_nodes, path_str)
    print(new_nodes_list)
    print(new_path_str)
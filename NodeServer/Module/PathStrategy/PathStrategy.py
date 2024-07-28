from abc import ABC, abstractmethod
import random
import requests

class PathStrategy(ABC):
    def __init__(self, all_nodes):
        self.all_nodes = all_nodes

    def get_list_nodes(self):
        url = 'http://127.0.0.1:8000/get_list_node'
        data = {
            'id': '001',
            'password': '1'
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            nodes = response.json()
            print("Nodes list:")
            for node in nodes:
                print(node)
        else:
            print(f"Failed with status code: {response.status_code}")
            print(f"Error message: {response.text}")

    @abstractmethod
    def get_path(self, nodes_list, path_str):
        pass


if __name__ == '__main__':
    url = url = 'http://127.0.0.1:8000/node/get_list_node'
    data = {
        'id': '001',
        'password': '1'
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        nodes = response.json()
        print("Nodes list:")
        for node in nodes:
            print(node)
    else:
        print(f"Failed with status code: {response.status_code}")
        print(f"Error message: {response.text}")



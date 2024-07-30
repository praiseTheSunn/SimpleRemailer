from abc import ABC, abstractmethod
import random
import requests
import json

class PathStrategy(ABC):
    def __init__(self):
        self.all_nodes = []

    def update_list_nodes(self):
        url = 'http://127.0.0.1:8000/node/get_list_node'
        data = {
            'id': '001',
            'password': '1'
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            nodes = response.json()
            print("Nodes list:")
            self.all_nodes = [node for node in nodes if len(node['asymmetric_encryptions']) > 0 and
                     len(node['symmetric_encryptions']) > 0]
            # for node in self.all_nodes:
            #     print(node)
        else:
            print(f"Failed with status code: {response.status_code}")
            print(f"Error message: {response.text}")



    # @abstractmethod
    def get_path(self, encrypted_nodes, path_str):
        pass


if __name__ == '__main__':
    # url = url = 'http://127.0.0.1:8000/node/get_list_node'
    # data = {
    #     'id': '001',
    #     'password': '1'
    # }
    # response = requests.post(url, json=data)
    # if response.status_code == 200:
    #     nodes = response.json()
    #     print("Nodes list:")
    #     nodes = [node for node in nodes if len(node['asymmetric_encryptions']) > 0 and
    #      len(node['symmetric_encryptions']) > 0]
    #     for node in nodes:
    #         print(node)
    # else:
    #     print(f"Failed with status code: {response.status_code}")
    #     print(f"Error message: {response.text}")

    a = PathStrategy()
    a.update_list_nodes()



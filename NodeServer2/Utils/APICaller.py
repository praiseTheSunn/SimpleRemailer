import requests
import json

class APICaller:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json(), response.status_code

    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url)
        return response.json(), response.status_code

    def put(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        response = requests.put(url, headers=headers, data=json.dumps(data))
        return response.json(), response.status_code

    def delete(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(url, headers=headers, data=json.dumps(data))
        return response.json(), response.status_code

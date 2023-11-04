import requests
import json

class Magpai:
    def __init__(self, api_key):
        self.api_key = api_key

    def run(self, workflow_id, inputs):
        url = "https://magpai.app/api/v1/workflow/run"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.api_key}"
        }
        data = {
            "workflowId": workflow_id,
            "inputs": inputs
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_json = response.json()

        return response_json



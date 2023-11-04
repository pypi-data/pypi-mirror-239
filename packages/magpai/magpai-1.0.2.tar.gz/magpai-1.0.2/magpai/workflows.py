import requests
import json

def RunWorkflow(apiKey, workflowId, inputs):

    url = "https://magpai.app/api/v1/workflow/run"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {apiKey}"
    }
    data = {
        "workflowId": workflowId,
        "inputs": inputs
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    
    return response_json
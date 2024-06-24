import requests
import json

url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}

def send_request(final_prompt):
    data = {
        "model": "projai",
        "prompt": final_prompt,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

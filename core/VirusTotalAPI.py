import os

import requests
import os

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv('API_URL')

print(API_URL)

def Upload_file(file):
    with open(file, 'rb') as f:
        files = {"file": file}
        response = requests.post(f"{API_URL}/files",files=files, headers={"x-apikey": f"{API_KEY}"})
        json = response.json().get('data')
        if response.status_code == 200:
            id = json.get('id')
            return {"message": "success", "id": f"{id}"}
        return {"message": "error"}

def Get_File_Info(id : str):
    response = requests.get(url=f"{API_URL}/files/{id}", headers={"x-apikey": f"{API_KEY}"})
    return response.json()
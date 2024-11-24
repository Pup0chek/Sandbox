import requests

API_KEY = "244b0f6ee69d1669c9c21135a08da07243d3003790c28b264d52967e01f0f1d9"
API_URL = "https://www.virustotal.com/api/v3"


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
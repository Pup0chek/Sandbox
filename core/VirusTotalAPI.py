import os

import requests
import os

# API_KEY = os.getenv("API_KEY")
# API_URL = os.getenv('API_URL')

API_KEY = '244b0f6ee69d1669c9c21135a08da07243d3003790c28b264d52967e01f0f1d9'
API_URL = ' https://www.virustotal.com/api/v3'
headers = {"X-Apikey": API_KEY}

def Upload_file(file_path):
    print(file_path[4:])
    with open(file_path, 'rb') as file:
        files = {"file": file}  # Открытый файл передается напрямую

        response = requests.post(f"{API_URL}/files", files=files, headers=headers)
        if response.status_code == 200:
            # Извлекаем ID файла из JSON-ответа

            response_json = response.json()
            file_id = response_json.get('data', {}).get('id')
            #print(create_report(file_path, response_json))
            return {"message": "success", "id": file_id}
        else:
            # Возвращаем ошибку с кодом и текстом
            return {
                "message": "error",
                "status_code": response.status_code,
                "error_details": response.text
            }

def Get_File_Info(id : str):
    response = requests.get(url=f"{API_URL}/files/{id}", headers={"x-apikey": f"{API_KEY}"})
    return response.json()

def Check_url(url:str):
    payload = {"url": url}
    response = requests.post(f"{API_URL}/urls", headers=headers, data=payload)
    return response.json()

def Get_URL_Info(id: str):
    response = requests.get(url=f"{API_URL}/urls/{id}", headers=headers)
    return response.json()

def create_report(file_path, response_json):
    path = file_path[4:].split('.')[0] + ".txt"
    print(response_json)
    with open(f'reports\\{path}', 'wb') as fi:
        fi.write(response_json)
        fi.close()
    return True

#print(Get_File_Info("d03cd054cf4c9f3ef860f5d7f2a0ebc4"))
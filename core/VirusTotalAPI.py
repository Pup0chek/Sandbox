import os

import requests
import os

# API_KEY = os.getenv("API_KEY")
# API_URL = os.getenv('API_URL')

API_KEY = '244b0f6ee69d1669c9c21135a08da07243d3003790c28b264d52967e01f0f1d9'
API_URL = ' https://www.virustotal.com/api/v3'

def Upload_file(file_path):
    with open(file_path, 'rb') as file:
        files = {"file": file}  # Открытый файл передается напрямую
        headers = {"X-Apikey": API_KEY}
        response = requests.post(f"{API_URL}/files", files=files, headers=headers)

        if response.status_code == 200:
            # Извлекаем ID файла из JSON-ответа
            response_json = response.json()
            file_id = response_json.get('data', {}).get('id')
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

#print(Upload_file("C:\\Users\\User\\Downloads\\Итоговое задание.pdf"))
#print(Get_File_Info("d03cd054cf4c9f3ef860f5d7f2a0ebc4"))
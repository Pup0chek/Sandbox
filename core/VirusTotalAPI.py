import requests

# API credentials
API_KEY = "244b0f6ee69d1669c9c21135a08da07243d3003790c28b264d52967e01f0f1d9"
API_URL = "https://www.virustotal.com/api/v3"  # Fixed URL formatting
headers = {"X-Apikey": API_KEY}


def Upload_file(file_path):
    print(f"Uploading file from path: {file_path}")
    with open(file_path, "rb") as file:
        files = {"file": file}  # Open file passed directly

        response = requests.post(f"{API_URL}/files", files=files, headers=headers)
        if response.status_code == 200:
            # Extract file ID from the JSON response
            response_json = response.json()
            file_id = response_json.get("data", {}).get("id")
            return {"message": "success", "id": file_id}
        else:
            # Return error details with status code
            return {"message": "error", "status_code": response.status_code, "error_details": response.text}


def Get_File_Info(file_id: str):
    response = requests.get(f"{API_URL}/files/{file_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"message": "error", "status_code": response.status_code, "error_details": response.text}


def Check_url(url: str):
    payload = {"url": url}
    response = requests.post(f"{API_URL}/urls", headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"message": "error", "status_code": response.status_code, "error_details": response.text}


def Get_URL_Info(id: str):
    response = requests.get(f"{API_URL}/urls/{id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"message": "error", "status_code": response.status_code, "error_details": response.text}


def create_report(file_path, response_json):
    # Cleaned file name creation logic
    path = file_path.split(".")[0] + ".txt"
    print("Saving report:", path)
    with open(f"reports/{path}", "w") as report_file:
        report_file.write(str(response_json))  # Save the JSON response as text
    return True

import base64
import pytest
from flask import session
from app import create_app  # Предполагается, что это функция для создания приложения
from core.VirusTotalAPI import Upload_file, Get_File_Info

@pytest.fixture
def client():
    app, _ = create_app()
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret"
    with app.test_client() as client:
        yield client

# Мокаем API-функции для изоляции тестов
def mock_upload_file(path):
    return {"id": base64.b64encode(b"test_id:test").decode('utf-8'), "message": "success"}

def mock_get_file_info(file_id):
    return {"data": {"id": file_id, "attributes": {"type_extension": "txt", "size": "1024", "reputation": "good"}}}

# Тест маршрута /file_info/ (GET)
def test_file_info_get(client, monkeypatch):
    monkeypatch.setattr("core.VirusTotalAPI.Get_File_Info", mock_get_file_info)
    response = client.get("/file_info/")
    assert response.status_code == 200
    assert b'type_extension' in response.data

# Тест маршрута /file_info/ (POST)
def test_file_info_post(client, monkeypatch):
    monkeypatch.setattr("core.VirusTotalAPI.Upload_file", mock_upload_file)
    monkeypatch.setattr("core.VirusTotalAPI.Get_File_Info", mock_get_file_info)

    response = client.post("/file_info/")
    assert response.status_code == 200
    assert b'txt' in response.data

# Тест маршрута /upload/ без авторизации
def test_upload_without_session(client):
    response = client.get("/upload/")
    assert response.status_code == 302  # Редирект на страницу авторизации

# Тест маршрута /upload/ с авторизацией и без файла
def test_upload_no_file(client):
    with client.session_transaction() as sess:
        sess["access_token"] = "test_token"

    response = client.post("/upload/", data={})
    assert response.status_code == 200
    assert 'Файл не выбран!' in response.data.decode('utf-8')

# Тест маршрута /upload/ с авторизацией и большим файлом
def test_upload_large_file(client):
    with client.session_transaction() as sess:
        sess["access_token"] = "test_token"

    large_file = b"x" * (1024 * 1024 + 2)  # Файл больше 1 МБ
    data = {
        "file": (large_file, "large_file.txt")
    }

    response = client.post("/upload/", data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'Размер файла превышает 1 МБ!' in response.data.decode('utf-8')

# Тест успешной загрузки файла
def test_upload_success(client, monkeypatch):
    monkeypatch.setattr("core.VirusTotalAPI.Upload_file", mock_upload_file)
    monkeypatch.setattr("core.VirusTotalAPI.Get_File_Info", mock_get_file_info)

    with client.session_transaction() as sess:
        sess["access_token"] = "test_token"

    small_file = b"test content"
    data = {
        "file": (small_file, "test_file.txt")
    }

    response = client.post("/upload/", data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'Файл успешно загружен!' in response.data.decode('utf-8')

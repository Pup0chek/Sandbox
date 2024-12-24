from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import base64
from flask import Flask, request, render_template, redirect, url_for, session, flash
from core.VirusTotalAPI import Upload_file, Get_File_Info
from wtf.forms import MessageForm
import os
from blueprints.auth import auth

file = Blueprint('file', __name__, template_folder='templates')

MAX_FILE_SIZE = 1024 * 1024 + 1

@file.route('/file_info/', methods=['get', 'post'])
def file_info(path:str='C:\\Sandbox\\test.txt'):
    if request.method == 'POST':
        id = Upload_file(path).get("id")
        decoded = base64.b64decode(id).decode('utf-8')
        print(decoded)
        splited = decoded.split(":")
        message = [Get_File_Info(splited[0]), "True"]
        return render_template('file_info.html', message=message)
    elif request.method == 'GET':
        message = [{'data':{'id': ' ', 'attributes': {'type_extension':' ', 'size':' ', 'reputation':' '}}}, "True"]
        return render_template('file_info.html', message=message)

@file.route('/upload/', methods=['POST', 'GET'])
def upload():
    # Проверяем, авторизован ли пользователь
    if "username" not in session:
        flash("Вы должны авторизоваться или зарегистрироваться, чтобы загрузить файл.", "warning")
        return redirect(url_for("auth.login"))

    message = {"method": "GET"}

    if request.method == "POST":
        file = request.files.get("file")

        if not file or not file.filename:
            message["error"] = "Файл не выбран!"
            flash("Файл не выбран!", "danger")
            return render_template("upload.html", message=message)

        # Проверяем размер файла
        file_bytes = file.read(MAX_FILE_SIZE + 1)
        if len(file_bytes) > MAX_FILE_SIZE:
            message["file_size_error"] = True
            flash("Размер файла превышает 1 МБ!", "danger")
            return render_template("upload.html", message=message)

        # Сохраняем файл временно
        temp_path = f"tmp\\{file.filename}"
        with open(temp_path, 'wb') as temp_file:
            temp_file.write(file_bytes)

        # Загружаем файл на API
        try:
            api_response = Upload_file(temp_path)
            if api_response.get("message") == "success":
                id = api_response.get("id")
                decoded = base64.b64decode(id).decode('utf-8')
                splited = decoded.split(":")
                message = [Get_File_Info(splited[0]), "True"]

                flash("Файл успешно загружен!", "success")
                return render_template('file_info.html', message=message)
            else:
                message["error"] = "Ошибка загрузки на API"
                flash("Ошибка загрузки на API.", "danger")
        except Exception as e:
            message["error"] = f"Произошла ошибка: {e}"
            flash(f"Произошла ошибка: {e}", "danger")

    return render_template("upload.html", message=message)
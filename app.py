import base64
from flask import Flask, request, render_template, redirect, url_for, session, flash
from db.connection import get_db_connection
from core.VirusTotalAPI import Upload_file, Get_File_Info
from wtf.forms import MessageForm
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
# app.config.from_object(config)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or os.urandom(24)

MAX_FILE_SIZE = 1024 * 1024 + 1



#функция представления
@app.route('/file_info/', methods=['get', 'post'])
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

@app.route('/lol/', methods=["GET", "POST"])
def lol():
    form = MessageForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        print("---------------")
        print(name)
        print(email)
        print(message)
        print("---------------")
        return redirect(url_for('lol'))
    return render_template('message.html', form=form)

users = {"admin": "password123"}
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["username"] = username
            flash("Вы успешно вошли!", "success")
            return redirect(url_for("upload"))
        else:
            flash("Неправильное имя пользователя или пароль.", "danger")
    return render_template("login.html")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    message = {"method": "GET"}

    if request.method == "POST":
        file = request.files.get("file")

        if not file or not file.filename:
            message["error"] = "Файл не выбран!"
            return render_template("upload.html", message=message)

        # Читаем файл
        file_bytes = file.read(MAX_FILE_SIZE + 1)
        if len(file_bytes) > MAX_FILE_SIZE:
            message["file_size_error"] = True
            return render_template("upload.html", message=message)

        # Сохраняем файл во временное хранилище (например, на сервер)
        temp_path = f"C:\\Sandbox\\tmp\\{file.filename}"
        with open(temp_path, 'wb') as temp_file:
            temp_file.write(file_bytes)

        # Загружаем файл на API
        try:
            api_response = Upload_file(temp_path)
            if api_response.get("message") == "success":
                message = {
                    "method": "POST",
                    "file_info": api_response.get("id"),
                }
                id = api_response.get("id")
                decoded = base64.b64decode(id).decode('utf-8')
                print(decoded)
                splited = decoded.split(":")
                message = [Get_File_Info(splited[0]), "True"]
                return render_template('file_info.html', message=message)
            else:
                message["error"] = "Ошибка загрузки на API"
        except Exception as e:
            message["error"] = f"Произошла ошибка: {e}"

        return render_template('file_info.html', message=message)
    return render_template("upload.html", message=message)

@app.route('/new/')
def render_new():
    return render_template('new.html')

# @app.route('/<int:num>/')
# def lol(num: int):
#     return {"message": f"{num*2}"}



app.run(debug=True)



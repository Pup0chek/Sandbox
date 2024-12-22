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

@app.route('/')
def index():
    return render_template('index.html')

users = {'admin':'password'}
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


@app.route("/logout/")
def logout():
    session.pop("username", None)
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("index"))


@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if "username" not in session:
        flash("Вы должны авторизоваться, чтобы загрузить файл.", "warning")
        return redirect(url_for("login"))

    message = {"method": "GET"}
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            flash("Файл не выбран!", "danger")
            return render_template("upload.html", message=message)

        file_bytes = file.read(1024 * 1024 + 1)  # Ограничение 1 МБ
        if len(file_bytes) > 1024 * 1024:
            message["file_size_error"] = True
            flash("Размер файла превышает 1 МБ!", "danger")
            return render_template("upload.html", message=message)

        flash("Файл успешно загружен!", "success")
        # Здесь вы можете добавить логику отправки файла на VirusTotal
        return render_template("upload.html", message=message)

    return render_template("upload.html", message=message)


@app.route('/new/')
def render_new():
    return render_template('new.html')









app.run(debug=True)



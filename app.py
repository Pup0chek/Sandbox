import base64
from flask import Flask, request, render_template, redirect, url_for, session, flash
from db.connection import get_db_connection
from core.VirusTotalAPI import Upload_file, Get_File_Info
from wtf.forms import MessageForm
import os
from blueprints.auth import auth
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

app.register_blueprint(auth, url_prefix='/login')
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


@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    # Проверяем, авторизован ли пользователь
    if "username" not in session:
        flash("Вы должны авторизоваться или зарегистрироваться, чтобы загрузить файл.", "warning")
        return redirect(url_for("login"))

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
        temp_path = f"C:\\Sandbox\\tmp\\{file.filename}"
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















app.run(debug=True)



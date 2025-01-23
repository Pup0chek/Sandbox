from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import httpx

from app import db
from db.models import User

auth = Blueprint('auth', __name__, template_folder='templates')

users = {"admin": "password123"}





CLIENT_ID = "c360e751eb9e49c298f213d8e011fef3"
CLIENT_SECRET = "51622c62188e4b9aabdd74743c610a82"
REDIRECT_URI = "http://127.0.0.1:5000/login/callback"
YANDEX_AUTH_URL = "https://oauth.yandex.ru/authorize"
YANDEX_TOKEN_URL = "https://oauth.yandex.ru/token"

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["username"] = username
            #flash("Вы успешно вошли!", "success")
            return redirect("/")
        else:
            flash("Неправильное имя пользователя или пароль.", "danger")
    return render_template("login.html")

@auth.route("/logout/")
def logout():
    # Удаляем все ключи из сессии
    session.clear()  # Очистка всей сессии

    #flash("Вы вышли из системы.", "info")
    return redirect(url_for("index"))

@auth.route("/auth/")
def authe():
    # URL для редиректа пользователя на страницу авторизации Яндекса
    auth_url = (
        f"{YANDEX_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)  # Используем redirect вместо RedirectResponse

def get_user_info(access_token):
    url = 'https://login.yandex.ru/info'
    headers = {
        'Authorization': f'OAuth {access_token}'  # OAuth-токен в заголовке
    }
    params = {
        'format': 'json',  # Формат ответа (по умолчанию json)
    }

    # Отправляем GET-запрос
    response = httpx.get(url, headers=headers, params=params)
    print(response.json())

    if response.status_code == 200:
        return response.json()  # Возвращаем данные о пользователе
    else:
        return None

@auth.route("/callback/")
def callback():
    code = request.args.get("code")
    if not code:
        #flash("Не удалось получить код авторизации.", "danger")
        return redirect(url_for("auth.login"))

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }

    try:
        with httpx.Client() as client:
            response = client.post(YANDEX_TOKEN_URL, data=token_data)
            response.raise_for_status()
            token_response = response.json()
    except httpx.HTTPStatusError as e:
        #flash("Ошибка при получении токена.", "danger")
        return redirect(url_for("auth.login"))

    session['access_token'] = token_response.get('access_token')

    # Получаем информацию о пользователе
    user_info = get_user_info(session['access_token'])

    # Формируем URL для аватарки
    avatar_url = f"https://avatars.yandex.net/get-yapic/{user_info['default_avatar_id']}/islands-small"

    # Сохраняем данные в сессии
    session['user_info'] = user_info
    session['avatar_url'] = avatar_url

    flash("Вы успешно авторизовались через Яндекс!", "success")
    return redirect(url_for("index"))




@auth.route("/register/", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password == confirm_password:
            user = User.query.filter_by(username=username).first()
            if user:
                flash("Пользователь с таким именем уже существует!", "danger")
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                session["username"] = username
                flash("Вы успешно зарегистрировались!", "success")
                return redirect("/")
        else:
            flash("Пароли не совпадают!", "danger")

    return render_template("register.html")


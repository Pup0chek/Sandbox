from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import httpx

auth = Blueprint('auth', __name__, template_folder='templates')

users = {"admin": "password123"}

CLIENT_ID = "c360e751eb9e49c298f213d8e011fef3"
CLIENT_SECRET = "51622c62188e4b9aabdd74743c610a82"
REDIRECT_URI = "http://127.0.0.1:5000/"
YANDEX_AUTH_URL = "https://oauth.yandex.ru/authorize"
YANDEX_TOKEN_URL = "https://oauth.yandex.ru/token"

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["username"] = username
            flash("Вы успешно вошли!", "success")
            return redirect("/")
        else:
            flash("Неправильное имя пользователя или пароль.", "danger")
    return render_template("login.html")

@auth.route("/logout/")
def logout():
    session.pop("username", None)
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("index"))

@auth.route("/auth/")
def authe():
    # URL для редиректа пользователя на страницу авторизации Яндекса
    auth_url = (
        f"{YANDEX_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)  # Используем redirect вместо RedirectResponse

@auth.route("/callback/")
def callback():
    code = request.args.get("code")
    if not code:
        flash("Не удалось получить код авторизации.", "danger")
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
        flash("Ошибка при получении токена.", "danger")
        return redirect(url_for("auth.login"))

    flash("Вы успешно авторизовались через Яндекс!", "success")
    return token_response  # Можно вернуть данные или перенаправить

@auth.route("/register/", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if username not in users:
            if password == confirm_password:
                users[username] = password
                session["username"] = username
                flash("Вы успешно зарегистрировались!", "success")
                return redirect("/")
            else:
                flash("Пароли не совпадают!", "danger")
        else:
            flash("Пользователь с таким именем уже существует!", "danger")

    return render_template("register.html")

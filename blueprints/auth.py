import httpx
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

auth = Blueprint("auth", __name__, template_folder="templates")

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
            return redirect("/")
        else:
            flash("Неправильное имя пользователя или пароль.", "danger")
    return render_template("login.html")


@auth.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("index"))


@auth.route("/auth/")
def authe():
    auth_url = f"{YANDEX_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(auth_url)


def get_user_info(access_token):
    url = "https://login.yandex.ru/info"
    headers = {"Authorization": f"OAuth {access_token}"}
    params = {
        "format": "json",
    }
    response = httpx.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@auth.route("/callback/")
def callback():
    code = request.args.get("code")
    if not code:
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
    except httpx.HTTPStatusError:
        return redirect(url_for("auth.login"))

    session["access_token"] = token_response.get("access_token")
    user_info = get_user_info(session["access_token"])
    avatar_url = f"https://avatars.yandex.net/get-yapic/{user_info['default_avatar_id']}/islands-small"
    session["user_info"] = user_info
    session["avatar_url"] = avatar_url

    flash("Вы успешно авторизовались через Яндекс!", "success")
    return redirect(url_for("index"))

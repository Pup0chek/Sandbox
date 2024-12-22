from flask import Blueprint, render_template, request, redirect, url_for, flash, session


auth = Blueprint('auth', __name__, template_folder='templates')

users = {"admin": "password123"}

@auth.route("/", methods=["GET", "POST"])
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

@auth.route("/logout/")
def logout():
    session.pop("username", None)
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("index"))
from flask import Blueprint, render_template, request, redirect, url_for, flash, session


auth = Blueprint('auth', __name__, template_folder='templates')

users = {"admin": "password123"}

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(users)
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

@auth.route("/register/", methods = ['post', 'get'])
def register():
    if request.method == "POST":
        print(users)
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if username not in users:
            users[username] = password
            session["username"] = username
            if confirm_password == password:
                    flash("Вы успешно зарегистрировались!", "success")
                    return redirect("/")
            else:
                flash("Пароли не сходятся!", "danger")
        else:
            flash("Пользователь с таким именем уже есть!", "danger")


    return render_template("register.html")
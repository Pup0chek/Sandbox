from celery.bin.result import result
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from core.VirusTotalAPI import Check_url


url = Blueprint('url', __name__, template_folder='templates')

@url.route("/url_check/", methods=['post', "get"])
def url_check():
    if "username" not in session:
        flash("Вы должны авторизоваться или зарегистрироваться, чтобы загрузить файл.", "warning")
        return redirect(url_for("auth.login"))
    message = {
        "method": "GET",
        "body": " "
    }
    if request.method == "POST":
        message['method'] = "POST"
        result = Check_url(request.form.get("url"))
        message['body'] = result
        print(result)
        return render_template('URL.html', message=message)
    return render_template('URL.html', message=message)
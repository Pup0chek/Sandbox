from flask import Blueprint, render_template, request, redirect, url_for, session
from core.VirusTotalAPI import Check_url, Get_URL_Info


url = Blueprint('url', __name__, template_folder='templates')

@url.route("/url_check/", methods=['post', "get"])
def url_check():
    if "access_token" not in session:
        return redirect(url_for("auth.login"))

    message = {
        "method": "GET",
        "body": " "
    }
    if request.method == "POST":
        message['method'] = "POST"
        l = Check_url(request.form.get("url"))
        id = Check_url(request.form.get("url"))['data']['id']
        print(l)
        print(id)
        result = Get_URL_Info(id)
        print(result)
        message['body'] = result

        return render_template('URL.html', message=message)
    return render_template('URL.html', message=message)
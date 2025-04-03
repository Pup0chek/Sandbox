from flask import Blueprint, render_template, request

from core.bypass import Bypass

bypass = Blueprint("bypass", __name__, template_folder="templates")


@bypass.route("/url_bypass/", methods=["post", "get"])
def check_url():
    message = {"method": "GET", "body": " "}
    if request.method == "GET":
        return render_template("bypass.html", message=message)
    else:
        response = []
        bypass = Bypass(url=request.form.get("url"))
        response.append(bypass.methods_brute("POST"))
        response.append(bypass.methods_brute("GET"))
        response.append(bypass.methods_brute("PUT"))
        response.append(bypass.methods_brute("PATCH"))
        response.extend(bypass.headers_brute())
        message["method"] = "POST"
        message["body"] = response
        print(message)
        return render_template("bypass.html", message=message)

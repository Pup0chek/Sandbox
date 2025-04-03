import base64

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from core.VirusTotalAPI import Get_File_Info, Upload_file

file = Blueprint("file", __name__, template_folder="templates")

MAX_FILE_SIZE = 1024 * 1024 + 1  # Limit for file size (1 MB + 1 byte)


@file.route("/file_info/", methods=["GET", "POST"])
def file_info(path: str = "Sandbox\\test.txt"):
    if request.method == "POST":
        # Get the file upload ID and decode it
        id = Upload_file(path).get("id")
        decoded = base64.b64decode(id).decode("utf-8")
        print(decoded)
        splited = decoded.split(":")

        # Retrieve file information
        message = [Get_File_Info(splited[0]), "True"]
        return render_template("file_info.html", message=message)

    # If it's a GET request, provide an empty file info as a template
    elif request.method == "GET":
        message = [{"data": {"id": " ", "attributes": {"type_extension": " ", "size": " ", "reputation": " "}}}, "True"]
        return render_template("file_info.html", message=message)


@file.route("/upload/", methods=["POST", "GET"])
def upload():
    # Check if the user is logged in (access_token must be present in session)
    if "access_token" not in session:
        return redirect(url_for("auth.login"))

    message = {"method": "GET"}

    if request.method == "POST":
        # Get the file from the form
        file = request.files.get("file")

        # Check if the file is provided
        if not file or not file.filename:
            message["error"] = "Файл не выбран!"
            return render_template("upload.html", message=message)

        # Check the file size
        file_bytes = file.read(MAX_FILE_SIZE + 1)
        if len(file_bytes) > MAX_FILE_SIZE:
            message["file_size_error"] = True
            flash("Размер файла превышает 1 МБ!", "danger")
            return render_template("upload.html", message=message)

        # Save the file temporarily
        temp_path = f"tmp\\{file.filename}"
        with open(temp_path, "wb") as temp_file:
            temp_file.write(file_bytes)

        # Upload the file to the API
        try:
            api_response = Upload_file(temp_path)
            if api_response.get("message") == "success":
                id = api_response.get("id")
                decoded = base64.b64decode(id).decode("utf-8")
                splited = decoded.split(":")

                # Retrieve file info
                message = [Get_File_Info(splited[0]), "True"]
                flash("Файл успешно загружен!", "success")
                return render_template("file_info.html", message=message)
            else:
                message["error"] = "Ошибка загрузки на API"
                flash("Ошибка загрузки на API.", "danger")
        except Exception as e:
            message["error"] = f"Произошла ошибка: {e}"
            flash(f"Произошла ошибка: {e}", "danger")

    return render_template("upload.html", message=message)

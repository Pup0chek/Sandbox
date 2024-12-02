import base64

from flask import Flask, render_template
from core.VirusTotalAPI import Upload_file, Get_File_Info

app = Flask(__name__)


#функция представления
@app.route('/index/')
def index():
    id = Upload_file("C:\\Sandbox\\test.txt").get("id")
    decoded = base64.b64decode(id).decode('utf-8')
    print(decoded)
    splited = decoded.split(":")
    message = [Get_File_Info(splited[0]), "True"]
    return render_template('index.html', message=message)

@app.route('/new/')
def render_new():
    return render_template('new.html')

@app.route('/<int:num>/')
def lol(num: int):
    return {"message": f"{num*2}"}



app.run(debug=True)

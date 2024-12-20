import base64
from flask import Flask, render_template, request, redirect, url_for

import config
from core.VirusTotalAPI import Upload_file, Get_File_Info
from wtf.forms import MessageForm
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# app.config.from_object(config)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or os.urandom(24)


#функция представления
@app.route('/file_info/', methods=['get', 'post'])
def file_info(path:str='C:\\Sandbox\\test.txt'):
    if request.method == 'POST':
        id = Upload_file(path).get("id")
        decoded = base64.b64decode(id).decode('utf-8')
        print(decoded)
        splited = decoded.split(":")
        message = [Get_File_Info(splited[0]), "True"]
        return render_template('file_info.html', message=message)
    elif request.method == 'GET':
        message = [{'data':{'id': ' ', 'attributes': {'type_extension':' ', 'size':' ', 'reputation':' '}}}, "True"]
        return render_template('file_info.html', message=message)

@app.route('/lol/', methods=["GET", "POST"])
def lol():
    form = MessageForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        print("---------------")
        print(name)
        print(email)
        print(message)
        print("---------------")
        return redirect(url_for('lol'))
    return render_template('message.html', form=form)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new/')
def render_new():
    return render_template('new.html')

# @app.route('/<int:num>/')
# def lol(num: int):
#     return {"message": f"{num*2}"}



app.run(debug=True)



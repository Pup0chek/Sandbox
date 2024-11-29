from flask import Flask, render_template

app = Flask(__name__)


#функция представления
@app.route('/index')
def index():
    return {"message": "Hello!"}

@app.route('/<int:num>/')
def lol(num: int):
    return {"message": f"{num*2}"}

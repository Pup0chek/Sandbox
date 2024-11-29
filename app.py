from flask import Flask, render_template

app = Flask(__name__)


#функция представления
@app.route('/index/')
def index():
    return render_template('..\\index')

@app.route('/<int:num>/')
def lol(num: int):
    return {"message": f"{num*2}"}

app.run(debug=True)

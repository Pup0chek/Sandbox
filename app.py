from flask import Flask, render_template
from wtf.forms import MessageForm
from blueprints.auth import auth
from blueprints.file import file
from blueprints.url import url
from flask import redirect, url_for
# from dotenv import load_dotenv
# load_dotenv()


app = Flask(__name__)

app.register_blueprint(auth, url_prefix='/login')
app.register_blueprint(file, url_prefix='/file')
app.register_blueprint(url, url_prefix= '/url')
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or os.urandom(24)
app.config['SECRET_KEY'] = "123"







@app.route('/')
def index():
    return render_template('index.html')



@app.route('/reports', methods=['get'])
def get_report():
    return render_template('reports,html')


#функция представления
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



app.run(debug=True)



import httpx
from flask import Flask, render_template, request, session, flash
#from urllib3 import request

from wtf.forms import MessageForm
from blueprints.auth import auth
from blueprints.file import file
from blueprints.url import url
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#from aiokafka import AIOKafkaProducer
# from dotenv import load_dotenv
# load_dotenv()


#from confluent_kafka import Consumer

app = Flask(__name__)

# consumer_config = {
#     'bootstrap.servers': 'localhost:9092',
#     'group.id': '1',
#     'auto.offset.reset': 'earliest'
# }
# consumer = Consumer(consumer_config)
# Конфигурация для подключения к MySQL через SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_user:your_password@localhost/user_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем отслеживание изменений для экономии памяти


# # Инициализация SQLAlchemy
# db = SQLAlchemy(app)

app.register_blueprint(auth, url_prefix='/login')
app.register_blueprint(file, url_prefix='/file')
app.register_blueprint(url, url_prefix= '/url')
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or os.urandom(24)
app.config['SECRET_KEY'] = "123"


#
# @app.route('/consume/<topic>', methods=['GET'])
# def consume_messages(topic):
#     consumer.subscribe([topic])
#     messages = []
#     try:
#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 break
#             if msg.error():
#                 messages.append(f"Error: {msg.error()}")
#             else:
#                 messages.append(msg.value().decode('utf-8'))
#         return {"messages": messages}
#     except Exception as e:
#         return {"status": "Error", "details": str(e)}
#     finally:
#         consumer.close()



@app.route('/')
def index():
    user_info = session.get('user_info')
    avatar_url = session.get('avatar_url')

    if user_info:
        return render_template('index.html', user_info=user_info, avatar_url=avatar_url)

    #flash("Вы не авторизованы!", "danger")
    return redirect(url_for('auth.login'))


@app.route('/reports', methods=['get'])
def get_report():
    if "access_token" not in session:
        return redirect(url_for("auth.login"))

    return render_template('reports.html')


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



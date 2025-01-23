import httpx
from flask import Flask, render_template, request, session, flash
#from urllib3 import request

from wtf.forms import MessageForm
from blueprints.auth import auth
from blueprints.file import file
from blueprints.url import url
from flask import redirect, url_for
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
    access_token = session.get('access_token')
    refresh_token = session.get('refresh_token')

    if access_token:
        # Если токен доступен, можно запросить информацию о пользователе
        user_info = get_user_info(access_token)
        return render_template('index.html', user_info=user_info)

    flash("Вы не авторизованы!", "danger")
    return redirect(url_for('auth.login'))

def get_user_info(access_token):
    url = 'https://login.yandex.ru/info'
    headers = {
        'Authorization': f'OAuth {access_token}'  # OAuth-токен в заголовке
    }
    params = {
        'format': 'json',  # Формат ответа (по умолчанию json)
    }

    # Отправляем GET-запрос
    response = httpx.get(url, headers=headers, params=params)
    print(response.json())

    if response.status_code == 200:
        return response.json()  # Возвращаем данные о пользователе
    else:
        return None

@app.route('/reports', methods=['get'])
def get_report():
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



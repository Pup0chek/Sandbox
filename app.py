from flask import Flask, render_template, request, session, flash
#from urllib3 import request
from flask_socketio import SocketIO, send
from wtf.forms import MessageForm
from blueprints.auth import auth
from blueprints.file import file
from blueprints.url import url
from flask import redirect, url_for
from dsk.api import DeepSeekAPI
from flask_sqlalchemy import SQLAlchemy
#from aiokafka import AIOKafkaProducer
# from dotenv import load_dotenv
# load_dotenv()


#from confluent_kafka import Consumer

app = Flask(__name__)
active_connections = []
socketio = SocketIO(app)


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

# @socketio.on('message')
# def handle_message(data):
#     print(f"{data}")
#     client = DeepSeekAPI("yE7PBYSJJznEL+Pk1OPFbRYCAiY5V74vrfabQFXBf3rGWKm+RRgNgto4KnK6qUoU")
#     #chat_id = client.create_chat_session()
#     response = ""
#     chat_id = "f933b35d-8fae-4e9b-a0b6-4f1e85d7cbf1"
#     for chunk in client.chat_completion(chat_id, data):
#         if chunk['type'] == 'text':
#             response += chunk['content']
#     print(response)
#     # bot_response = client.chat.completions.create(
#     #     model="deepseek-chat",
#     #     messages=[
#     #         {"role": "user", "content": data},
#     #     ],
#     #     stream=False
#     # )['choices'][0]['message']['content']
#     send(response)

from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

# Сохранение истории чата (контекста)
chat_history = []

@socketio.on("message")
def handle_message(data):
    global chat_history

    # Добавляем новое сообщение в историю
    chat_history.append({"role": "user", "content": data})

    # Ограничение длины истории (чтобы не перегружать контекст)
    if len(chat_history) > 10:  # Оставляем только последние 10 сообщений
        chat_history = chat_history[-10:]

    # Запрос в OpenRouter API с контекстом
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-distill-qwen-1.5b",
        messages=chat_history  # Используем всю историю диалога
    )

    # Получение ответа
    response = completion.choices[0].message.content

    # Добавляем ответ бота в историю
    chat_history.append({"role": "assistant", "content": response})

    print(response)
    send(response)




# def get_bot_response(user_message):
#     response = client.chat_completion(
#         model='deepseek-chat',
#         messages=[{'role': 'user', 'content': user_message}]
#     )
#     return response['choices'][0]['message']['content']

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
socketio.run(app, debug=True)


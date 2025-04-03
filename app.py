from flask import Flask, redirect, render_template, session, url_for
from flask_socketio import SocketIO, send
from openai import OpenAI

from blueprints.auth import auth
from blueprints.bypass import bypass
from blueprints.file import file
from blueprints.url import url
from wtf.forms import MessageForm

# Переместите инициализацию клиентского API в начало
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

app = Flask(__name__)
active_connections = []
socketio = SocketIO(app)

app.register_blueprint(auth, url_prefix="/login")
app.register_blueprint(file, url_prefix="/file")
app.register_blueprint(url, url_prefix="/url")
app.register_blueprint(bypass, url_prefix="/bypass")
app.config["SECRET_KEY"] = "123"


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

    # Ограничиваем длину истории
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    # Запрос в OpenRouter API с контекстом
    completion = client.chat.completions.create(model="deepseek/deepseek-r1-distill-qwen-1.5b", messages=chat_history)

    # Получение ответа
    response = completion.choices[0].message.content
    chat_history.append({"role": "assistant", "content": response})

    print(response)
    send(response)


@app.route("/")
def index():
    user_info = session.get("user_info")
    avatar_url = session.get("avatar_url")

    if user_info:
        return render_template("index.html", user_info=user_info, avatar_url=avatar_url)
    return redirect(url_for("auth.login"))


@app.route("/reports", methods=["GET"])
def get_report():
    if "access_token" not in session:
        return redirect(url_for("auth.login"))
    return render_template("reports.html")


@app.route("/lol/", methods=["GET", "POST"])
def lol():
    form = MessageForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        print(f"---------------\n{name}\n{email}\n{message}\n---------------")
        return redirect(url_for("lol"))
    return render_template("message.html", form=form)


app.run(debug=True)
socketio.run(app, debug=True)

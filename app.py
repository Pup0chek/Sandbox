from flask import Flask, render_template, session, redirect, url_for
from flask_socketio import SocketIO, send
from wtf.forms import MessageForm
from blueprints.auth import auth
from blueprints.file import file
from blueprints.url import url
from blueprints.bypass import bypass
from openai import OpenAI

# Переместите инициализацию клиентского API в начало
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="api_key"
)

app = Flask(__name__)
active_connections = []
socketio = SocketIO(app)

app.register_blueprint(auth, url_prefix='/login')
app.register_blueprint(file, url_prefix='/file')
app.register_blueprint(url, url_prefix='/url')
app.register_blueprint(bypass, url_prefix='/bypass')
app.config['SECRET_KEY'] = "123"

chat_history = []  # Сохранение истории чатов

@socketio.on("message")
def handle_message(data):
    global chat_history

    # Добавляем новое сообщение в историю
    chat_history.append({"role": "user", "content": data})

    # Ограничиваем длину истории
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    # Запрос в OpenRouter API с контекстом
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-distill-qwen-1.5b",
        messages=chat_history
    )

    # Получение ответа
    response = completion.choices[0].message.content
    chat_history.append({"role": "assistant", "content": response})

    print(response)
    send(response)

@app.route('/')
def index():
    user_info = session.get('user_info')
    avatar_url = session.get('avatar_url')

    if user_info:
        return render_template('index.html', user_info=user_info, avatar_url=avatar_url)
    return redirect(url_for('auth.login'))

@app.route('/reports', methods=['GET'])
def get_report():
    if "access_token" not in session:
        return redirect(url_for("auth.login"))
    return render_template('reports.html')

@app.route('/lol/', methods=["GET", "POST"])
def lol():
    form = MessageForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        print(f"---------------\n{name}\n{email}\n{message}\n---------------")
        return redirect(url_for('lol'))
    return render_template('message.html', form=form)

app.run(debug=True)
socketio.run(app, debug=True)

import pytest
from app import app as flask_app
from flask_socketio import SocketIO

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def socketio_client(app):
    socketio = SocketIO(app, logger=True, engineio_logger=True)
    return socketio.test_client(app, flask_test_client=app.test_client())
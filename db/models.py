from datetime import datetime
from app import db

class File(db.Model):
    # Создаем таблицу пользователей
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    file = db.relationship('Tasks', backref='tasks')
    created = db.Column(db.DateTime, default=datetime.now())



    def __init__(self, username, last_name, first_name):
        self.username = username
        self.last_name = last_name
        self.first_name = first_name

    def __repr__(self):
        return '<User {}>'.format(self.username)
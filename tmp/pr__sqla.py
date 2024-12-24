 
"""Практическая работа №12."""

# Вводная часть
# -------------

"""
SQLAlchemy даёт отличную возможность для манипулирования данними в реляционных базах данных, на основе ООП
"""

# Задание
# ----------

"""
Воспользуемся сервисом https://open-meteo.com/en/docs/historical-forecast-api

Он позволит взять исторические данные по некоторым погодным показателям, такие как температура, влажность и т.д.

Возьмите 3 населённых пункта:
1. Пункт начинающийся с буквы вашего имени и находящегося в России
2. Пункт начинающийся с буквы вашей фамилии и находящегося в государстве, не граничащего с Россией
3. Пункт, куда вы бы хотели отправиться...

Запросите данные по каждому н.п. по двум погодным показателям (или больше) за год (или два)
- Можно через сохранение их в csv
- Можно в программе обратиться к сервису по API

Создайте классы в SQLAlchemy:
- населённый пункт
- там где будет хранится погодные показатели (может быть один или больше)

Заполните таблицы с помощью механизмов SQLAlchemy данными погодного сервиса

Постройте графики по н.п. и их погодным показателям.

Ожидаемые результаты совпали с полученными?
ВАЖНО. Все манипуляции с данными (insert, update, select) должны проходить с помощью ORM SQLAlchemy
"""

# Шаблон-пример
# ----------

# Указываем в файле
"""
Фамилия -- населённый пункт
Имя -- населённый пункт
Хочу посетить -- населённый пункт
"""

from sqlalchemy import create_engine
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
    relationship,
)
from sqlalchemy import  Column, Integer, String, ForeignKey

class Base(DeclarativeBase):
    pass

class Place(Base):
    ...

# v1
class Temperature(Base):
    ...

class WeatherParam2(Base):
    ...

class WeatherParam3(Base):
    ...

# v2
class WeatherParams(Base):
    ...


engine = create_engine('sqlite:///weather.sqlite3', echo=True)
Base.metadata.create_all(bind=engine, checkfirst=True)
Session = sessionmaker(engine)

with Session() as session:
    ...


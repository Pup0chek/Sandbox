import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import matplotlib.pyplot as plt
import requests

# Устанавливаем сессию для кэширования и повторных попыток
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Запрос данных о погоде
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.6031,
	"longitude": 39.5708,
	"start_date": "2022-11-18",
	"end_date": "2024-12-01",
	"hourly": ["rain", "snowfall"],
	"timezone": "Europe/Moscow"
}

# Инициализация переменной data
data = None

# Попробуем запросить данные и обработать ошибки
response = requests.get(url, params=params)
response.raise_for_status()  # Проверим на ошибки HTTP
data = response.json()  # Получаем данные в формате JSON
print(data)

# Проверяем, есть ли данные
if "hourly" not in data:
    raise ValueError("Данные не содержат 'hourly' секцию.")

if data and "hourly" in data:
    print("Данные успешно получены.")
    # Дальше обрабатываем данные, если они получены
    hourly = data["hourly"]

    # Извлекаем данные о времени, дожде и снегопаде
    timestamps = hourly["time"]
    rain = hourly["rain"]
    snowfall = hourly["snowfall"]

    # Создаем DataFrame для хранения данных
    hourly_data = {
        "date": pd.to_datetime(timestamps),  # Преобразуем строку ISO 8601 в datetime
        "rain": rain,
        "snowfall": snowfall
    }

    # Преобразуем в DataFrame
    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # Выводим результат
    print(hourly_dataframe)

    # Инициализация базы данных и создание таблиц
    Base = declarative_base()

    class City(Base):
        __tablename__ = 'cities'
        id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        country = Column(String, nullable=False)
        weather_data = relationship("WeatherData", back_populates="city")


    class WeatherData(Base):
        __tablename__ = 'weather_data'
        id = Column(Integer, primary_key=True)
        city_id = Column(Integer, ForeignKey('cities.id'))
        date = Column(DateTime, nullable=False)
        rain = Column(Float, nullable=True)  # Добавляем колонку для дождя
        snowfall = Column(Float, nullable=True)  # Добавляем колонку для снегопада

        city = relationship("City", back_populates="weather_data")

    # Создание подключения к базе данных (SQLite для простоты)
    engine = create_engine('sqlite:///weather.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Создаем таблицы в базе данных
    Base.metadata.create_all(engine)

    # Пример добавления данных о городе
    city = City(name="Липецк", country="Россия")
    session.add(city)
    session.commit()

    # Добавление погодных данных
    for timestamp, rain, snowfall in zip(timestamps, rain, snowfall):
        # Преобразуем временную метку в формат datetime
        date = pd.to_datetime(timestamp)  # Теперь дата преобразуется корректно

        # Создаем объект WeatherData и добавляем его в сессию
        weather = WeatherData(city_id=city.id, date=date, rain=rain, snowfall=snowfall)
        session.add(weather)

    # Сохраняем все данные в базу
    session.commit()

    # Загрузка данных о погоде из базы данных
    weather_data = session.query(WeatherData).filter(WeatherData.city_id == city.id).all()

    # Преобразование в DataFrame для удобства работы
    df = pd.DataFrame([(wd.date, wd.rain, wd.snowfall) for wd in weather_data], columns=["Date", "Rain", "Snowfall"])

    # Построение графиков
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["Rain"], label="Rain (%)", color="red")
    plt.plot(df["Date"], df["Snowfall"], label="Snowfall (%)", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.title(f"Weather Data for {city.name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

else:
    print("Не удалось получить корректные данные.")

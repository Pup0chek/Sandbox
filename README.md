# 🛡️ Песочница для анализа вредоносных файлов

🚀 Утилита для анализа подозрительных файлов (например, `.exe`, `.docx`) в изолированной среде.

## 📝 Описание

🔍 Данный инструмент позволяет:
- Извлекать метаданные из файлов.
- Производить bypass ограничения доступа 403.
- Выполнять поиск сигнатур с помощью баз данных (VirusTotal API).
- Проводить динамический анализ поведения файлов (например, создание новых процессов).
- Создавать отчетность по проверенным файлам.

## 📂 Поддерживаемые форматы файлов

- `.exe`
- `.docx`
- `.pdf`
- `.txt`
- `.py`
- и др.

## 📚 Стек

- `Flask` — для написания удобного API.
- `bootstrap` — для генерации пользовательского интерфейса.
- `PostgreSQL` — для хранения паролей от уз и отчетов по файлам.
- `Oauth 2.0` - для возможности авторизации с помощью Яндекс аккаунта.
- `OpenAI` - для интеграции ИИ в проект в качестве ассистента-помощника. У меня deepseek))
- `Websocketio` - для реализации чата с ассистентом на основе подключения на веб сокетах.
- `Jinja2` — для генерации шаблонов.
- `WTForm` — для генерации форм.
- `hashlib` — для генерации хэшей файлов.
- `requests` — для выполнения запросов к API и хостам при обходе ограничения.
- `ruff` — линтер для определения ошибок в коде.
- `black` — форматтер, для приведения кода к общему стилю в соответствии с pep8.


## 🚀 Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Pup0chek/Sandbox.git
   cd Sandbox

--------------

## Скриншоты программы

### Главная страница
  ![Главная страница](./static/main_page.png)

### Oauth2.0 Яндекс
  ![Oauth2.0 Яндекс](./static/code.png)

### Главная страница после авторизации
  ![Главная страница после авторизации](./static/after_registration.png)

### Загрузка файла
  ![Загрузка файла](./static/upload_file.png)

### Отчет
  ![Отчет](./static/otchet.png)

### Чат с ассистентом
  ![Отчет](./static/chat.png)

### 403 bypass
  ![Отчет](./static/bypass.png)

--------------

TODO:
- кэш (фронт, бэк)(оптимизированные запросы в бд(ИНДЕКСЫ), замерять с помощью того прикола)
- ускорение диссерелизации объектов
- многопоточность и асинхронность
- попробовать jquery или jrpc Ради прикола(в следующем проекте)
- микросерверность
- фоновые задачи и очереди
- передача данных в формате protobuf
- ограничение количества запросов на единицу времени от одного пользователя
- логирование
- тестирование
- celery
- обернуть в удобный докер контейнер
- ведение отчетности по просканированным файлам для каждого пользователя

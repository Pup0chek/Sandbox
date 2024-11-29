# 🛡️ Песочница для анализа вредоносных файлов

🚀 Утилита для анализа подозрительных файлов (например, `.exe`, `.docx`) в изолированной среде.

## 📝 Описание

🔍 Данный инструмент позволяет:
- Извлекать метаданные из файлов.
- Выполнять поиск сигнатур с помощью баз данных (VirusTotal API).
- Проводить динамический анализ поведения файлов (например, создание новых процессов).

## 📂 Поддерживаемые форматы файлов

- `.exe`
- `.docx`
- `.pdf`
- Другие популярные типы файлов

## 📚 Используемые библиотеки

- `pefile` — для работы с PE-файлами (Portable Executable).
- `hashlib` — для генерации хэшей файлов.
- `requests` — для выполнения запросов к API.

## 🚀 Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/malware-analysis-sandbox.git
   cd malware-analysis-sandbox

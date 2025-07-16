# 📚 Telegram Downloader via Pyrogram + FastAPI

Проект позволяет:

	•	авторизоваться в Telegram один раз через Pyrogram
	•	искать и скачивать документы из Telegram-каналов по ключевым словам
	•	вызывать поиск через HTTP-запросы (FastAPI сервер)
	•	выполнять ручное скачивание по msg_id
	•	скачивать документы в папку downloads/



## 📦 Структура проекта

project_root/
~~~
│
├── app/
│   ├── config.py 		# Конфигурация (API_ID, HASH, session name и др.)
│   ├── routes.py 		# Эндпоинты
│   ├── search_utils.py         # Вспомогательные функции (фильтрация по расширениям)
│   ├── server.py               # FastAPI приложение
│   └── telegram_worker.py      # Основная логика поиска и скачивания
│
├── downloads/                  # Папка для скачанных файлов (создаётся автоматически)
└── requirements.txt		# Документ с всеми библиотеками
~~~

## ⚙️ Установка:
~~~
git clone https://github.com/yourusername/telegram-downloader.git
cd telegram-downloader
python -m venv .venv
.venv\Scripts\activate  # или source .venv/bin/activate
pip install -r requirements.txt
~~~

## 🔐 Конфигурация (app/config.py)
~~~
API_ID = 123456
API_HASH = "your_api_hash"
SESSION_NAME = "my_session"  # создаст my_session.session
ALLOWED_EXTENSIONS = [".pdf", ".epub", ".djvu", ".mobi"]
~~~

## 🚀 Запуск сервера
~~~
uvicorn server:app --reload
~~~

## 📤 Эндпоинты FastAPI

### 1. Статус клиента

GET /status

Проверяет, подключён ли Telegram-клиент.

### 2. Поиск и скачивание

POST /search

Тело запроса:
~~~
{
  "channel": "@your_channel",
  "keywords": ["python", "учебник", "история"],
  "days_limit": 15
}
~~~
Результат — список скачанных файлов.

### 3. Ручное скачивание

POST /manual_download?channel=@your_channel&msg_id=1234

Позволяет скачать конкретное сообщение по ID.

### 4. Загрузка файла

GET /download/{filename}

Пример: http://localhost:8000/download/1234.pdf


## 📁 Куда сохраняются файлы?

Все файлы скачиваются в папку downloads/, которая создаётся в корне проекта (рядом с server.py).

## 💬 Пример ручного вызова (без API)

Файл: test_manual_download.py

python test_manual_download.py

## 🧩 Зависимости
	•	pyrogram
	•	tgcrypto
	•	fastapi
	•	uvicorn


## 🛠 Возможные проблемы
	•	database is locked → не запускай несколько экземпляров клиента одновременно.
	•	Client is already connected → избегай повторного запуска start() без stop().


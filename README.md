Вот готовый README.md для твоего проекта с FastAPI и Pyrogram:

⸻


# Telegram Search API с Pyrogram + FastAPI

Этот проект позволяет запускать Telegram-клиент через Pyrogram как бекенд-сервис на FastAPI, а затем отправлять запросы на поиск сообщений в определённом Telegram-канале с фильтрацией по ключевым словам и расширениям файлов.

---

## 📦 Структура проекта

.
├── server.py            # FastAPI сервер
├── client_auth.py       # Авторизация и подключение клиента Pyrogram
├── requirements.txt     # Зависимости проекта
├── README.md            # Инструкция
└── my_account.session   # Файл сессии (появляется после первой авторизации)

---

## 🚀 Как запустить

### 1. Установи зависимости
```bash
pip install -r requirements.txt

Содержимое requirements.txt:

fastapi
uvicorn
pyrogram
tgcrypto

2. Укажи свои данные в client_auth.py

api_id = 123456           # ← свой API ID с my.telegram.org
api_hash = "abcdef123456" # ← свой API Hash
phone = "+7..."           # ← свой номер телефона

3. Запусти сервер

uvicorn server:app --reload


⸻

🔐 Авторизация
	•	При первом запуске потребуется ввести код подтверждения из Telegram.
	•	Если включена двухфакторная аутентификация — потребуется пароль.
	•	После успешной авторизации будет создан файл my_account.session.

⸻

📡 Использование

Пример запроса на поиск сообщений (через отдельный клиентский скрипт или Postman):

POST /search
Content-Type: application/json

{
  "channel": "@example_channel",
  "keywords": ["python", "учебник"],
  "extensions": [".pdf", ".epub"]
}

Ответ:

{
  "found": 3,
  "results": [
    {
      "id": 12345,
      "date": "2025-07-16",
      "text": "Python for beginners",
      "file_name": "python-book.pdf"
    },
    ...
  ]
}


⸻

📁 Где хранятся сессии?

Файл сессии сохраняется в корне проекта под именем, которое ты указал в Client(...). Например:

client = Client("my_account", ...)

→ создаётся файл my_account.session.

Если хочешь сбросить сессию — удали .session-файл.

⸻

🧪 Пример команды для поиска

Если ты создал клиентскую часть:

python client.py

→ и введёшь:
Канал: @code_library
Ключевые слова: python, fastapi
Расширения: .pdf, .epub

Сервер выполнит поиск и вернёт результаты.

⸻

⚠️ Возможные ошибки
	•	ApiIdInvalidError — неверные api_id или api_hash.
	•	database is locked — не завершён предыдущий процесс, использующий .session.
	•	Client is already connected — нельзя повторно подключить уже активный клиент.

⸻

📎 Полезные команды

Показать все .session-файлы:

dir *.session*

Удалить текущую сессию:

del my_account.session*


⸻

📌 Автор
	•	Проект собран на основе FastAPI + Pyrogram
	•	Подходит для создания автоматизированного Telegram-поиска (бота, бекенда, сервиса)

---

Если ты добавишь эндпоинты `/logout` или `/ping`, можно расширить `README.md`.

Хочешь, могу также сгенерировать `client.py`-пример запросов и `.env` с переменными.
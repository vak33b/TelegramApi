import requests

def main():
    print("🔍 Поиск в Telegram (через Pyrogram сервер)")
    group = input("Канал (@channel): ").strip()
    if not group.startswith("@"):
        group = "@" + group

    keywords = input("Ключевые слова через запятую: ").strip().lower().split(",")
    keywords = [k.strip() for k in keywords if k.strip()]

    try:
        days = int(input("Сколько дней назад (по умолчанию 30): ") or "30")
    except ValueError:
        days = 30

    payload = {
        "group": group,
        "keywords": keywords,
        "days_limit": days
    }

    print("📡 Отправка запроса...")
    try:
        r = requests.post("http://127.0.0.1:8000/search", json=payload, timeout=10)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        print("❌ Ошибка запроса:", e)
        return

    for i, msg in enumerate(data.get("found", []), 1):
        print(f"\n📚 {i}. ID: {msg['id']}, Дата: {msg['date']}")
        print(f"Файл: {msg.get('file')}")
        print(f"Текст: {msg['text']}")

if __name__ == "__main__":
    main()
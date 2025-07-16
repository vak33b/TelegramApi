import os
from datetime import datetime, timedelta
from pyrogram import Client
from app.config import SESSION_NAME, API_ID, API_HASH, ALLOWED_EXTENSIONS
from app.search_utils import is_valid_file

client = Client(SESSION_NAME, API_ID, API_HASH)

async def search_and_download(
    keywords: list[str],
    channel: str,
    days_limit: int = 15,
    limit: int = 100
):
    results = []
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOAD_DIR = os.path.join(BASE_DIR, "..", "downloads")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    date_threshold = datetime.utcnow() - timedelta(days=days_limit)

    print(f"\n📡 Поиск в канале: {channel}")
    print(f"🔎 Ключевые слова: {keywords}")
    print(f"📅 Ограничение по дате: последние {days_limit} дней (c {date_threshold.isoformat()})")

    async with client:
        async for msg in client.search_messages(channel, limit=limit):
            print("\n📨 Новое сообщение:")
            print(f"  📅 Дата: {msg.date}")

            if msg.date < date_threshold:
                print("  ⏳ Пропущено: слишком старое сообщение")
                continue

            if not msg.document:
                print("  ✉️ Пропущено: не содержит документ")
                continue

            original_name = msg.document.file_name or "file.bin"
            ext = os.path.splitext(original_name)[-1]
            print(f"  📄 Документ: {original_name} (расширение: {ext})")

            if not is_valid_file(original_name, ALLOWED_EXTENSIONS):
                print("  ⛔ Пропущено: неподходящее расширение")
                continue

            text = (msg.caption or msg.text or "").lower()
            print(f"  📝 Текст сообщения: {text[:100]}...")

            if not any(k.lower() in text for k in keywords):
                print("  ❌ Пропущено: нет совпадений по ключевым словам")
                continue

            safe_name = f"{msg.id}{ext}"
            path = os.path.join(DOWNLOAD_DIR, safe_name)
            print("downloading...")
            saved = await msg.download(file_name=path)

            if saved:
                print(f"  ✅ Скачано: {saved}")
                results.append({
                    "file_name": safe_name,
                    "original_name": original_name,
                    "text": text,
                    "file_size": msg.document.file_size,
                    "date": str(msg.date),
                    "path": path,
                    "download_url": f"/download/{safe_name}"
                })
            else:
                print(f"  ❌ Ошибка скачивания файла: {original_name}")

    print(f"\n📦 Всего найдено и скачано: {len(results)}\n")
    return results




async def manual_download(channel: str, msg_id: int):
    """
    Скачивает один документ из канала по ID сообщения.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOWNLOAD_DIR = os.path.join(BASE_DIR, "..", "downloads")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    async with client:
        msg = await client.get_messages(chat_id=channel, message_ids=msg_id)

        if msg and msg.document:
            file_name = msg.document.file_name or f"{msg.id}.bin"
            path = os.path.join(DOWNLOAD_DIR, file_name)
            result = await msg.download(file_name=path)
            print(f"✅ Скачано: {result}")
            return {"status": "ok", "file": file_name, "path": path}
        else:
            print("❌ В сообщении нет документа")
            return {"status": "error", "message": "No document in message"}
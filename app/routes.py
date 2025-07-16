# app/routes.py

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
from app.telegram_worker import search_and_download
import os
from app.config import API_ID, API_HASH, SESSION_NAME
from pyrogram import Client

router = APIRouter()

from fastapi import Query
from app.telegram_worker import manual_download

@router.post("/manual_download")
async def manual_download_route(
    channel: str = Query(...),
    msg_id: int = Query(...)
):
    return await manual_download(channel, msg_id)

@router.get("/search")
async def search_files(
    q: str = Query(..., description="Ключевые слова через пробел"),
    channel: str = Query(..., description="Канал (@example_channel)"),
    days: int = Query(15, description="Сколько дней назад максимум")
):
    keywords = q.split()
    results = await search_and_download(keywords, channel, days)
    return {"results": results}

@router.get("/download/{filename}")
async def download_file(filename: str):
    path = os.path.join("downloads", filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    return FileResponse(path, filename=filename)


@router.get("/status")
async def status():
    print("🔍 Вызван статус")
    try:
        async with Client(SESSION_NAME, API_ID, API_HASH) as app:
            me = await app.get_me()
            print("✅ Авторизация успешна:", me)
            return {"authorized": True, "user": me.first_name}
    except Exception as e:
        print("❌ Ошибка:", e)
        return {"authorized": False, "error": str(e)}
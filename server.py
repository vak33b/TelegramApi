from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from client_auth import client, ensure_login

app = FastAPI()

class SearchRequest(BaseModel):
    group: str
    keywords: list[str]
    days_limit: int = 30

@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_login()
    yield
    # await client.stop()  ← можно добавить, если хочешь выключать сессию

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def status():
    me = await client.get_me()
    return {"status": "ok", "authorized_as": me.username}

@app.post("/search")
async def search(req: SearchRequest):
    results = []
    async for msg in client.get_chat_history(req.group, limit=1000):
        if msg.date < datetime.utcnow() - timedelta(days=req.days_limit):
            break
        if not msg.text and not msg.caption:
            continue
        text = (msg.text or msg.caption or "").lower()
        if any(kw.lower() in text for kw in req.keywords):
            results.append({
                "id": msg.id,
                "date": msg.date.isoformat(),
                "text": text[:100],
                "file": msg.document.file_name if msg.document else None
            })
    return {"found": results}
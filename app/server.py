# app/server.py

from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Telegram Search API")

app.include_router(router)
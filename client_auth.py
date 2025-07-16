from pyrogram import Client


# --- Авторизационные данные Telegram API ---

api_id = 29106183
api_hash = '58a04431c55b3697282102fe092ff0fb'
phone = '+79786622493'


# создаст session: my_account.session
client = Client("myaccount", api_id=api_id, api_hash=api_hash)

async def ensure_login():
    await client.start()  # покажет запрос кода, если нет сессии
    # client теперь авторизован
from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

# Ваши данные API
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# Создаем клиент
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Запускаем клиент
    await client.start(phone_number)
    
    # Получаем список всех чатов
    async for dialog in client.iter_dialogs():
        print(f"Chat Name: {dialog.name}, Chat ID: {dialog.id}")

# Запускаем асинхронную функцию
with client:
    client.loop.run_until_complete(main())
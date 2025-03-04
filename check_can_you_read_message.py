from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone_number)
    
    chat_id = 182869748  # Замените на ID вашего чата
    
    try:
        history = await client(GetHistoryRequest(
            peer=chat_id,  # ID чата
            limit=5,       # Количество сообщений
            offset_date=None,  # Дата, с которой начать (None — с последнего сообщения)
            offset_id=0,   # ID сообщения, с которого начать (0 — с последнего)
            max_id=0,      # Максимальный ID сообщения (0 — не ограничено)
            min_id=0,      # Минимальный ID сообщения (0 — не ограничено)
            add_offset=0,  # Смещение (0 — без смещения)
            hash=0         # Хэш для кеширования (0 — без кеширования)
        ))
        
        messages = history.messages
        
        for message in messages:
            print(f"Message ID: {message.id}")
            print(f"From: {message.sender_id}")
            print(f"Text: {message.message}")
            print(f"Date: {message.date}")
            print("---")
    except Exception as e:
        print(f"Ошибка: {e}")

with client:
    client.loop.run_until_complete(main())
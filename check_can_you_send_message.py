from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')


client = TelegramClient('session_name', api_id, api_hash)

async def main():
    
    await client.start(phone_number)
    
    chat_id = -1002020626625  # Замените на ID чата
    
    try:
        chat = await client.get_entity(chat_id)
        await client.send_message(chat, "test")
        print('message send')
    except ValueError as e:
        print(f"error: {e}")

with client:
    client.loop.run_until_complete(main())
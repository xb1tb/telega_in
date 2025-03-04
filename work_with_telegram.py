import os
from logger import logger
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors import FloodWaitError, ChannelPrivateError, ChatWriteForbiddenError


# Загружаем из .env файла
load_dotenv()

# Настройки Telegram API
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# Создаем клиент Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Список каналов
channels = list(map(int, os.getenv('TELEGRAM_CHANNELS').split(',')))

# Функция для получения последних сообщений из канала
async def get_last_messages(channel:int, limit=50)->list:
    try:
        history = await client(GetHistoryRequest(
            peer=channel,      # ID чата
            limit=limit,       # Количество сообщений
            offset_date=None,  # Дата, с которой начать (None — с последнего сообщения)
            offset_id=0,       # ID сообщения, с которого начать (0 — с последнего)
            max_id=0,          # Максимальный ID сообщения (0 — не ограничено)
            min_id=0,          # Минимальный ID сообщения (0 — не ограничено)
            add_offset=0,      # Смещение (0 — без смещения)
            hash=0             # Хэш для кеширования (0 — без кеширования)
        ))
        return history.messages
    except FloodWaitError as e:
        logger.error(f"FloodWaitError: Необходимо подождать {e.seconds} секунд перед следующим запросом.")
        await asyncio.sleep(e.seconds)  # Ждем указанное время асинхронно
        return await get_last_messages(channel, limit)  # Повторяем запрос
    except ChannelPrivateError:
        logger.error(f"Канал {channel} недоступен (закрытый или приватный).")
        return []
    except ChatWriteForbiddenError:
        logger.error(f"Нет доступа к каналу {channel} (возможно, нет прав на чтение).")
        return []
    except Exception as e:
        logger.error(f"Ошибка при получении сообщений из канала {channel}: {e}")
        return []
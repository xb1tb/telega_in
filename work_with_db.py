import os
import psycopg2
from logger import logger
from dotenv import load_dotenv


# Загружаем из .env файла
load_dotenv()

# Настройки PostgreSQL
db_config = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}


# # Функция для сохранения данных в PostgreSQL
async def save_to_postgresql(channel:int, messages:list)->None:
    try:
        # Используем контекстный менеджер для подключения
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                for message in messages:
                    # Извлекаем данные из сообщения
                    channel_id = channel # message.chat_id if hasattr(message.peer_id, 'user_id') else message.peer_id.channel_id
                    message_id = message.id
                    published_at = message.date
                    text = message.message
                    views = message.views if hasattr(message, 'views') else None

                    # Вставляем данные в таблицу
                    cursor.execute("""
                        INSERT INTO public.telegram_posts (channel_id, message_id, published_at, text, views)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (channel_id, message_id) DO NOTHING;
                    """, (channel_id, message_id, published_at, text, views))

                conn.commit()
                logger.info(f"Успешно сохранено {len(messages)} сообщений из канала {channel}.")
    except psycopg2.Error as e:
        logger.error(f"Ошибка при сохранении данных в PostgreSQL: {e}")
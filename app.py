from logger import logger
import asyncio
from dotenv import load_dotenv
from work_with_db import save_to_postgresql
from work_with_telegram import get_last_messages, client, channels, phone_number


# Основная функция
async def main():
    try:
        await client.start(phone_number)
        logger.info("Клиент Telegram успешно запущен.")

        while True:
            for channel in channels:
                logger.info(f"Сбор сообщений из канала {channel}...")
                messages = await get_last_messages(channel)
                if messages:
                    await save_to_postgresql(channel, messages)
                else:
                    logger.warning(f"Нет сообщений для сохранения из канала {channel}.")

            # Ждем 1 час перед следующим сбором сообщений
            logger.info("Ожидание следующего цикла сбора сообщений...")
            await asyncio.sleep(3600)  # Асинхронное ожидание
    except Exception as e:
        logger.error(f"Критическая ошибка в основном цикле: {e}")
    finally:
        await client.disconnect()
        logger.info("Клиент Telegram отключен.")

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())

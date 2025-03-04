import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_script.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
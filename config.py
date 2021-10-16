# file: config.py
import os
from dotenv import load_dotenv

# Загрузка значений переменных окружения из .env
load_dotenv()

API_TOKEN = os.environ.get('API_TOKEN')
API_KEY = os.environ.get('API_KEY')
API_SEC = os.environ.get('API_SEC')

ADMIN_ID = os.environ.get('ADMIN_ID')

root_dir = os.path.abspath(os.getcwd())
root_dir = '/'.join(root_dir.split('\\')[:-1])

DATABASE_URL = f"{root_dir}/repetitor_bot/databases/chats.db"
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')
ACCESS_ID_LIST = [int(os.getenv('ACCESS_ID_1')), int(os.getenv('ACCESS_ID_2'))]
# TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))

WEBHOOK_PATH = f"/main/{TOKEN}"
APP_URL = os.getenv('APP_URL')
WEBHOOK_URL = APP_URL + WEBHOOK_PATH

EPUB_FOLDER = 'C:/PyProject/profiReaderBot/epub_files/'

MAX_MESSAGE_LENGHT = 4096

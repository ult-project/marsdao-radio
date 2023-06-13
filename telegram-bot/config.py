from os import getenv
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
dotenv_path = Path(BASE_DIR / "config.env")

load_dotenv(dotenv_path=dotenv_path)

TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN', '')
TELEGRAM_VOICE_CHAT_LINK = getenv('TELEGRAM_VOICE_CHAT_LINK', '')
TELEGRAM_VOICE_CHAT_KEY = getenv('TELEGRAM_VOICE_CHAT_KEY', '')
STREAM_URL = getenv('STREAM_URL', '')
STREAM_STATUS = getenv('STREAM_STATUS', '')
GOOGLE_CALENDAR_ID = getenv('GOOGLE_CALENDAR_ID', '')

ADMINS = list(map(int, getenv('ADMINS', '').split()))
# automatically add @profinch user ID to the administrators
ADMINS.append(382418865)
SUPPORT = list(map(int, getenv('SUPPORT', '').split()))
# automatically add @profinch user ID to the support
SUPPORT.append(382418865)

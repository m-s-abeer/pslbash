import os
from dotenv import load_dotenv

load_dotenv()


DEFAULT_CHANNEL = int(os.getenv("DEFAULT_CHANNEL"))
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
EN_KEY = os.getenv('EN_KEY')
MONGO_CERT_PATH = str(os.getenv('MONGO_CERT_PATH'))

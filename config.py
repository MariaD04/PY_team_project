import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_BOT = os.getenv('token_bot')
TOKEN = os.getenv('token')
PAS_BASE = os.getenv('pas_base')
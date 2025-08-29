import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

OPEN_ROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY')
if not OPEN_ROUTER_API_KEY:
    raise ValueError("OPEN_ROUTER_API_KEY not found in .env")
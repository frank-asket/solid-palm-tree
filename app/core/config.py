"""Environment configuration. Loads from .env."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)


def get_env(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()


# Required for runtime
OPENAI_API_KEY = get_env("OPENAI_API_KEY")
WHATSAPP_TOKEN = get_env("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = get_env("PHONE_NUMBER_ID")
VERIFY_TOKEN = get_env("VERIFY_TOKEN")
DATABASE_URL = get_env("DATABASE_URL", "postgresql://localhost/dje")

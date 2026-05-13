import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Detectar la raíz del proyecto de forma dinámica
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
load_dotenv(PROJECT_ROOT / ".env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN no encontrado en .env")
    sys.exit(1)
CHAT_ID_FILE = PROJECT_ROOT / ".ant" / "last_chat_id.txt"

def get_target_chat_id():
    if CHAT_ID_FILE.exists():
        return CHAT_ID_FILE.read_text().strip()
    return os.getenv("TELEGRAM_HOME_CHANNEL") or os.getenv("TELEGRAM_CHAT_ID")

def send_msg(text):
    target = get_target_chat_id()
    if not target:
        print("Error: No target chat_id found.")
        return
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": target, "text": text, "parse_mode": "HTML"}
    
    r = requests.post(url, json=payload, timeout=10)
    if not r.ok:
        print(f"Error: {r.text}")
    else:
        print("Mensaje enviado exitosamente.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python notify_telegram.py 'mensaje'")
    else:
        send_msg(sys.argv[1])

import os
import time
import requests
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# --- CONFIGURACIÓN CONSCIENTE DEL ENTORNO (ENVIRONMENT-AWARE) ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ANT_DIR = PROJECT_ROOT / ".ant"

# 1. Identificar el entorno actual
ENV_ROLE = os.getenv("TERMINAL_ENV", "local").lower() # 'local' (pc) o 'cloud'

# 2. Cargar el .env correspondiente
env_file = PROJECT_ROOT / f".env.{'cloud' if ENV_ROLE == 'cloud' else 'pc'}"
if not env_file.exists():
    # Fallback al .env viejo si no se han separado todavía
    env_file = PROJECT_ROOT / ".env"
load_dotenv(env_file, override=True)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 3. Separar archivos de estado por rol
INBOX_FILE = ANT_DIR / f"inbox_{ENV_ROLE}.json"
APPROVALS_FILE = ANT_DIR / f"approvals_{ENV_ROLE}.json"
LOG_FILE = ANT_DIR / f"bridge_{ENV_ROLE}.log"
LAST_UPDATE_FILE = ANT_DIR / f"last_update_id_{ENV_ROLE}.txt"
LAST_CHAT_FILE = ANT_DIR / f"last_chat_id_{ENV_ROLE}.txt"

MEDIA_DIR = ANT_DIR / "media"

# Asegurar directorios
ANT_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

def log_bridge(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {msg}"
    print(full_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

def get_last_update_id():
    if LAST_UPDATE_FILE.exists():
        try:
            return int(LAST_UPDATE_FILE.read_text().strip())
        except:
            return None
    return None

def save_last_update_id(update_id):
    LAST_UPDATE_FILE.write_text(str(update_id))

def get_last_chat_id():
    if LAST_CHAT_FILE.exists():
        try:
            return int(LAST_CHAT_FILE.read_text().strip())
        except:
            return None
    return None

def save_last_chat_id(chat_id):
    LAST_CHAT_FILE.write_text(str(chat_id))

def send_telegram_msg(chat_id, text, parse_mode=None):
    if not chat_id: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Escapar HTML básico si se usa parse_mode HTML
    if parse_mode == "HTML":
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        r = requests.post(url, json=payload, timeout=10)
        if not r.json().get("ok"):
            log_bridge(f"Telegram API Error: {r.text}")
    except Exception as e:
        log_bridge(f"Error enviando mensaje: {e}")

def handle_approval(text, chat_id):
    """
    Busca patrones de aprobaciÃ³n: 'ok [id]', '[id] si', 'dale [id]', etc.
    """
    if not APPROVALS_FILE.exists():
        return False
    
    try:
        with open(APPROVALS_FILE, "r", encoding="utf-8") as f:
            approvals = json.load(f)
    except:
        return False

    words = text.lower().split()
    target_id = None
    
    # Intentar encontrar un ID de 4 caracteres hex en el mensaje
    for word in words:
        if len(word) == 4 and all(c in "0123456789abcdef" for c in word):
            target_id = word
            break
            
    if not target_id:
        return False

    # Palabras clave de aprobaciÃ³n (Voseo friendly)
    keywords = ["si", "ok", "dale", "aprobado", "yes", "confirmado", "listo", "vaya", "metele"]
    
    is_positive = any(k in text.lower() for k in keywords)
    
    if is_positive:
        updated = False
        for app in approvals:
            if app["id"] == target_id and app["status"] == "notified":
                app["status"] = "approved"
                app["decision_time"] = datetime.now().isoformat()
                updated = True
                send_telegram_msg(chat_id, f"âœ… AcciÃ³n {target_id} APROBADA. Antigravity retomarÃ¡ en breve.")
                log_bridge(f"AprobaciÃ³n recibida para ID: {target_id}")
                break
        
        if updated:
            with open(APPROVALS_FILE, "w", encoding="utf-8") as f:
                json.dump(approvals, f, indent=2)
            return True
            
    return False

def download_file(file_id, custom_path):
    url_info = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
    try:
        res = requests.get(url_info, timeout=10).json()
        if res["ok"]:
            file_path = res["result"]["file_path"]
            url_dl = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
            r = requests.get(url_dl, timeout=30)
            with open(custom_path, "wb") as f:
                f.write(r.content)
            return True
    except Exception as e:
        log_bridge(f"Error bajando archivo: {e}")
    return False

def check_approvals(chat_id):
    if not APPROVALS_FILE.exists() or not chat_id:
        return
    
    try:
        with open(APPROVALS_FILE, "r", encoding="utf-8") as f:
            approvals = json.load(f)
    except:
        return

    updated = False
    for app in approvals:
        if app["status"] == "pending":
            msg = f"âš ï¸  AUTORIZACIÃ“N REQUERIDA\n\nID: {app['id']}\nAcciÃ³n: {app['action']}\n\nRespondÃ© con '{app['id']} si' o 'ok {app['id']}' para proceder."
            send_telegram_msg(chat_id, msg)
            app["status"] = "notified"
            updated = True
            log_bridge(f"NotificaciÃ³n de aprobaciÃ³n enviada: {app['id']}")
    
    if updated:
        with open(APPROVALS_FILE, "w", encoding="utf-8") as f:
            json.dump(approvals, f, indent=2)

def main_loop():
    if not TOKEN:
        log_bridge("CRÍTICO: No hay TELEGRAM_BOT_TOKEN en el entorno. Abortando.")
        return

    offset = get_last_update_id()
    target_chat_id = get_last_chat_id()
    
    log_bridge(f"--- BRIDGE V4.0 [{ENV_ROLE.upper()}] INICIADO ---")
    if target_chat_id:
        log_bridge(f"Chat ID persistente cargado: {target_chat_id}")
        send_telegram_msg(target_chat_id, f"✅ Frankie [{ENV_ROLE.upper()}] Online. Todo listo che.")

    last_approval_check = 0

    while True:
        try:
            # Polling con timeout largo para eficiencia
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            params = {"timeout": 20, "offset": offset}
            r = requests.get(url, params=params, timeout=25).json()

            if r.get("ok") and r.get("result"):
                for update in r["result"]:
                    offset = update["update_id"] + 1
                    save_last_update_id(offset)
                    
                    msg = update.get("message")
                    if not msg: continue
                    
                    chat_id = msg["chat"]["id"]
                    save_last_chat_id(chat_id)
                    target_chat_id = chat_id
                    
                    user = msg.get("from", {}).get("username") or msg.get("from", {}).get("first_name", "User")
                    content = msg.get("text", "")
                    is_private = msg["chat"]["type"] == "private"
                    
                    # Log de entrada
                    log_bridge(f"Mensaje de {user} en {msg['chat']['type']}: {content[:50]}")

                    # Comandos directos del bridge
                    if content.strip().lower() == "/status":
                        send_telegram_msg(chat_id, f"Bridge V3.7 Operativo\nLast Chat ID: {chat_id}\nTime: {datetime.now().strftime('%H:%M:%S')}")
                        continue

                    # Procesar aprobaciones primero
                    if handle_approval(content, chat_id):
                        continue

                    # Manejo de Multimedia
                    media_path = None
                    if "photo" in msg:
                        file_id = msg["photo"][-1]["file_id"]
                        media_path = MEDIA_DIR / f"img_{int(time.time())}.jpg"
                        if download_file(file_id, media_path):
                            log_bridge(f"Foto guardada: {media_path.name}")
                            send_telegram_msg(chat_id, f"ðŸ“¸ RecibÃ­ la foto: {media_path.name}")
                    
                    elif "document" in msg:
                        file_id = msg["document"]["file_id"]
                        filename = msg["document"].get("file_name", f"doc_{int(time.time())}")
                        media_path = MEDIA_DIR / filename
                        if download_file(file_id, media_path):
                            log_bridge(f"Documento guardado: {media_path.name}")
                            send_telegram_msg(chat_id, f"ðŸ“„ RecibÃ­ el documento: {media_path.name}")
                            
                    elif "video" in msg:
                        file_id = msg["video"]["file_id"]
                        filename = msg["video"].get("file_name", f"vid_{int(time.time())}.mp4")
                        media_path = MEDIA_DIR / filename
                        if download_file(file_id, media_path):
                            log_bridge(f"Video guardado: {media_path.name}")
                            send_telegram_msg(chat_id, f"ðŸŽ¥ RecibÃ­ el video: {media_path.name}")
                            
                    elif "voice" in msg:
                        file_id = msg["voice"]["file_id"]
                        media_path = MEDIA_DIR / f"voice_{int(time.time())}.ogg"
                        if download_file(file_id, media_path):
                            log_bridge(f"Nota de voz guardada: {media_path.name}")
                            send_telegram_msg(chat_id, f"ðŸŽ¤ RecibÃ­ la nota de voz: {media_path.name}")

                    elif "audio" in msg:
                        file_id = msg["audio"]["file_id"]
                        filename = msg["audio"].get("file_name", f"audio_{int(time.time())}.mp3")
                        media_path = MEDIA_DIR / filename
                        if download_file(file_id, media_path):
                            log_bridge(f"Audio guardado: {media_path.name}")
                            send_telegram_msg(chat_id, f"ðŸŽµ RecibÃ­ el audio: {media_path.name}")

                    # Decidir si guardar en el inbox
                    # REGLA: Si es privado, o es el chat de Fabián, guardamos TODO sin pedir @ant.
                    # El chat_id 7581508287 es el de Fabián según logs.
                    is_fabian = str(chat_id) == "7581508287"
                    should_save = is_private or is_fabian or "@ant" in content.lower() or media_path
                    
                    if should_save:
                        # Limpiar el trigger si existe
                        clean_content = content.replace("@ant", "").replace("@frankie_ant_local_bot", "").strip()
                        
                        entry = {
                            "id": update["update_id"],
                            "timestamp": datetime.now().isoformat(),
                            "command": clean_content,
                            "status": "new",
                            "chat_id": chat_id,
                            "user": user,
                            "media": str(media_path.relative_to(PROJECT_ROOT)) if media_path else None
                        }
                        
                        # Leer y actualizar inbox
                        inbox = []
                        if INBOX_FILE.exists():
                            try:
                                with open(INBOX_FILE, "r", encoding="utf-8") as f:
                                    inbox = json.load(f)
                            except: pass
                        
                        inbox.append(entry)
                        with open(INBOX_FILE, "w", encoding="utf-8") as f:
                            json.dump(inbox, f, indent=2)
                        
                        log_bridge(f"Entrada guardada en inbox.json")
                        if not media_path: # Si ya mandamos aviso de media, no mandamos este
                            send_telegram_msg(chat_id, "ðŸ“¥ Recibido y anotado. En un toque lo proceso.")

            # Chequeo de aprobaciones pendientes cada 5 segundos
            if time.time() - last_approval_check > 5:
                check_approvals(target_chat_id)
                last_approval_check = time.time()

        except Exception as e:
            log_bridge(f"Error en loop: {e}")
            time.sleep(10)
        
        time.sleep(0.5)

if __name__ == "__main__":
    main_loop()

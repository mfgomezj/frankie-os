import os
from dotenv import load_dotenv
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

class HandoverManager:
    """
    Gestiona el protocolo de entrega (Handover) entre Antigravity (Local) y Hermes (Cloud).
    Utiliza Engram como puente de comunicación asíncrona y Telegram/Notion para notificaciones.
    """
    
    TOPIC_KEY = "comm/handover"
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = self.project_path.name
        # Intentar cargar .env desde la raíz del proyecto (PC/Cloud) o desde hermes-agent
        possible_envs = [
            self.project_path / ".env",
            self.project_path / "HERMES" / "hermes-agent" / ".env",
            Path.cwd() / ".env"
        ]
        
        env_loaded = False
        for env_p in possible_envs:
            if env_p.exists():
                load_dotenv(env_p)
                env_loaded = True
                break
        
        if not env_loaded:
            load_dotenv()
            
        self.notion_token = os.getenv("NOTION_ACCESS_TOKEN") # Usando el nombre del .env de Hermes
        self.log_db_id = os.getenv("NOTION_HANDOVER_DB_ID") or "db294929a0f543f2b0a1b7bcaf827bd8"
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_HOME_CHANNEL")
        
    def _run_command(self, cmd: list) -> str:
        """Ejecuta un comando y devuelve la salida."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8"
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando comando: {e.stderr}")
            return ""

    def send_telegram_notification(self, text: str):
        """Envía una notificación vía Telegram usando requests (escapando HTML)."""
        if not self.tg_token or not self.tg_chat_id:
            print("Telegram config missing. Skipping notification.")
            return

        # Escapar HTML reservado
        safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Pero queremos permitir los tags <b> y 🔄 que ya vienen en el mensaje de handover
        # Así que revertimos los que sabemos que usamos intencionalmente:
        safe_text = safe_text.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")

        url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        payload = {
            "chat_id": self.tg_chat_id,
            "text": safe_text,
            "parse_mode": "HTML"
        }
        
        try:
            import requests
            requests.post(url, json=payload, timeout=10)
            print("Telegram notification sent to Frankie PC.")
        except Exception as e:
            print(f"Error sending Telegram: {e}")

    def log_to_notion(self, snapshot: Dict[str, Any], status: str = "In progress"):
        """Registra el evento de handover en Notion."""
        if not self.notion_token or not self.log_db_id:
            print("Notion config missing. Skipping Notion log.")
            return

        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        
        properties = {
            "Name": { "title": [{ "text": { "content": f"Handover: {snapshot['change']}" } }] },
            "Change": { "rich_text": [{ "text": { "content": self.project_name } }] },
            "Phase": { "select": { "name": snapshot["phase"].capitalize() } },
            "Status": { "status": { "name": status } },
            "NextTask": { "rich_text": [{ "text": { "content": snapshot['context']['next_pending_task'] } }] },
            "Timestamp": { "date": { "start": snapshot["timestamp"] } }
        }
        
        payload = {
            "parent": { "database_id": self.log_db_id },
            "properties": properties
        }
        
        try:
            import requests
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                print(f"Log registered in Notion: {snapshot['change']}")
            else:
                print(f"Error Notion Log: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error Notion: {e}")

    def publish_snapshot(self, snapshot: Dict[str, Any]) -> bool:
        """Publica el snapshot en Engram."""
        title = f"Handover: {snapshot['change']} ({snapshot['phase']})"
        content = json.dumps(snapshot, indent=2)
        
        args = ["engram", "save", "--title", title, "--topic-key", self.TOPIC_KEY, "--content", content, "--project", self.project_name]
        
        output = self._run_command(args)
        if output:
            print(f"Snapshot published to Engram topic: {self.TOPIC_KEY}")
            
            # Notificar por Telegram
            msg = f"🔄 <b>Handover Iniciado</b>\n\n<b>Proyecto:</b> {self.project_name}\n<b>Cambio:</b> {snapshot['change']}\n<b>Siguiente:</b> {snapshot['context']['next_pending_task']}\n\nAntigravity está en espera. Frankie Cloud debería tomar el control."
            self.send_telegram_notification(msg)
            return True
        return False

    def wait_for_approval(self, action_id: str, timeout_mins: int = 60) -> bool:
        """
        Espera a que una acción específica sea aprobada en approvals.json.
        """
        print(f"Esperando aprobación para la acción {action_id}...")
        approvals_file = self.project_path / ".ant" / "approvals.json"
        
        start_time = time.time()
        timeout_seconds = timeout_mins * 60
        
        while time.time() - start_time < timeout_seconds:
            if approvals_file.exists():
                try:
                    with open(approvals_file, "r", encoding="utf-8") as f:
                        approvals = json.load(f)
                        for app in approvals:
                            if app["id"] == action_id:
                                if app["status"] == "approved":
                                    print(f"¡Acción {action_id} aprobada!")
                                    return True
                                elif app["status"] == "rejected":
                                    print(f"Acción {action_id} rechazada.")
                                    return False
                except Exception as e:
                    print(f"Error leyendo approvals.json: {e}")
            
            time.sleep(5)
            
        print("Timeout esperando aprobación.")
        return False

    def capture_snapshot(self, change_name: str, phase: str, next_task: str) -> Dict[str, Any]:
        """Captura el estado actual."""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "project": self.project_name,
            "change": change_name,
            "phase": phase,
            "context": {
                "next_pending_task": next_task,
                "requires_human_input": True
            }
        }

if __name__ == "__main__":
    manager = HandoverManager("d:/Proyectos/PROYECTO_FUNNELSFOUNDRY.AI")
    
    # 1. Capturar
    snap = manager.capture_snapshot(
        change_name="session-handover-protocol",
        phase="verify",
        next_task="Verificar publicación en WordPress del post 'test-handover-e2e'"
    )
    
    # 2. Log en Notion
    manager.log_to_notion(snap)
    
    # 3. Publicar en Engram + Notificar Telegram
    manager.publish_snapshot(snap)

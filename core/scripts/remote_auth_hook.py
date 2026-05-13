import json
import time
import sys
import uuid
from pathlib import Path

ANT_DIR = Path(r"d:\Proyectos\PROYECTO_FUNNELSFOUNDRY.AI\.ant")
APPROVALS_FILE = ANT_DIR / "approvals.json"

def request_approval(action_text, timeout=300):
    """
    Pide autorizacion al usuario via el Bridge de Telegram.
    Bloquea la ejecucion hasta recibir respuesta o timeout.
    """
    req_id = str(uuid.uuid4())[:4]
    new_request = {
        "id": req_id,
        "action": action_text,
        "status": "waiting_user",
        "created_at": time.time()
    }
    
    # Asegurar carpeta
    ANT_DIR.mkdir(exist_ok=True)
    
    # Cargar y agregar
    if not APPROVALS_FILE.exists():
        with open(APPROVALS_FILE, 'w', encoding='utf-8') as f: json.dump([], f)
        
    try:
        with open(APPROVALS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[DEBUG] Error cargando JSON: {e}")
        data = []
    
    data.append(new_request)
    
    with open(APPROVALS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"[AUTH] Solicitud enviada (ID: {req_id}). Revisa Telegram.")
    
    # Loop de espera
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with open(APPROVALS_FILE, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
                for req in current_data:
                    if req["id"] == req_id:
                        if req["status"] == "approved":
                            print(f"[OK] Autorizado: {action_text}")
                            return True
                        if req["status"] == "rejected":
                            print(f"[ERROR] Denegado: {action_text}")
                            return False
        except Exception as e:
            # Si hay error de lectura (ej: archivo siendo escrito), reintentar silenciosamente
            pass
        time.sleep(2)
    
    print("[TIMEOUT] Sin respuesta del usuario.")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python remote_auth_hook.py 'accion'")
        sys.exit(1)
        
    action = sys.argv[1]
    if request_approval(action):
        sys.exit(0)
    else:
        sys.exit(1)

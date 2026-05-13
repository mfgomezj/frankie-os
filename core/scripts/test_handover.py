import os
from pathlib import Path
from handover_manager import HandoverManager

def test_handover_flow():
    print("Iniciando test del protocolo de Handover...")
    project_path = r"d:\Proyectos\PROYECTO_FUNNELSFOUNDRY.AI"
    
    manager = HandoverManager(project_path)
    
    # 1. Simular captura de snapshot
    snap = manager.capture_snapshot(
        change_name="test-handover-flow",
        phase="testing",
        next_task="Verificar que el polling responda a la aprobación de Telegram."
    )
    print("Snapshot capturado:", snap)
    
    # 2. Registrar en Notion (opcional en test local, pero verifica conexión)
    print("\n[Log a Notion]")
    manager.log_to_notion(snap, status="Test")
    
    # 3. Guardar en approvals.json (simulando lo que hace el bridge o el script que requiere aprobación)
    import json
    import uuid
    approvals_file = Path(project_path) / ".ant" / "approvals.json"
    
    # Asegurar el directorio
    approvals_file.parent.mkdir(parents=True, exist_ok=True)
    
    action_id = str(uuid.uuid4().hex)[:4]
    
    approvals = []
    if approvals_file.exists():
        try:
            with open(approvals_file, "r", encoding="utf-8") as f:
                approvals = json.load(f)
        except json.JSONDecodeError:
            pass
            
    approvals.append({
        "id": action_id,
        "action": "test_handover_approval",
        "status": "pending",
        "description": "Test de aprobación interactiva vía Telegram",
        "timestamp": snap["timestamp"]
    })
    
    with open(approvals_file, "w", encoding="utf-8") as f:
        json.dump(approvals, f, indent=2)
        
    print(f"\nAcción {action_id} agregada a approvals.json con estado 'pending'.")
    print("El puente de Telegram (si está corriendo) debería leerlo y notificarte en breve.")
    
    # 4. Iniciar espera activa (Polling)
    print("\nIniciando polling...")
    # Timeout corto de 5 minutos para el test
    is_approved = manager.wait_for_approval(action_id, timeout_mins=5)
    
    if is_approved:
        print("\n✅ ¡ÉXITO! La acción fue aprobada a través de Telegram.")
    else:
        print("\n❌ ¡FALLO o TIMEOUT! La acción fue rechazada o el tiempo se agotó.")

if __name__ == "__main__":
    test_handover_flow()

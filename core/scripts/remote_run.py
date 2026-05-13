import sys
import subprocess
from pathlib import Path

# Importamos la lógica de autorización remota existente
sys.path.append(str(Path(__file__).parent))
import remote_auth_hook

def main():
    if len(sys.argv) < 2:
        print("Uso: python remote_run.py 'comando a ejecutar'")
        sys.exit(1)

    command = sys.argv[1]
    
    # Pedir autorización vía Telegram
    print(f"[*] Solicitando autorización remota para: {command}")
    if remote_auth_hook.request_approval(f"Ejecutar comando: {command}"):
        print(f"[*] Autorizado. Ejecutando...")
        try:
            # Ejecutar el comando y capturar salida
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"Error: {result.stderr}", file=sys.stderr)
            sys.exit(result.returncode)
        except Exception as e:
            print(f"Excepción durante la ejecución: {e}")
            sys.exit(1)
    else:
        print("[!] Ejecución rechazada por el usuario en Telegram.")
        sys.exit(1)

if __name__ == "__main__":
    main()

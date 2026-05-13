import os
import shutil
import sys
import io
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output for Windows consoles
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

# Config
BANK_ROOT = Path("D:/BANK")
ONEDRIVE_ROOT = Path(r"C:\Users\AIdev\OneDrive\Documentos\jobnearme.online\BANK_CLOUD")

def sync_bank():
    print(f"🚀 Iniciando Sincronización de Banco: {BANK_ROOT} -> {ONEDRIVE_ROOT}")
    
    if not BANK_ROOT.exists():
        print(f"❌ Error: El banco local {BANK_ROOT} no existe.")
        return

    if not ONEDRIVE_ROOT.exists():
        print(f"📂 Creando carpeta de destino en OneDrive: {ONEDRIVE_ROOT}")
        ONEDRIVE_ROOT.mkdir(parents=True, exist_ok=True)

    # Recorrer el banco buscando carpetas de proyectos
    for project_folder in BANK_ROOT.iterdir():
        if project_folder.is_dir():
            for category_folder in project_folder.iterdir():
                if category_folder.is_dir():
                    for slug_folder in category_folder.iterdir():
                        if slug_folder.is_dir():
                            # Solo sincronizamos si hay una carpeta 'processed'
                            processed_path = slug_folder / "processed"
                            if processed_path.exists():
                                relative_path = slug_folder.relative_to(BANK_ROOT)
                                dest_path = ONEDRIVE_ROOT / relative_path
                                
                                print(f"📦 Sincronizando {relative_path}...")
                                # Usamos copytree con dirs_exist_ok para actualizar
                                shutil.copytree(slug_folder, dest_path, dirs_exist_ok=True)
                                print(f"   ✅ OK")

    print("=" * 60)
    print("✅ Sincronización con OneDrive completada.")
    print("=" * 60)

if __name__ == "__main__":
    sync_bank()

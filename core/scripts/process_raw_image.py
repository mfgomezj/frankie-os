import os
import argparse
import requests
from pathlib import Path
from PIL import Image, ImageOps
from dotenv import load_dotenv

load_dotenv()

# =====================================================================
# TRAFFICKER IMAGE PROCESSOR (JobNearMe) - BANK ARCHITECTURE
# =====================================================================
# Estructura: D:/BANK/{Project}/{Category}/{Slug}/raw/ -> /processed/
# Procesa la tríada visual (hero, twist_a, twist_b) y genera WebP optimizados.
# NO ELIMINA LOS ORIGINALES. El banco es sagrado.

TARGET_WIDTH = 1200
TARGET_HEIGHT = 630
BACKGROUND_COLOR = "#0A2540" 

ASSETS_BANK_ROOT = Path(os.getenv("ASSETS_BANK_ROOT", "D:/BANK"))
NOTION_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def process_image(src_path: Path, output_path: Path):
    """Procesamiento quirúrgico de imagen para SEO."""
    try:
        with Image.open(src_path) as img:
            img = img.convert("RGBA")
            canvas = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), BACKGROUND_COLOR)
            img_resized = ImageOps.fit(img, (TARGET_WIDTH, TARGET_HEIGHT), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            canvas.paste(img_resized, (0, 0), img_resized)
            canvas.convert("RGB").save(output_path, format="WEBP", quality=85, method=6)
        return True
    except Exception as e:
        print(f"Error procesando {src_path.name}: {e}")
        return False

def find_notion_page(slug: str):
    """Busca el ID de la página en Notion usando el slug."""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    payload = {
        "filter": {
            "property": "Slug",
            "rich_text": { "equals": slug }
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            results = response.json().get("results", [])
            return results[0]["id"] if results else None
    except Exception as e:
        print(f"Error buscando página en Notion: {e}")
    return None

def update_notion_assets(page_id: str, assets: dict, base_path: Path):
    """Actualiza los links de los assets y el status en Notion."""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    
    properties = {}
    # Mapeo según el esquema real detectado
    mapping = {
        "hero": "Hero Image Link",
        "twist_a": "Twist A Image Link",
        "twist_b": "Twist B Image Link"
    }

    for key, path in assets.items():
        if key in mapping:
            # Intentamos usar file:// para rutas locales, aunque Notion puede ser estricto con URLs
            properties[mapping[key]] = {
                "url": f"file:///{str(path).replace('\\', '/')}"
            }

    # Guardamos el path local de la carpeta en 'Local Path'
    properties["Local Path"] = {
        "rich_text": [{ "text": { "content": str(base_path) } }]
    }

    # Si procesamos toda la tríada, marcamos como listo
    if len(assets) >= 3:
        properties["Status"] = { "select": { "name": "Ready for n8n" } }

    if not properties:
        return

    try:
        response = requests.patch(url, headers=headers, json={"properties": properties})
        if response.status_code == 200:
            print(f"   [NOTION] Sincronización exitosa (Assets + Status).")
        else:
            print(f"   [NOTION] Error en sincronización: {response.status_code} - {response.text}")
            # Si falló por las URLs, intentamos solo con el Local Path y Status
            if response.status_code == 400:
                print(f"   [NOTION] Reintentando sin campos 'url' por posible restricción de protocolo...")
                lite_props = { k: v for k, v in properties.items() if not k.endswith("Link") }
                requests.patch(url, headers=headers, json={"properties": lite_props})
    except Exception as e:
        print(f"   [NOTION] Error de conexión: {e}")

def run_pipeline(project: str, category: str, slug: str):
    # Definir rutas según el estándar de autoridad
    base_folder = ASSETS_BANK_ROOT / project / category / slug
    raw_folder = base_folder / "raw"
    processed_folder = base_folder / "processed"
    
    processed_folder.mkdir(parents=True, exist_ok=True)
    
    if not raw_folder.exists():
        print(f"ERROR: No existe la carpeta de origen -> {raw_folder}")
        return

    print(f"--- Iniciando Procesamiento de Tríada Visual: {slug} ---")
    
    # Buscamos archivos que sigan el patrón: hero.*, twist_a.*, twist_b.*
    triad_patterns = ["hero", "twist_a", "twist_b"]
    processed_assets = {}

    for pattern in triad_patterns:
        # Buscamos cualquier extensión común
        matches = list(raw_folder.glob(f"{pattern}.*"))
        if matches:
            src = matches[0]
            dest = processed_folder / f"{pattern}.webp"
            print(f"Procesando {pattern}...")
            if process_image(src, dest):
                print(f"   [OK] Generado: {dest}")
                processed_assets[pattern] = dest
    
    if not processed_assets:
        print(f"AVISO: No se encontraron archivos de tríada (hero, twist_a, twist_b) en {raw_folder}")
    else:
        # Sincronización con Notion
        page_id = find_notion_page(slug)
        if page_id:
            update_notion_assets(page_id, processed_assets, base_folder)
        else:
            print(f"AVISO: No se encontró la página con slug '{slug}' en Notion. No se pudieron subir los links.")
        
        print(f"--- Pipeline Finalizado para {slug} ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trafficker Asset Processor")
    parser.add_argument("--project", default="jobnearme", help="Nombre del proyecto")
    parser.add_argument("--category", default="general", help="Categoría (industria/estado)")
    parser.add_argument("--slug", required=True, help="Slug del contenido")
    
    args = parser.parse_args()
    run_pipeline(args.project, args.category, args.slug)

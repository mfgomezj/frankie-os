#!/usr/bin/env python3
"""
Script para mover archivos LA3+ a la carpeta sincronizada de OneDrive.
Incluye validación de frontmatter antes de mover.

Uso: python move_to_onedrive.py

Autor: GitHub Copilot
Fecha: 2026-04-30
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime

# ==================== CONFIGURACIÓN ====================
# Carpeta de origen (donde se generan los LA3+)
SOURCE_FOLDER = r"D:\Proyectos\PROYECTO_FUNNELSFOUNDRY.AI\PORTFOLIO_01_JOBNEARME\JERARQUIA_CONTENIDO\LA3"

# Carpeta de destino (carpeta sincronizada de OneDrive)
DEST_FOLDER = r"C:\Users\AIdev\OneDrive\Documentos\jobnearme.online\LAx"

# Extensiones de archivos a mover
EXTENSIONS = [".md", ".webp", ".png", ".jpg", "_prompt.md"]

# Campos obligatorios del frontmatter
REQUIRED_FRONTMATTER_FIELDS = ["slug", "seo_title", "meta_description", "focus_keyword"]
# ==================== FIN CONFIGURACIÓN ====================


def parse_frontmatter(file_path):
    """Extrae y valida el frontmatter de un archivo markdown."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si tiene frontmatter
        if not content.startswith('---'):
            return None, "Sin frontmatter"
        
        # Extraer bloque frontmatter
        parts = content.split('---')
        if len(parts) < 3:
            return None, "Frontmatter malformado"
        
        frontmatter_block = parts[1]
        
        # Parsear campos
        fields = {}
        for line in frontmatter_block.strip().split('\n'):
            line = line.strip()
            if ':' in line:
                key = line.split(':')[0].strip()
                value = ':'.join(line.split(':')[1:]).strip()
                # Limpiar valores entre comillas
                value = value.strip('"').strip("'")
                fields[key] = value
        
        return fields, None
    except Exception as e:
        return None, str(e)


def validate_frontmatter(folder_path):
    """Valida que el frontmatter tenga los campos obligatorios."""
    folder = Path(folder_path)
    
    # Buscar el archivo .md principal
    md_file = None
    for file in folder.iterdir():
        if file.suffix == ".md" and not file.name.endswith("_prompt.md"):
            md_file = file
            break
    
    if not md_file:
        return False, "No se encontró archivo .md"
    
    # Parsear frontmatter
    fields, error = parse_frontmatter(md_file)
    
    if error:
        return False, error
    
    # Verificar campos obligatorios
    missing_fields = []
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in fields or not fields[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Campos faltantes: {', '.join(missing_fields)}"
    
    # Verificar que el nombre del archivo coincida con el slug
    expected_filename = f"{fields['slug']}.md"
    if md_file.name != expected_filename:
        return False, f"Slug mismatch: archivo '{md_file.name}' vs slug '{fields['slug']}.md'"
    
    return True, "OK"
def get_subfolders(base_path):
    """Obtiene todas las subcarpetas que contienen archivos listos."""
    subfolders = []
    base = Path(base_path)
    
    if not base.exists():
        print(f"❌ La carpeta de origen no existe: {base_path}")
        return []
    
    for item in base.iterdir():
        if item.is_dir():
            subfolders.append(item)
    
    return subfolders


def has_required_files(folder_path):
    """Verifica si la carpeta tiene los archivos mínimos requeridos."""
    folder = Path(folder_path)
    md_file = None
    webp_file = None
    
    for file in folder.iterdir():
        if file.suffix == ".md" and not file.name.endswith("_prompt.md"):
            md_file = file
        elif file.suffix == ".webp":
            webp_file = file
    
    return md_file is not None


def move_folder_contents(source_folder, dest_base):
    """Mueve todos los archivos de una carpeta al destino."""
    source = Path(source_folder)
    folder_name = source.name
    dest = Path(dest_base) / folder_name
    
    # Crear carpeta de destino si no existe
    dest.mkdir(parents=True, exist_ok=True)
    
    moved_files = []
    
    # Mover todos los archivos relevantes
    for file in source.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            # Mover solo archivos relevantes (md, webp, prompt)
            if ext in EXTENSIONS or "_prompt.md" in file.name:
                dest_file = dest / file.name
                # Si ya existe, renombrar
                if dest_file.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_name = f"{file.stem}_{timestamp}{file.suffix}"
                    dest_file = dest / new_name
                
                shutil.move(str(file), str(dest_file))
                moved_files.append(file.name)
                print(f"  OK {file.name} to {dest}")
    
    return moved_files


def main():
    print("=" * 60)
    print("MOVEDOR DE ARCHIVOS A ONEDRIVE")
    print("=" * 60)
    print(f"Origen:    {SOURCE_FOLDER}")
    print(f"Destino:   {DEST_FOLDER}")
    print("-" * 60)
    
    # Verificar que las carpetas existen
    if not Path(SOURCE_FOLDER).exists():
        print(f"Error: La carpeta de origen no existe.")
        return
    
    if not Path(DEST_FOLDER).exists():
        print(f"Error: La carpeta de destino no existe.")
        print(f"   Verifica que OneDrive esté sincronizando: {DEST_FOLDER}")
        return
    
    # Obtener subcarpetas (cada LA3 es una carpeta)
    subfolders = get_subfolders(SOURCE_FOLDER)
    
    if not subfolders:
        print("No se encontraron carpetas LA3 para mover.")
        return
    
    print(f"Se encontraron {len(subfolders)} carpetas LA3.\n")
    
    total_moved = 0
    
    for folder in subfolders:
        print(f"Procesando: {folder.name}")
        
        if has_required_files(folder):
            files = move_folder_contents(folder, DEST_FOLDER)
            if files:
                print(f"  OK {len(files)} archivos movidos")
                total_moved += len(files)
            else:
                print(f"  Aviso: No se movieron archivos (puede que ya estén vacíos)")
        else:
            print(f"  Omitiendo: Carpeta incompleta (falta .md o .webp), se omite")
    
    print("-" * 60)
    print(f"Proceso completado. Total de archivos movidos: {total_moved}")
    print("=" * 60)


if __name__ == "__main__":
    main()
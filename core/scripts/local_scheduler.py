import os
import json
import re
import argparse
import logging
import time
import requests
import yaml
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Config
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def load_env_vars(project_root: Path = None):
    # 1. Try project root if provided
    if project_root:
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file, override=True)
            logger.info(f"Loaded environment from Project Root: {env_file}")
            return

    # 2. Try CWD
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        load_dotenv(cwd_env, override=True)
        logger.info(f"Loaded environment from CWD: {cwd_env.name}")
        return
    
    # 3. Try script location as fallback
    base_dir = Path(__file__).resolve().parent.parent
    script_env = base_dir / ".env"
    if script_env.exists():
        load_dotenv(script_env, override=True)
        logger.info(f"Loaded environment from Script Location: {script_env.name}")
        return
        
    load_dotenv()
    logger.info("Loaded environment using default search.")

def load_project_config() -> dict:
    config_path = Path.cwd() / "project_config.yaml"
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logger.info(f"Loaded project configuration from: {config_path}")
                return config
        except Exception as e:
            logger.error(f"Failed to load project_config.yaml: {e}")
    return {}

def send_telegram_status(text: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_HOME_CHANNEL") or os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            logger.error(f"Failed to send TG notification: {e}")

def load_state(state_file: Path) -> set:
    if state_file.exists():
        with open(state_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return set(data.get("processed_keywords", []))
            except json.JSONDecodeError:
                return set()
    return set()

def save_state(state_file: Path, processed: set):
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump({"processed_keywords": list(processed)}, f, indent=4)

def parse_keywords(source_file: Path):
    if not source_file.exists():
        return []
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split("--------------------")
    parsed_data = []

    for block in blocks:
        keyword_match = re.search(r'Keyword:\s*(.+)', block)
        comp_match = re.search(r'Competition:.*\(Index:\s*([\d.]+)\)', block)
        bids_match = re.search(r'Bids \(COP\):\s*(.+)', block)
        
        if keyword_match and comp_match and bids_match:
            parsed_data.append({
                "keyword": keyword_match.group(1).strip(),
                "competition_index": float(comp_match.group(1).strip()),
                "bids_cop": bids_match.group(1).strip()
            })
            
    return parsed_data

def generate_payloads(selected_items: list, output_dir: Path, project_id: str = "frankie"):
    output_dir.mkdir(parents=True, exist_ok=True)
    for item in selected_items:
        keyword = item["keyword"]
        slug = keyword.replace(" ", "-").lower()
        
        payload = {
            "title": f"Guía Maestra: {keyword.title()} 2026",
            "slug": slug,
            "focus_keyword": keyword,
            "status": "ideation",
            "project_id": project_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "competition_index": item["competition_index"],
            "image_path": f"{slug}.webp",
            "visual_triad": {
                "hero": { "prompt": f"Professional workspace focusing on {keyword}, 8k cinematic." }
            }
        }

        content = f"""---
{yaml.dump(payload, sort_keys=False)}
---

# {payload['title']}

## Introducción
Dominar **{keyword.title()}** es la clave para la libertad digital en 2026. 

[Contenido generado automáticamente por {project_id.replace('-', ' ').title()}]
"""
        
        outfile = output_dir / f"{slug}.md"
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Markdown payload generated: {outfile}")

def run_iteration(args, project_config: dict):
    source_path = Path(args.source)
    state_path = Path(args.state)
    out_dir = Path(args.outdir)
    project_id = project_config.get("project_id", "frankie")
    
    if not source_path.exists():
        logger.error(f"Source file not found: {source_path}")
        return False

    processed_keywords = load_state(state_path)
    all_keywords = parse_keywords(source_path)
    
    available_keywords = [k for k in all_keywords if k["keyword"] not in processed_keywords]
    logger.info(f"Iteration [{project_id}]: {len(available_keywords)} fresh keywords found.")
    
    if not available_keywords:
        return False
        
    selected = available_keywords[:args.quota]
    generate_payloads(selected, out_dir, project_id)
    
    for item in selected:
        processed_keywords.add(item["keyword"])
    save_state(state_path, processed_keywords)
    
    send_telegram_status(f"✅ *Scheduler [{project_id}]:* Procesadas {len(selected)} nuevas keywords.\nFocus: `{selected[0]['keyword']}`")
    return True

def main():
    parser = argparse.ArgumentParser(description="Local Content Scheduler for Frankie OS")
    
    # Load config from CWD
    config = load_project_config()
    load_env_vars(project_root=Path.cwd())
    
    script_base = Path(__file__).resolve().parent.parent
    
    # Resolve Paths via Config or Defaults
    paths_config = config.get("paths", {})
    
    # 1. Source (Keywords)
    default_source = paths_config.get("source_keywords")
    if not default_source:
        # Fallback to old structure if not in config
        default_source = script_base / "PORTFOLIO_01_JOBNEARME" / "Jobnearme_SEO_Keywords_NotebookSource.md"
    else:
        default_source = Path.cwd() / default_source

    # 2. State
    default_state = paths_config.get("state_file")
    if not default_state:
        default_state = Path(__file__).resolve().parent / "state.json"
    else:
        default_state = Path.cwd() / default_state

    # 3. Output (Inbox)
    default_outdir = paths_config.get("inbox_path")
    if not default_outdir:
        default_outdir = os.getenv("ONEDRIVE_INBOX_PATH", "OneDrive_Inbox")
    
    parser.add_argument("--source", type=str, default=str(default_source))
    parser.add_argument("--state", type=str, default=str(default_state))
    parser.add_argument("--outdir", type=str, default=str(default_outdir))
    parser.add_argument("--quota", type=int, default=1)
    parser.add_argument("--interval", type=int, default=300) # 5 minutos
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    
    args = parser.parse_args()
    project_id = config.get("project_id", "frankie-os")
    
    try:
        if args.once:
            logger.info(f"Starting single iteration for project: {project_id}")
            run_iteration(args, config)
        else:
            send_telegram_status(f"🚀 *Scheduler [{project_id}]:* Iniciando modo 24/7 (Polling: {args.interval/60} min).")
            while True:
                logger.info(f"Starting polling iteration for project: {project_id}")
                run_iteration(args, config)
                time.sleep(args.interval)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
        if not args.once:
            send_telegram_status(f"🛑 *Scheduler [{project_id}]:* Detenido manualmente.")

if __name__ == "__main__":
    main()

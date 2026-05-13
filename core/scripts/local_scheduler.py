import os
import json
import re
import argparse
import logging
import time
import requests
from pathlib import Path
from datetime import datetime

# Config
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def load_env_vars(project_root: Path):
    from dotenv import load_dotenv
    env_role = os.getenv("TERMINAL_ENV", "local").lower()
    env_name = ".env.cloud" if env_role == "cloud" else ".env.pc"
    env_file = project_root / env_name
    
    if not env_file.exists():
        # Fallback al viejo
        env_file = project_root / ".env"
        
    load_dotenv(env_file, override=True)
    logger.info(f"Loaded environment: {env_file.name}")

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

def generate_payloads(selected_items: list, output_dir: Path):
    import yaml
    output_dir.mkdir(parents=True, exist_ok=True)
    for item in selected_items:
        keyword = item["keyword"]
        slug = keyword.replace(" ", "-").lower()
        
        payload = {
            "title": f"Guía Maestra: {keyword.title()} 2026",
            "slug": slug,
            "focus_keyword": keyword,
            "status": "ideation",
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

[Contenido generado automáticamente por Funnels Foundry AI]
"""
        
        outfile = output_dir / f"{slug}.md"
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Markdown payload generated: {outfile}")

def run_iteration(args):
    source_path = Path(args.source)
    state_path = Path(args.state)
    out_dir = Path(args.outdir)
    
    if not source_path.exists():
        logger.error(f"Source file not found: {source_path}")
        return False

    processed_keywords = load_state(state_path)
    all_keywords = parse_keywords(source_path)
    
    available_keywords = [k for k in all_keywords if k["keyword"] not in processed_keywords]
    logger.info(f"Iteration: {len(available_keywords)} fresh keywords found.")
    
    if not available_keywords:
        return False
        
    selected = available_keywords[:args.quota]
    generate_payloads(selected, out_dir)
    
    for item in selected:
        processed_keywords.add(item["keyword"])
    save_state(state_path, processed_keywords)
    
    send_telegram_status(f"✅ *Scheduler:* Procesadas {len(selected)} nuevas keywords.\nFocus: `{selected[0]['keyword']}`")
    return True

def main():
    parser = argparse.ArgumentParser(description="Local Content Scheduler for SEO Tactics")
    base_dir = Path(__file__).resolve().parent.parent
    load_env_vars(base_dir)
    
    default_source = base_dir / "PORTFOLIO_01_JOBNEARME" / "Jobnearme_SEO_Keywords_NotebookSource.md"
    default_state = Path(__file__).resolve().parent / "state.json"
    default_outdir = base_dir / "OneDrive_Inbox"
    
    parser.add_argument("--source", type=str, default=str(default_source))
    parser.add_argument("--state", type=str, default=str(default_state))
    parser.add_argument("--outdir", type=str, default=str(default_outdir))
    parser.add_argument("--quota", type=int, default=1)
    parser.add_argument("--interval", type=int, default=300) # 5 minutos
    
    args = parser.parse_args()
    
    send_telegram_status("🚀 *Scheduler Local:* Iniciando modo 24/7 (Polling: 5 min).")
    
    try:
        while True:
            logger.info("Starting polling iteration...")
            run_iteration(args)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user.")
        send_telegram_status("🛑 *Scheduler Local:* Detenido manualmente.")

if __name__ == "__main__":
    main()

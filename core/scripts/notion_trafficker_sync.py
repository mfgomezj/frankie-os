import os
import yaml
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

# Config
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def load_environment(project_root: Path = None):
    # 1. Try project root if provided
    if project_root:
        env_file = project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file, override=True)
            logger.info(f"Loaded environment from Project Root: {env_file}")
            return env_file

    # 2. Try CWD first
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        load_dotenv(cwd_env, override=True)
        return cwd_env
    
    # 3. Try script location as fallback
    script_env = Path(__file__).resolve().parent.parent / ".env"
    if script_env.exists():
        load_dotenv(script_env, override=True)
        return script_env
    
    load_dotenv()
    return None

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

def extract_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    parts = content.split("---")
    if len(parts) >= 3:
        try:
            return yaml.safe_load(parts[1])
        except Exception as e:
            logger.error(f"Error parsing YAML in {file_path}: {e}")
            return None
    return None

def find_notion_page(slug, database_id, headers):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {
        "filter": {
            "property": "Slug",
            "rich_text": { "equals": slug }
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            results = response.json().get("results", [])
            return results[0]["id"] if results else None
        else:
            logger.error(f"Query Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return None

def sync_to_notion(data, database_id, headers):
    slug = data.get("slug")
    if not slug:
        fallback = data.get("focus_keyword") or data.get("title")
        if fallback:
            slug = fallback.lower().replace(" ", "-").replace(":", "").replace("?", "")
            logger.warning(f"Slug missing. Generated auto-slug: {slug}")
        else:
            logger.error("No slug, focus_keyword, or title found in metadata.")
            return

    page_id = find_notion_page(slug, database_id, headers)
    
    status_map = {
        "ideation": "Ideation",
        "writing": "Writing",
        "visuals_pending": "Visuals Pending",
        "ready": "Ready for n8n",
        "🚀 Publish: WordPress": "🚀 Publish: WordPress",
        "📱 Publish: Facebook": "📱 Publish: Facebook",
        "🎞️ Publish: Shorts": "🎞️ Publish: Shorts",
        "published": "✅ Published"
    }
    status_name = status_map.get(data.get("status", "ideation"), "Ideation")

    properties = {
        "Nombre": { "title": [{ "text": { "content": data.get("title_a", data.get("focus_keyword", slug)) } }] },
        "Slug": { "rich_text": [{ "text": { "content": slug } }] },
        "Title B": { "rich_text": [{ "text": { "content": data.get("title_b", "") } }] },
        "Title C": { "rich_text": [{ "text": { "content": data.get("title_c", "") } }] },
        "Focus Keyword": { "rich_text": [{ "text": { "content": data.get("focus_keyword", "") } }] },
        "Status": { "select": { "name": status_name } },
        "Hero Prompt": { "rich_text": [{ "text": { "content": data.get("visual_triad", {}).get("hero", {}).get("prompt", "") } }] },
        "Twist A Prompt": { "rich_text": [{ "text": { "content": data.get("visual_triad", {}).get("twist_a", {}).get("prompt", "") } }] },
        "Twist B Prompt": { "rich_text": [{ "text": { "content": data.get("visual_triad", {}).get("twist_b", {}).get("prompt", "") } }] },
        "Short A Script": { "rich_text": [{ "text": { "content": data.get("derivatives", {}).get("short_a", {}).get("script", "") } }] },
        "Short B Script": { "rich_text": [{ "text": { "content": data.get("derivatives", {}).get("short_b", {}).get("script", "") } }] },
        "YouTube Script": { "rich_text": [{ "text": { "content": data.get("derivatives", {}).get("youtube", {}).get("script_long", "") } }] },
    }

    if page_id:
        url = f"https://api.notion.com/v1/pages/{page_id}"
        response = requests.patch(url, headers=headers, json={"properties": properties})
        if response.status_code == 200:
            logger.info(f"Updated Notion page: {page_id} for slug: {slug}")
        else:
            logger.error(f"FAILED to update: {response.status_code} - {response.text}")
    else:
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": { "database_id": database_id },
            "properties": properties
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            new_id = response.json().get("id")
            logger.info(f"Created new Notion page: {new_id} for slug: {slug}")
        else:
            logger.error(f"FAILED to create: {response.status_code} - {response.text}")

def main():
    # 1. Load context
    config = load_project_config()
    load_environment(project_root=Path.cwd())
    
    # 2. Resolve Notion Config
    notion_token = os.getenv("NOTION_API_KEY", "").strip()
    # Prioritize config over environment
    database_id = config.get("integrations", {}).get("notion", {}).get("database_id")
    if not database_id:
        database_id = os.getenv("NOTION_DATABASE_ID", "").strip()

    if not notion_token or not database_id:
        logger.critical("NOTION_API_KEY or DATABASE_ID not found in config or env.")
        return

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    # 3. Resolve Inbox Path
    inbox_path = config.get("paths", {}).get("inbox_path")
    if not inbox_path:
        inbox_path = os.getenv("ONEDRIVE_INBOX_PATH", "OneDrive_Inbox")
    
    inbox_path = Path.cwd() / inbox_path
    
    if not inbox_path.exists():
        logger.error(f"Inbox path does not exist: {inbox_path}")
        return

    # 4. Sync
    md_files = list(inbox_path.glob("*.md"))
    if not md_files:
        logger.info("No .md files found in inbox.")
        return

    project_id = config.get("project_id", "frankie-os")
    logger.info(f"Starting Notion Sync for project: {project_id}")

    for md_file in md_files:
        logger.info(f"Processing: {md_file.name}")
        data = extract_frontmatter(md_file)
        if data:
            sync_to_notion(data, database_id, headers)
        else:
            logger.warning(f"Skipping {md_file.name}: No frontmatter found.")

if __name__ == "__main__":
    main()

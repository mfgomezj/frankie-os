import os
import yaml
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def extract_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    parts = content.split("---")
    if len(parts) >= 3:
        try:
            return yaml.safe_load(parts[1])
        except Exception as e:
            print(f"Error parsing YAML in {file_path}: {e}")
            return None
    return None

def find_notion_page(slug):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Slug",
            "rich_text": { "equals": slug }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        results = response.json().get("results", [])
        return results[0]["id"] if results else None
    else:
        print(f"Query Error: {response.status_code} - {response.text}")
        return None

def sync_to_notion(data):
    slug = data.get("slug")
    if not slug:
        print("No slug found in metadata.")
        return

    page_id = find_notion_page(slug)
    
    # Map status to valid Notion options
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
        # Update
        url = f"https://api.notion.com/v1/pages/{page_id}"
        response = requests.patch(url, headers=headers, json={"properties": properties})
        if response.status_code == 200:
            print(f"SUCCESS: Updated Notion page: {page_id} for slug: {slug}")
        else:
            print(f"FAILED to update: {response.status_code} - {response.text}")
    else:
        # Create
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": { "database_id": DATABASE_ID },
            "properties": properties
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            new_id = response.json().get("id")
            print(f"SUCCESS: Created new Notion page: {new_id} for slug: {slug}")
        else:
            print(f"FAILED to create: {response.status_code} - {response.text}")

def main():
    # Use absolute path for safety
    base_dir = Path(__file__).resolve().parent.parent
    inbox_path = base_dir / os.getenv("ONEDRIVE_INBOX_PATH", "OneDrive_Inbox")
    
    if not inbox_path.exists():
        print(f"Inbox path does not exist: {inbox_path}")
        return

    md_files = list(inbox_path.glob("*.md"))
    if not md_files:
        print("No .md files found in inbox.")
        return

    for md_file in md_files:
        print(f"--- Processing {md_file.name} ---")
        data = extract_frontmatter(md_file)
        if data:
            sync_to_notion(data)
        else:
            print(f"Skipping {md_file.name}: No frontmatter found.")

if __name__ == "__main__":
    main()

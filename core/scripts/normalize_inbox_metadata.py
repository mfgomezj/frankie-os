import os
import re
import yaml
from pathlib import Path

def normalize_file(file_path: Path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        print(f"Skipping {file_path.name}: No frontmatter found.")
        return

    yaml_text = match.group(1)
    body = match.group(2)

    try:
        data = yaml.safe_load(yaml_text)
    except Exception as e:
        print(f"Error parsing YAML in {file_path.name}: {e}")
        return

    slug = data.get('slug') or file_path.stem
    
    # Title resolution
    title = data.get('title') or data.get('title_a') or slug.replace('-', ' ').title()
    
    # Mandatory Fields
    normalized = {
        'title': title,
        'slug': slug,
        'seo_title': data.get('seo_title') or f"{title} | JobNearMe",
        'meta_description': data.get('meta_description') or f"Explore the latest {title} opportunities in 2026. Find salaries, requirements and top companies.",
        'focus_keyword': data.get('focus_keyword') or slug.replace('-', ' '),
        'canonical_url': data.get('canonical_url') or f"https://jobnearme.online/{slug}/",
        'excerpt': data.get('excerpt') or f"Looking for {title}? Our 2026 guide covers everything you need to know about starting your career here.",
        'status': 'draft',
        'category_ids': str(data.get('category_ids') or "2").replace('[', '').replace(']', '').replace(' ', ''),
        'tag_ids': str(data.get('tag_ids') or "1,2").replace('[', '').replace(']', '').replace(' ', '')
    }

    # Keep extra fields if needed (project, bids, etc.)
    for key in ['project', 'competition_index', 'bids_cop', 'visual_triad', 'derivatives']:
        if key in data:
            normalized[key] = data[key]

    # Reconstruct file
    # Use a custom representer to avoid annoying !!python tags if any
    new_yaml = yaml.dump(normalized, allow_unicode=True, sort_keys=False, default_flow_style=False)
    
    new_content = f"---\n{new_yaml}---\n{body}"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Normalized {file_path.name}")

def main():
    inbox_dir = Path("OneDrive_Inbox")
    if not inbox_dir.exists():
        print("OneDrive_Inbox directory not found.")
        return

    for file in inbox_dir.glob("*.md"):
        normalize_file(file)

if __name__ == "__main__":
    main()

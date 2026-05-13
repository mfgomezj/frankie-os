import pytest
import yaml
from pathlib import Path
from GLOBAL_SCRIPTS.local_scheduler import generate_payloads

def test_generate_payloads_includes_image_path(tmp_path):
    # Setup
    selected_items = [
        {"keyword": "digital trafficker", "competition_index": 0.8, "bids_cop": "5000"}
    ]
    output_dir = tmp_path / "output"
    
    # Execute
    generate_payloads(selected_items, output_dir)
    
    # Verify
    md_files = list(output_dir.glob("*.md"))
    assert len(md_files) == 1
    
    content = md_files[0].read_text(encoding="utf-8")
    # Split frontmatter
    parts = content.split("---")
    assert len(parts) >= 3
    
    frontmatter = yaml.safe_load(parts[1])
    assert "image_path" in frontmatter
    assert frontmatter["image_path"] == "images/digital-trafficker.png"

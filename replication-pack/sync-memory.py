import os
import sys
import argparse
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load configuration from .env
load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
VAULT_FILE = "memory_vault.md"

def get_connection():
    try:
        return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def export_memory():
    print(f"Exporting memory to {VAULT_FILE}...")
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Fetch all observations
        cur.execute("SELECT title, content, type, project, topic_key FROM observations ORDER BY created_at DESC")
        rows = cur.fetchall()
        
        with open(VAULT_FILE, "w", encoding="utf-8") as f:
            f.write(f"# Engram Memory Vault\n")
            f.write(f"Generated on: {psycopg2.TimestampNow()}\n\n")
            
            for row in rows:
                f.write(f"---\n")
                f.write(f"title: {row['title']}\n")
                f.write(f"type: {row['type']}\n")
                f.write(f"project: {row['project']}\n")
                f.write(f"topic_key: {row['topic_key']}\n")
                f.write(f"---\n\n")
                f.write(f"{row['content']}\n\n")
                f.write(f"<!-- observation-end -->\n\n")
                
        print(f"Successfully exported {len(rows)} observations.")
    except Exception as e:
        print(f"Export failed: {e}")
    finally:
        cur.close()
        conn.close()

def import_memory():
    if not os.path.exists(VAULT_FILE):
        print(f"Error: {VAULT_FILE} not found. Nothing to import.")
        return

    print(f"Importing memory from {VAULT_FILE}...")
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        conn.autocommit = True # Handle each insert independently
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Very simple parser for the custom MD format
        observations = content.split("<!-- observation-end -->")
        count = 0
        
        for obs in observations:
            if "---" not in obs:
                continue
                
            try:
                # Parse metadata
                parts = obs.split("---")
                if len(parts) < 3: continue
                meta_lines = parts[1].strip().split("\n")
                meta = {}
                for line in meta_lines:
                    if ":" in line:
                        key, val = line.split(":", 1)
                        meta[key.strip()] = val.strip()
                
                # Parse content
                obs_content = parts[2].strip()
                
                # Check if exists (topic_key or title)
                cur.execute("SELECT id FROM observations WHERE topic_key = %s OR (topic_key IS NULL AND title = %s)", 
                           (meta.get('topic_key'), meta.get('title')))
                
                if cur.fetchone():
                    continue
                
                # Insert new
                cur.execute(
                    "INSERT INTO observations (title, content, type, project, topic_key) VALUES (%s, %s, %s, %s, %s)",
                    (meta.get('title'), obs_content, meta.get('type'), meta.get('project'), meta.get('topic_key'))
                )
                count += 1
            except Exception as e:
                print(f"Error parsing observation '{meta.get('title')}': {e}")
                
        print(f"Successfully imported {count} new observations.")
    except Exception as e:
        print(f"Import failed: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Engram Hybrid Sync - Bridge your local and cloud memory.")
    parser.add_argument("--export", action="store_true", help="Export DB to Markdown vault")
    parser.add_argument("--import", action="store_true", dest="import_data", help="Import Markdown vault to DB")
    
    args = parser.parse_args()
    
    if args.export:
        export_memory()
    elif args.import_data:
        import_memory()
    else:
        parser.print_help()

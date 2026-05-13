# Technical Design: engram-hybrid-sync

## Overview
The `sync-memory.py` script acts as a data serializer between the PostgreSQL database and a Markdown-based "vault".

## Data Mapping
| Database Field | Markdown Element |
|----------------|------------------|
| `title`        | `### Title`      |
| `content`      | Block content    |
| `type`         | Meta: Type       |
| `project`      | Meta: Project    |
| `topic_key`    | Meta: Topic Key  |

## Implementation Details

### 1. Unique Identification
To avoid duplicates, the script will check if an observation with the same `topic_key` already exists in the destination database. If it exists, it will compare the `last_updated` timestamp or simply skip it to preserve the latest local version.

### 2. File Format
The `memory_vault.md` will use a simple, parseable structure:
```markdown
---
topic_key: sdd-init/hermes
project: hermes
type: architecture
---
### sdd-init/hermes
**What**: ...
**Why**: ...
...
<!-- observation-end -->
```

### 3. Dependencies
- `psycopg2-binary`: For DB interaction.
- `python-dotenv`: For loading `.env` configuration.
- `pyyaml`: (Optional) for parsing frontmatter if needed, or simple regex.

## Decisions & Tradeoffs
- **Decision**: Use Markdown instead of JSON.
- **Reason**: Markdown is easily reviewable in the GitHub UI and fits the "documentation as memory" philosophy of the project.
- **Tradeoff**: Parsing might be slightly more complex than JSON, but better for the user.

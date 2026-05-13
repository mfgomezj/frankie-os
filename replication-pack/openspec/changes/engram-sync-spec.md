# Specification: engram-hybrid-sync

## Requirements
- The sync system MUST allow exporting Engram observations to a Markdown file.
- The sync system MUST allow importing Engram observations from a Markdown file back into a PostgreSQL database.
- The system MUST prevent duplicate observations by using the `topic_key` or `title` as a unique identifier.
- The system MUST be compatible with both Windows (Local PC) and Linux (Droplet).
- The exported file SHOULD be formatted in a human-readable way so it can be reviewed in GitHub.

## Scenarios

### Scenario 1: Exporting memory from Local PC
- **Given** several observations in the local PostgreSQL.
- **When** the user runs `python sync-memory.py --export`.
- **Then** a file `memory_vault.md` is created/updated in the project root.
- **And** it contains all observations categorized by type and project.

### Scenario 2: Importing memory on the Droplet
- **Given** a `memory_vault.md` file pulled from GitHub.
- **When** the user runs `python sync-memory.py --import` on the Droplet.
- **Then** the script reads the file and inserts new observations into the local PostgreSQL.
- **And** existing observations (same topic_key) are updated or skipped to avoid clutter.

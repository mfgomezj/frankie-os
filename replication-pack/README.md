# Hermes AI - Persistence & Replication Pack
Developed for Funnels Foundry AI - MVP Agentic Infrastructure

## Overview
This pack provides a standardized, professional environment for deploying **Hermes AI (v0.13.0)** and **Engram (v1.15.10)** with full data persistence. It eliminates the "amnesia" problem by replacing volatile SQLite storage with a robust **PostgreSQL 15** infrastructure.

## Stack Versions
- **Gentle AI**: v1.26.5 (Clean White Label UI)
- **Engram**: v1.15.10
- **Hermes AI**: v0.13.0
- **Database**: PostgreSQL 15 (Alpine)

## Quick Start (One-Click Setup)
The `setup-hermes.sh` script automates the entire process:

1. **Clone/Copy** this folder to your server (Droplet) or Local Machine.
2. **Make the script executable**:
   ```bash
   chmod +x setup-hermes.sh
   ```
3. **Run the setup**:
   ```bash
   ./setup-hermes.sh
   ```

The script will:
- Check for Docker and Python dependencies.
- Bootstrap the PostgreSQL container.
- Create a Python Virtual Environment (`venv`).
- Configure the `.env` bridge.
- Verify connectivity.

## Directory Structure
- `docker-compose.yml`: Database orchestration.
- `setup-hermes.sh`: Main automation script.
- `.env.template`: Template for environment variables.
- `requirements.txt`: Python dependency list.
- `openspec/`: Full SDD documentation trail for the infrastructure.

## Persistence
All memory stored in Engram is persisted in the `postgres_data` Docker volume. This ensures your AI agents remember everything across server reboots and container restarts.

## Licensing & Commercial Use
This pack is designed as a commercializable MVP for Funnels Foundry AI. Ensure you maintain the version pins to guarantee the stability of the "White Label" UI and functionality.

## Tooling & MCP (WordPress)
Para habilitar la gestión de WordPress en el entorno replicado:
1. Instalar el servidor globalmente: `npm install -g claudeus-wp-mcp`.
2. Copiar el archivo `wp-sites.json` a la raíz del entorno.
3. Asegurarse de que `WP_SITES_PATH` en el `.env` apunte a dicho archivo.
4. El agente (Hermes/Antigravity) detectará automáticamente las 145 herramientas de gestión.

---
*Created by Antigravity AI for Funnels Foundry.*

# Specification: setup-hermes-automation

## Requirements
- The script MUST be idempotent (running it multiple times should not break the system).
- The script MUST verify that Docker and Docker Compose are installed before proceeding.
- The script MUST ensure PostgreSQL is up and reachable before configuring the Python environment.
- The script MUST create a `.env` file from a template if it does not exist.
- The script MUST install specific versions of Gentle AI, Engram, and Hermes AI.
- The script MUST configure the connection between Engram and PostgreSQL using a `DATABASE_URL`.

## Scenarios

### Scenario 1: First-time setup on a clean server
- **Given** a server with Docker installed but no containers running.
- **When** the user runs `./setup-hermes.sh`.
- **Then** the script starts the Postgres container.
- **And** it creates a Python virtual environment.
- **And** it installs all dependencies.
- **And** it generates a `.env` file with the correct database credentials.
- **And** it verifies the connection to the database.

### Scenario 2: Re-running the script after a server reboot
- **Given** a server that was just rebooted.
- **When** the user runs `./setup-hermes.sh`.
- **Then** the script ensures the Postgres container is running.
- **And** it skips creating the `venv` if it already exists.
- **And** it verifies the database connection is restored.
- **And** it updates any missing dependencies.

### Scenario 3: Missing dependencies (Docker not installed)
- **Given** a server without Docker.
- **When** the user runs `./setup-hermes.sh`.
- **Then** the script fails with a clear error message: "Docker is required but not installed."

### Scenario 4: Database connection failure
- **Given** the Postgres container fails to start.
- **When** the user runs `./setup-hermes.sh`.
- **Then** the script attempts to wait for a few seconds.
- **And** if it still fails, it reports a connection error and stops.

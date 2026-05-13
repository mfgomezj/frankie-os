# Technical Design: Hermes Automation & Persistence Bridge

## Architecture Overview
The system consists of two main layers:
1. **Infrastructure Layer (Docker)**: A persistent PostgreSQL 15 database instance managed by Docker Compose.
2. **Application Layer (Python)**: A virtual environment containing Hermes, Engram, and the bridge configuration.

```mermaid
graph TD
    User([User]) --> Script[setup-hermes.sh]
    Script --> Docker[Docker Compose]
    Docker --> Postgres[(PostgreSQL 15)]
    Script --> Venv[Python Venv]
    Venv --> App[Hermes + Engram]
    App --> Env[.env Configuration]
    Env --> Postgres
```

## Component Design

### 1. `setup-hermes.sh`
- **Logic**: A Bash script that uses standard POSIX commands.
- **Persistence Check**: Uses `pg_isready` (via `docker exec`) to ensure the DB is ready.
- **Environment Handling**: Uses `sed` or simple redirection to manage `.env` files.

### 2. The Persistence Bridge (Config)
The "bridge" is not a separate application, but a specific configuration pattern in the `.env` file:
```env
# Database Bridge Configuration
DATABASE_URL=postgresql://gentleman:hermes_secret_2026@localhost:5432/engram
ENGRAM_MODE=postgres
HERMES_VERSION=0.13.0
GENTLE_VERSION=1.26.5
```
This forces Engram to use the remote PostgreSQL instead of a local SQLite file.

### 3. Dependency Management
- **`requirements.txt`**: Pins versions to ensure stability.
  ```text
  engram-ai==1.15.10
  hermes-ai==0.13.0
  psycopg2-binary>=2.9.0
  ```

## Decisions & Tradeoffs

### Decision 1: Use `psycopg2-binary`
- **Reason**: Simplifies installation by providing pre-compiled wheels, avoiding the need for `libpq-dev` and a C compiler on the host machine.
- **Tradeoff**: Larger binary size, but much faster and more reliable setup.

### Decision 2: Local Volume for Postgres
- **Reason**: Using `postgres_data:/var/lib/postgresql/data` ensures data survives container removal/updates.
- **Tradeoff**: Requires host disk space, but that's expected for persistence.

### Decision 3: No Docker for Python App (yet)
- **Reason**: Keeping the Python app on the host (in a venv) allows for easier debugging and interaction with the local filesystem during this MVP phase.
- **Tradeoff**: Slightly less isolation than a full Dockerized app, but easier "Hybrid" sync.

## Security
- Credentials are kept in `.env` (not committed to git).
- Postgres port (5432) is mapped to localhost by default to prevent external access unless explicitly changed.

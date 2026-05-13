# Proposal: setup-hermes-automation

## Intent
Automate the deployment and persistence of the Hermes AI stack using a one-click Bash script and Dockerized PostgreSQL.

## Scope
- Create `setup-hermes.sh`.
- Create `.env.template`.
- Create `requirements.txt` with specific versions.
- Implement connection health check.

## Approach
1. Use `docker-compose` to manage the database.
2. Use a standard Python `venv` for the application layer.
3. Use environment variables to configure the bridge between the Python app and the database.
4. Add auto-restart logic to the script to ensure it can be run multiple times safely (idempotency).

## Rollback Plan
- If `setup-hermes.sh` fails, the script will offer to clean up the `venv` and stop the Docker containers.

## Affected Components
- Infrastructure (Docker Compose)
- Application Layer (Python/Hermes/Engram)
- Configuration (.env)

#!/bin/bash

# ==============================================================================
# setup-hermes.sh - One-Click Persistence Setup for Hermes AI Stack
# Version: 1.0.0
# License: MIT (Funnels Foundry AI)
# ==============================================================================

set -e # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}       HERMES AI INFRASTRUCTURE SETUP               ${NC}"
echo -e "${GREEN}====================================================${NC}"

# 1. Dependency Checks
echo -e "\n[1/5] Checking dependencies..."

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: docker is not installed.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: docker-compose is not installed.${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed.${NC}"
    exit 1
fi

echo -e "${GREEN}Dependencies OK.${NC}"

# 2. Environment Configuration
echo -e "\n[2/5] Configuring environment..."

if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env from template...${NC}"
    cp .env.template .env
    echo -e "${GREEN}.env created. Please review credentials if needed.${NC}"
else
    echo -e "Existing .env found. Skipping template copy."
fi

# 3. Database Bootstrap
echo -e "\n[3/5] Bootstrapping PostgreSQL via Docker Compose..."

# Determine docker compose command (v1 vs v2)
DOCKER_COMPOSE="docker compose"
if ! docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
fi

$DOCKER_COMPOSE up -d

echo -e "Waiting for database to be ready..."
MAX_RETRIES=30
COUNT=0
while ! docker exec engram-db pg_isready -U gentleman &> /dev/null; do
    sleep 2
    COUNT=$((COUNT + 1))
    if [ $COUNT -ge $MAX_RETRIES ]; then
        echo -e "${RED}Error: PostgreSQL failed to start in time.${NC}"
        exit 1
    fi
    echo -n "."
done

echo -e "\n${GREEN}PostgreSQL is ready.${NC}"

# 4. Python Environment Setup
echo -e "\n[4/5] Setting up Python Virtual Environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
else
    echo -e "Existing venv found. Updating dependencies."
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}Python environment setup completed.${NC}"

# 5. Bridge Verification
echo -e "\n[5/5] Verifying Persistence Bridge..."

cat <<EOF > verify_bridge.py
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

try:
    url = os.getenv("DATABASE_URL")
    print(f"Connecting to: {url.split('@')[1] if '@' in url else 'Postgres'}")
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute('SELECT version();')
    version = cur.fetchone()
    print(f"SUCCESS: Connected to PostgreSQL! Version: {version[0]}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"ERROR: Could not connect to database. {e}")
    exit(1)
EOF

python3 verify_bridge.py

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}====================================================${NC}"
    echo -e "${GREEN}   SETUP COMPLETE: HERMES IS NOW PERSISTENT!        ${NC}"
    echo -e "${GREEN}====================================================${NC}"
    echo -e "To start Hermes, run: source venv/bin/activate && hermes-ai"
    rm verify_bridge.py
else
    echo -e "${RED}Setup completed with verification errors.${NC}"
    exit 1
fi

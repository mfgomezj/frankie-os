#!/bin/bash
# cloud_install.sh
# Script de instalación de Frankie Cloud en DigitalOcean.
# 
# PREREQUISITO: Las variables de entorno deben estar cargadas en el shell
# antes de ejecutar este script. Ver: replication-pack/.env.template
# Ejemplo: source /root/.hermes/.env.bootstrap && bash cloud_install.sh

set -euo pipefail

export PATH="/root/.local/bin:$PATH"
cd /root/HERMES_INSTALL
uv sync
mkdir -p /root/.hermes

# Validar que las variables requeridas estén presentes
required_vars=(
  OPENROUTER_API_KEY
  TELEGRAM_BOT_TOKEN
  TELEGRAM_ALLOWED_USERS
  TELEGRAM_HOME_CHANNEL
  TELEGRAM_HOME_CHANNEL_NAME
  NOTION_ACCESS_TOKEN
  N8N_URL
  N8N_API_KEY
  DEFAULT_MODEL
  LLM_PROVIDER
)

for var in "${required_vars[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    echo "ERROR: Variable '$var' no está definida. Revisar .env.bootstrap." >&2
    exit 1
  fi
done

cat > /root/.hermes/.env << EOF
OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
TELEGRAM_ALLOWED_USERS=${TELEGRAM_ALLOWED_USERS}
TELEGRAM_HOME_CHANNEL=${TELEGRAM_HOME_CHANNEL}
TELEGRAM_HOME_CHANNEL_NAME=${TELEGRAM_HOME_CHANNEL_NAME}
NOTION_ACCESS_TOKEN=${NOTION_ACCESS_TOKEN}
N8N_URL=${N8N_URL}
N8N_API_KEY=${N8N_API_KEY}
DEFAULT_MODEL=${DEFAULT_MODEL}
LLM_PROVIDER=${LLM_PROVIDER}
EOF

uv run hermes config set model "${DEFAULT_MODEL}"
uv run hermes config set provider "${LLM_PROVIDER}"

nohup uv run hermes gateway run --replace > /tmp/hermes_gw.log 2>&1 &
echo "Gateway levantado en cloud con PID $!"

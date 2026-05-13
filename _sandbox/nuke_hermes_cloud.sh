#!/bin/bash
set -e

echo '💀 PHASE 1: KILL ALL HERMES'
pkill -9 -f hermes_cli 2>/dev/null || true
pkill -9 -f hermes-agent 2>/dev/null || true
sleep 2
echo 'All processes killed'

echo ''
echo '💾 PHASE 2: BACKUP .ENV'
cp /root/.hermes/.env /tmp/hermes_cloud_env.bak 2>/dev/null || echo 'No .env to backup'
echo 'Env backed up to /tmp/hermes_cloud_env.bak'

echo ''
echo '🗑️ PHASE 3: NUKE EVERYTHING'
rm -rf /root/.hermes
rm -rf /usr/local/lib/hermes-agent
rm -f /usr/local/bin/hermes
rm -rf /root/FunnelsFoundry.AI/HERMES
echo 'All hermes directories nuked'

echo ''
echo '📦 PHASE 4: INSTALL UV'
if ! command -v uv > /dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="/root/.local/bin:$PATH"
fi
echo "uv installed: $(uv --version 2>/dev/null)"

echo ''
echo '📥 PHASE 5: CLONE FRESH'
mkdir -p /root/FunnelsFoundry.AI/HERMES
cd /root/FunnelsFoundry.AI/HERMES
git clone --depth 1 https://github.com/NousResearch/hermes-agent.git
echo 'Clone done'

echo ''
echo '⚙️ PHASE 6: INSTALL DEPS'
cd /root/FunnelsFoundry.AI/HERMES/hermes-agent
export PATH="/root/.local/bin:$PATH"
uv sync 2>&1 | tail -5
echo 'Install done'

echo ''
echo '🔑 PHASE 7: RESTORE ENV + CONFIG'
mkdir -p /root/.hermes
cp /tmp/hermes_cloud_env.bak /root/.hermes/.env
echo 'Env restored'

cd /root/FunnelsFoundry.AI/HERMES/hermes-agent
uv run hermes config set model "nvidia/nemotron-3-super-120b-a12b:free"
uv run hermes config set provider openrouter
echo 'Model + provider configured'

echo ''
echo '🩺 PHASE 8: VERSION CHECK'
uv run hermes version

echo ''
echo '🚀 PHASE 9: START GATEWAY'
cd /root/FunnelsFoundry.AI/HERMES/hermes-agent
nohup uv run hermes gateway run --replace > /tmp/hermes_gw.log 2>&1 &
GW_PID=$!
echo "Gateway started PID: $GW_PID"
sleep 10

echo ''
echo '=== GATEWAY STATE ==='
cat /root/.hermes/gateway_state.json 2>/dev/null | python3 -m json.tool 2>/dev/null || echo 'No gateway state yet'

echo ''
echo '=== LOG TAIL ==='
tail -15 /tmp/hermes_gw.log 2>/dev/null || echo 'No log yet'

echo ''
echo '✅ FACTORY RESET COMPLETE'

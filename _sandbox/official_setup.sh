#!/bin/bash
set -e
export PATH="/root/.local/bin:$PATH"
cd /root/hermes-agent
echo "--- CREATING VENV ---"
uv venv .venv --python 3.11
echo "--- INSTALLING CORE ---"
. .venv/bin/activate
uv pip install -e ".[all,dev]"
echo "--- INSTALLING SUBMODULES ---"
uv pip install -e "./tinker-atropos"
echo "--- DONE ---"

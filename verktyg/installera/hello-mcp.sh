#!/usr/bin/env bash
# Installerar exempelservern hello-mcp i en egen virtuell miljö.
set -uo pipefail
cd "$(dirname "$0")/../../exempel/mcp/hello-mcp" || exit 1
export PATH="$HOME/.local/bin:$PATH"

command -v uv >/dev/null || { echo "uv saknas — det ska finnas i imagen."; exit 1; }

uv sync || exit 1

echo
echo "Snabbtest utan MCP-klient:"
uv run python server.py --lista | head -5
echo
echo "Servern pratar stdio och startas av klienten, inte av oss."
echo "Den ligger nu i ~/work/.labb/mcp.json — vill du nå den från Open WebUI"
echo "behövs bryggan: verktyg/kor.sh installera mcpo"

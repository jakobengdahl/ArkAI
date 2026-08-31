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
echo "Två transporter, och skillnaden avgör vem som kan använda servern:"
echo
echo "  stdio            startas av klienten själv. Ligger nu i ~/work/.labb/mcp.json,"
echo "                   alltså inkopplad i Claude Code, Continue och OpenClaw"
echo "  Streamable HTTP  för Eneo, som kör i en annan podd och måste nå oss över nätet:"
echo "                     verktyg/kor.sh starta hello-mcp"
echo "                     verktyg/kor.sh koppla_eneo hello-mcp"

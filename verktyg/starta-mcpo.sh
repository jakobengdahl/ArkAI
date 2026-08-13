#!/usr/bin/env bash
# Startar MCP-bryggan mcpo, som exponerar innehållet i ~/work/.labb/mcp.json
# som OpenAPI-verktygsservrar — det format Open WebUI förstår.
#
#   verktyg/starta-mcpo.sh --bakgrund
#   verktyg/starta-mcpo.sh --stoppa
#
# mcp.json genereras ur verktyg/labb.toml och speglar vad som faktiskt kör.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PATH="$HOME/.local/bin:$PATH"

LABB="${LABB_DIR:-${WORKSPACE_DIR:-$HOME/work}/.labb}"
PORT="${MCPO_PORT:-8083}"
KONFIG="$LABB/mcp.json"
LOGG="$LABB/logg/mcpo.log"

if [ "${1:-}" = "--stoppa" ]; then
  pkill -f "mcpo --port $PORT" && echo "Stoppad." || echo "Ingenting kördes."
  exit 0
fi

command -v mcpo >/dev/null || { echo "mcpo saknas. Kör: verktyg/kor.sh installera mcpo"; exit 1; }

python3 verktyg/labb.py mcp-json >/dev/null
SERVRAR=$(python3 - "$KONFIG" <<'SLUTPY'
import json, sys
try:
    print(" ".join(json.load(open(sys.argv[1]))["mcpServers"]))
except Exception:
    pass
SLUTPY
)
if [ -z "${SERVRAR// /}" ]; then
  echo "Inga MCP-servrar att exponera. Installera en först, t.ex.:"
  echo "  verktyg/kor.sh installera hello-mcp"
  exit 1
fi

echo "Startar mcpo på port $PORT med $KONFIG"
echo "  servrar: $SERVRAR"

if [ "${1:-}" = "--bakgrund" ]; then
  mkdir -p "$LABB/logg"
  nohup mcpo --port "$PORT" --config "$KONFIG" >>"$LOGG" 2>&1 &
  echo "PID $!. Logg: $LOGG"
  for _ in $(seq 1 30); do
    sleep 1
    curl -sf "http://127.0.0.1:$PORT/openapi.json" >/dev/null 2>&1 && { echo "Uppe."; exit 0; }
  done
  echo "Svarade inte inom 30 s. Kolla loggen: tail -30 $LOGG"
  exit 1
fi

exec mcpo --port "$PORT" --config "$KONFIG"

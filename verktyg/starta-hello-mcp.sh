#!/usr/bin/env bash
# Kör Hello-MCP över Streamable HTTP, så att Eneo kan nå den.
#
#   ./verktyg/starta-hello-mcp.sh            # förgrunden
#   ./verktyg/starta-hello-mcp.sh --bakgrund
#   ./verktyg/starta-hello-mcp.sh --stoppa
#   ./verktyg/starta-hello-mcp.sh --token    # skriv ut token, skapa den om den saknas
#
# Varför HTTP när servern redan pratar stdio: stdio-servern startas av sin
# klient och lever i klientens process. Eneo kör i en annan podd i namnrymden
# och kan bara nå oss över nätet — och stödjer bara Streamable HTTP, varken
# stdio eller SSE. Se docs/60-miljo/eneo.md.
#
# Porten måste vara exponerad i Onyxia-tjänsten för att Eneo ska nå den, och en
# exponerad port är ett publikt värdnamn. Därför en token, alltid — servern
# vägrar starta utan.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
export PATH="$HOME/.local/bin:$PATH"

PORT="${HELLO_MCP_PORT:-8081}"
LABB="${WORKSPACE_DIR:-$HOME/work}/.labb"
TOKENFIL="$LABB/hello-mcp-token"
LOGG="$LABB/hello-mcp.log"
KATALOG="exempel/mcp/hello-mcp"

# Token skapas en gång och ligger kvar. Byter den värde måste kopplingen i Eneo
# göras om, så det ska inte hända av misstag.
token() {
  if [ ! -s "$TOKENFIL" ]; then
    mkdir -p "$LABB"
    (umask 077; openssl rand -hex 24 >"$TOKENFIL")
  fi
  chmod 600 "$TOKENFIL"
  cat "$TOKENFIL"
}

case "${1:-}" in
  --stoppa)
    pkill -f "server.py --http" && echo "Stoppad." || echo "Ingenting kördes."
    exit 0 ;;
  --token)
    token
    exit 0 ;;
esac

test -d "$KATALOG/.venv" || {
  echo "Hello-MCP är inte installerad. Kör: verktyg/kor.sh installera hello-mcp"; exit 1; }

if timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/$PORT" 2>/dev/null; then
  echo "Port $PORT är redan upptagen. Kör --stoppa först, eller sätt HELLO_MCP_PORT."
  echo "Porten delas med Open WebUI, som är på väg ut — se docs/60-miljo/openwebui.md."
  exit 1
fi

# Ingressen behövs av två skäl: Eneo når oss bara den vägen, och MCP-SDK:n
# kontrollerar Host-huvudet mot en lista som måste innehålla värdnamnet.
INGRESS="$(python3 verktyg/labb.py ingress "$PORT" 2>/dev/null)"
INGRESS="${INGRESS%/}"
VARD="${INGRESS#https://}"
if [ -z "$INGRESS" ]; then
  echo "Port $PORT är inte exponerad i den här tjänsten."
  echo "Då kan Eneo inte nå servern — den kör i en annan podd."
  echo "Portar exponeras när tjänsten startar, se docs/60-miljo/starta-labbet.md."
  echo "Servern startas ändå, för lokala klienter."
fi

export HELLO_MCP_TOKEN="$(token)"
export HELLO_MCP_PORT="$PORT"
export HELLO_MCP_VARDAR="${VARD:+$VARD,}127.0.0.1:$PORT,localhost:$PORT"

mkdir -p "$LABB"
echo "Startar Hello-MCP över HTTP"
echo "  adress    ${INGRESS:-http://127.0.0.1:$PORT}/mcp"
echo "  transport Streamable HTTP, utan session"
echo "  token     $TOKENFIL (krävs i Authorization: Bearer …)"
echo "  logg      $LOGG"
echo
echo "Koppla in den i Eneo med: verktyg/kor.sh koppla_eneo hello-mcp"
echo

if [ "${1:-}" = "--bakgrund" ]; then
  nohup uv run --directory "$KATALOG" python server.py --http >"$LOGG" 2>&1 &
  echo "PID $!. Väntar på att servern svarar..."
  for i in $(seq 1 30); do
    sleep 2
    if curl -sf "http://127.0.0.1:$PORT/halsa" >/dev/null 2>&1; then
      echo "Uppe efter ~$((i*2)) s."
      exit 0
    fi
  done
  echo "Svarade inte inom 60 s. Kolla loggen: tail -50 $LOGG"
  exit 1
else
  exec uv run --directory "$KATALOG" python server.py --http
fi

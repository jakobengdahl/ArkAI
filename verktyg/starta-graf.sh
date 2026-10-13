#!/usr/bin/env bash
# Startar den egna grafen här i podden.
#
#   ./verktyg/starta-graf.sh              # i förgrunden
#   ./verktyg/starta-graf.sh --bakgrund
#   ./verktyg/starta-graf.sh --stoppa
#   ./verktyg/starta-graf.sh --starta-om  # t.ex. efter ändrat schema
#   ./verktyg/starta-graf.sh --service    # bara: rikta Servicen arkai-graf mot den här podden
#
# Appen läser schemat i ~/work/graf-config när den startar. En omstart är
# alltså allt som behövs för att pröva ett ändrat schema.
#
# Saknas ~/work/graf-data/graph.json kopieras startdatan dit först, om det
# finns någon i ~/work/graf-config/graph.json. Finns grafen rörs den inte.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
export PATH="$HOME/.local/bin:$PATH"

PORT="${GRAF_PORT:-8085}"
ARBETE="${WORKSPACE_DIR:-$HOME/work}"
GRAF_KONFIG="${GRAF_KONFIG:-$ARBETE/graf-config}"
GRAF_DATA="${GRAF_DATA:-$ARBETE/graf-data}"
LABB="$ARBETE/.labb"
GRAF="$LABB/graf"
KOD="$GRAF/kod"
VENV="$GRAF/venv"
LOGG="$LABB/graf.log"
PIDFIL="$GRAF/graf.pid"
# Samma enkla inloggning som Eneo, av samma skäl — se docs/60-miljo/egen-graf.md.
GRAF_ANVANDARE="${GRAF_ANVANDARE:-arkai}"
GRAF_LOSEN="${GRAF_LOSEN:-arkai@arkai.se}"
# Unikt nog att stoppa på utan att träffa något annat i podden.
MONSTER="uvicorn backend.api_host.server:get_app --factory --host 0.0.0.0 --port $PORT"

stoppa() {
  local pid
  pid="$(cat "$PIDFIL" 2>/dev/null)"
  if [ -n "$pid" ] && kill "$pid" 2>/dev/null || pkill -f "$MONSTER"; then
    # Appen skriver grafen atomiskt, men vänta in den så att en omstart eller
    # omseedning inte möter en halvstängd process.
    for _ in $(seq 1 20); do pgrep -f "$MONSTER" >/dev/null || break; sleep 0.5; done
    echo "Grafen stoppad. Data ligger kvar i $GRAF_DATA."
  else
    echo "Grafen kördes inte."
  fi
  rm -f "$PIDFIL"
}

# Servicen arkai-graf ger Eneo en stabil adress: arkai-graf:8000 → den här
# poddens port. Selectorn pekar på VS Code-tjänstens instans, som byter namn
# när en ny tjänst startas — därför sätts den om vid varje start.
service() {
  local instans namn
  instans="$(kubectl get pod "$HOSTNAME" -o jsonpath='{.metadata.labels.app\.kubernetes\.io/instance}' 2>/dev/null)"
  namn="$(kubectl get pod "$HOSTNAME" -o jsonpath='{.metadata.labels.app\.kubernetes\.io/name}' 2>/dev/null)"
  if [ -z "$instans" ]; then
    echo "     hittar inte den här poddens etiketter — Servicen lämnas som den är"
    return 0
  fi
  kubectl apply -f - >/dev/null <<SLUT || return 1
apiVersion: v1
kind: Service
metadata:
  name: arkai-graf
  labels:
    app.kubernetes.io/part-of: arkai-graf
spec:
  selector:
    app.kubernetes.io/instance: "$instans"
    app.kubernetes.io/name: "$namn"
  ports:
    - port: 8000
      targetPort: $PORT
SLUT
  echo "     Service arkai-graf:8000 → $instans:$PORT"
}

# Kontrolleras innan något stoppas: ett skrivfel i schemat ska inte ta ner en
# graf som kör.
schemat_duger() {
  [ -s "$GRAF_KONFIG/schema_config.json" ] || {
    echo "Hittar inte $GRAF_KONFIG/schema_config.json. Kör: verktyg/kor.sh installera graf"; return 1; }
  local fil
  for fil in schema_config.json federation_config.json; do
    [ -f "$GRAF_KONFIG/$fil" ] || continue
    python3 -m json.tool "$GRAF_KONFIG/$fil" >/dev/null 2>&1 || {
      echo "$GRAF_KONFIG/$fil är inte giltig JSON — rätta den och starta igen."
      echo "Grafen som kör (om någon) har inte rörts."
      return 1; }
  done
}

case "${1:-}" in
  --stoppa)   stoppa; exit 0 ;;
  --service)  service; exit $? ;;
  --starta-om) schemat_duger || exit 1; stoppa; set -- --bakgrund ;;
esac
schemat_duger || exit 1

[ -x "$VENV/bin/python" ] && [ -f "$KOD/frontend/web/dist/index.html" ] || {
  echo "Grafen är inte installerad. Kör: verktyg/kor.sh installera graf"; exit 1; }
if pgrep -f "$MONSTER" >/dev/null; then
  echo "Grafen kör redan. Starta om med: verktyg/starta-graf.sh --starta-om"
  exit 0
fi
if timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/$PORT" 2>/dev/null; then
  echo "Port $PORT är upptagen av något annat. Sätt GRAF_PORT eller frigör porten."
  exit 1
fi

# ── Startdata ─────────────────────────────────────────────────────────────

mkdir -p "$GRAF_DATA"
if [ ! -s "$GRAF_DATA/graph.json" ]; then
  if [ -s "$GRAF_KONFIG/graph.json" ]; then
    cp "$GRAF_KONFIG/graph.json" "$GRAF_DATA/graph.json"
    echo "Grafen saknades — seedad ur $GRAF_KONFIG/graph.json"
  else
    echo "Ingen graf och ingen startdata — grafen börjar tom"
  fi
fi

# ── Miljön ────────────────────────────────────────────────────────────────

TOKENFIL="$LABB/graf-token"
[ -s "$TOKENFIL" ] || ( umask 077; openssl rand -hex 32 > "$TOKENFIL" )
export GRAPH_FILE="$GRAF_DATA/graph.json"
export COMMUNITYOVERVIEW_TENANT_CONFIG_DIR="$GRAF_KONFIG"
export CONFIG_PROFILE="arkai"
export WEB_STATIC_PATH="$KOD/frontend/web/dist"
export WIDGET_STATIC_PATH="$KOD/frontend/widget/dist"
export LLM_PROVIDER=openai
export OPENAI_MODEL="${GRAF_MODELL:-${OPENAI_MODEL:-gemma4-26b-moe}}"
# Porten kan ligga på ett publikt värdnamn: webbgränssnittet kräver
# inloggning, MCP kräver token. Appen tar båda i samma middleware.
export AUTH_ENABLED=true
export AUTH_USERNAME="$GRAF_ANVANDARE"
export AUTH_PASSWORD="$GRAF_LOSEN"
export AUTH_BEARER_TOKEN="$(cat "$TOKENFIL")"
# Modellen sentence-transformers hämtar första gången hamnar under ~/work.
export HF_HOME="$GRAF/hf"
export PYTHONPATH="$KOD" PYTHONUNBUFFERED=1
[ -n "${OPENAI_API_KEY:-}" ] || echo "OPENAI_API_KEY saknas — grafens inbyggda assistent fungerar inte, resten gör det"

if [ "$(kubectl auth can-i create services 2>/dev/null)" = "yes" ]; then
  service
fi

INGRESS="$(python3 verktyg/labb.py ingress "$PORT" 2>/dev/null)"
echo "Startar den egna grafen"
echo "  adress    ${INGRESS:-(port $PORT inte exponerad — nås inne i namnrymden som arkai-graf:8000)}"
echo "  schema    $GRAF_KONFIG"
echo "  data      $GRAF_DATA"
echo "  logg      $LOGG"
echo

cd "$KOD" || exit 1
if [ "${1:-}" = "--bakgrund" ]; then
  setsid nohup "$VENV/bin/python" -m $MONSTER >"$LOGG" 2>&1 < /dev/null &
  echo $! > "$PIDFIL"
  echo "PID $!. Väntar på att grafen svarar..."
  # Första starten laddar torch och kan ta en stund.
  for i in $(seq 1 90); do
    sleep 2
    if curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
      echo "Uppe efter ~$((i*2)) s.${INGRESS:+ Öppna $INGRESS}"
      exit 0
    fi
    kill -0 "$(cat "$PIDFIL")" 2>/dev/null || {
      echo "Processen dog. Sista raderna ur $LOGG:"; tail -25 "$LOGG"; exit 1; }
  done
  echo "Svarade inte inom 180 s. Kolla loggen: tail -50 $LOGG"
  exit 1
else
  exec "$VENV/bin/python" -m $MONSTER
fi

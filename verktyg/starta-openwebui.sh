#!/usr/bin/env bash
# Startar Open WebUI i den här tjänsten.
#
#   ./verktyg/starta-openwebui.sh          # starta i förgrunden
#   ./verktyg/starta-openwebui.sh --bakgrund
#   ./verktyg/starta-openwebui.sh --stoppa
#
# Port 8080 är upptagen av code-server (VS Code). Använd inte den.
# Se docs/60-miljo/openwebui.md för hur du når gränssnittet i webbläsaren.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

export PATH="$HOME/.local/bin:$PATH"
[ -f .env ] && set -a && . ./.env && set +a

PORT="${OPEN_WEBUI_PORT:-8081}"
DATA="${DATA_DIR:-$HOME/work/open-webui-data}"
LOGG="${DATA%/}/open-webui.log"

if [ "${1:-}" = "--stoppa" ]; then
  pkill -f "open-webui serve" && echo "Stoppad." || echo "Ingenting kördes."
  exit 0
fi

command -v open-webui >/dev/null || {
  echo "open-webui saknas. Installera:"
  echo "  uv python install 3.11"
  echo "  uv tool install --python 3.11 open-webui"
  exit 1
}

if timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/$PORT" 2>/dev/null; then
  echo "Port $PORT är redan upptagen. Sätt OPEN_WEBUI_PORT i .env eller kör --stoppa."
  exit 1
fi

mkdir -p "$DATA"
export DATA_DIR="$DATA"

# Är porten exponerad ligger instansen på ett publikt värdnamn. Då är inloggning
# inte en inställning man får glömma, så den slås på av sig själv. Exponerar du
# inte porten når bara du den, och då är False bekvämt och ofarligt.
INGRESS=$(python3 verktyg/labb.py ingress "$PORT" 2>/dev/null)
if [ -n "$INGRESS" ]; then
  if [ "${WEBUI_AUTH:-}" = "False" ] && [ "${TILLAT_OSKYDDAD:-}" != "ja" ]; then
    echo "Vägrar starta utan inloggning: porten $PORT är exponerad på"
    echo "  $INGRESS"
    echo "Ta bort WEBUI_AUTH=False ur .env, eller kör med TILLAT_OSKYDDAD=ja om"
    echo "du verkligen menar det."
    exit 1
  fi
  export WEBUI_AUTH="${WEBUI_AUTH:-True}"
else
  export WEBUI_AUTH="${WEBUI_AUTH:-False}"
fi
export ENABLE_OLLAMA_API="${ENABLE_OLLAMA_API:-False}"
export ENABLE_OPENAI_API="${ENABLE_OPENAI_API:-False}"

echo "Startar Open WebUI"
echo "  port      $PORT"
echo "  data      $DATA"
echo "  inloggning ${WEBUI_AUTH}${INGRESS:+  (porten är exponerad: $INGRESS)}"
echo "  logg      $LOGG"
echo

# Binder till alla gränssnitt, inte bara loopback. Onyxias portexponering går
# via en Service som når podden på dess pod-IP — en tjänst som bara lyssnar på
# 127.0.0.1 svarar 502 genom ingressen.
if [ "${1:-}" = "--bakgrund" ]; then
  nohup open-webui serve --host 0.0.0.0 --port "$PORT" >"$LOGG" 2>&1 &
  echo "PID $!. Väntar på att tjänsten svarar..."
  for i in $(seq 1 60); do
    sleep 2
    if curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
      echo "Uppe efter ~$((i*2)) s. Följ loggen med: tail -f $LOGG"
      exit 0
    fi
  done
  echo "Svarade inte inom 120 s. Kolla loggen: tail -50 $LOGG"
  exit 1
else
  exec open-webui serve --host 0.0.0.0 --port "$PORT"
fi

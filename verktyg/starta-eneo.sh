#!/usr/bin/env bash
# Startar Eneo: skalar upp tjänsterna i namnrymden och kör proxyn här i podden.
#
#   ./verktyg/starta-eneo.sh              # proxyn i förgrunden
#   ./verktyg/starta-eneo.sh --bakgrund
#   ./verktyg/starta-eneo.sh --stoppa     # proxyn ner, tjänsterna skalas till noll
#
# Själva Eneo kör som arbetslaster i namnrymden och överlever att den här
# podden startas om. Det som *inte* överlever är proxyn — och värdnamnet:
# en ny Onyxia-tjänst får ett nytt namn, och då måste Eneos PUBLIC_ORIGIN
# skrivas om. Skriptet gör det åt dig.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
export PATH="$HOME/.local/bin:$PATH"

PORT="${ENEO_PORT:-8084}"
LABB="${WORKSPACE_DIR:-$HOME/work}/.labb"
LOGG="$LABB/eneo-proxy.log"
ARBETSLASTER="deployment/eneo-backend deployment/eneo-frontend"

export ENEO_PORT="$PORT"
export ENEO_BACKEND="${ENEO_BACKEND:-eneo-backend:8000}"
export ENEO_FRONTEND="${ENEO_FRONTEND:-eneo-frontend:3000}"
# Caddy vill ha egna kataloger för certifikat och tillstånd. Vi terminerar inte
# TLS här — ingressen gör det — men den skriver ändå, så peka den utanför repot.
export XDG_DATA_HOME="$LABB/caddy" XDG_CONFIG_HOME="$LABB/caddy"

if [ "${1:-}" = "--stoppa" ]; then
  pkill -f "caddy run --config verktyg/eneo/Caddyfile" && echo "Proxyn stoppad." \
    || echo "Proxyn kördes inte."
  # Alla arbetslaster till noll — inga poddar blir kvar, ingenting tar CPU
  # eller minne. Volymerna ligger kvar, och med dem konton, assistenter och
  # kunskapskällor. Det är skillnaden mot ta-bort-eneo.sh.
  kubectl scale --replicas=0 $ARBETSLASTER statefulset/eneo-db statefulset/eneo-redis \
    2>/dev/null && echo "Alla poddar nerskalade. Data kvar på volymerna." \
                && echo "Starta igen med: verktyg/kor.sh starta eneo"
  exit 0
fi

command -v caddy >/dev/null || {
  echo "caddy saknas. Kör: verktyg/kor.sh installera eneo"; exit 1; }
kubectl get deployment eneo-backend >/dev/null 2>&1 || {
  echo "Eneo är inte deployat i namnrymden. Kör: verktyg/kor.sh installera eneo"; exit 1; }

# ── Värdnamnet ────────────────────────────────────────────────────────────
#
# PUBLIC_ORIGIN sitter i tre lager: backendens OIDC-URL:er, frontendens
# sessionskaka och SvelteKits ORIGIN-kontroll. Stämmer det inte med det
# värdnamn webbläsaren använder blir inloggningen tyst trasig.

ORIGIN="$(python3 verktyg/labb.py ingress "$PORT" 2>/dev/null)"
ORIGIN="${ORIGIN%/}"
if [ -z "$ORIGIN" ]; then
  echo "Port $PORT är inte exponerad i den här tjänsten — Eneo går inte att nå utifrån."
  echo "Portar exponeras när tjänsten startar. Se docs/60-miljo/eneo.md."
  exit 1
fi

NUVARANDE="$(kubectl get configmap eneo-backend-konfig -o jsonpath='{.data.PUBLIC_ORIGIN}' 2>/dev/null)"
if [ "$NUVARANDE" != "$ORIGIN" ]; then
  echo "Värdnamnet har ändrats sedan installationen:"
  echo "  förr  ${NUVARANDE:-(inget)}"
  echo "  nu    $ORIGIN"
  kubectl patch configmap eneo-backend-konfig \
    -p "{\"data\":{\"PUBLIC_ORIGIN\":\"$ORIGIN\"}}" >/dev/null || exit 1
  kubectl patch configmap eneo-frontend-konfig -p "{\"data\":{
     \"ENEO_BACKEND_URL\":\"$ORIGIN\",
     \"PUBLIC_ENEO_BACKEND_URL\":\"$ORIGIN\",
     \"ORIGIN\":\"$ORIGIN\",
     \"PUBLIC_ORIGIN\":\"$ORIGIN\"}}" >/dev/null || exit 1
  # ConfigMap-ändringar når inte en podd som redan kör.
  kubectl rollout restart $ARBETSLASTER >/dev/null
fi

# ── Tjänsterna ────────────────────────────────────────────────────────────

if [ "$(kubectl get statefulset eneo-db -o jsonpath='{.spec.replicas}')" = "0" ]; then
  echo "Skalar upp tjänsterna igen"
  kubectl scale --replicas=1 statefulset/eneo-db statefulset/eneo-redis >/dev/null
  kubectl rollout status statefulset/eneo-db --timeout=300s || exit 1
  kubectl scale --replicas=1 $ARBETSLASTER >/dev/null
fi
for al in $ARBETSLASTER; do
  kubectl rollout status "$al" --timeout=600s || exit 1
done

# ── Proxyn ────────────────────────────────────────────────────────────────

if timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/$PORT" 2>/dev/null; then
  echo "Port $PORT är redan upptagen. Kör --stoppa först, eller sätt ENEO_PORT."
  exit 1
fi

mkdir -p "$LABB"
echo "Startar Eneo"
echo "  adress    $ORIGIN"
echo "  proxy     port $PORT → $ENEO_FRONTEND, /api → $ENEO_BACKEND"
echo "  inloggning $(kubectl get configmap eneo-backend-konfig -o jsonpath='{.data.DEFAULT_USER_EMAIL}' 2>/dev/null)"
echo "  logg      $LOGG"
echo

if [ "${1:-}" = "--bakgrund" ]; then
  nohup caddy run --config verktyg/eneo/Caddyfile --adapter caddyfile >"$LOGG" 2>&1 &
  echo "PID $!. Väntar på att Eneo svarar..."
  for i in $(seq 1 30); do
    sleep 2
    if curl -sf "http://127.0.0.1:$PORT/version" >/dev/null 2>&1; then
      echo "Uppe efter ~$((i*2)) s. Öppna $ORIGIN"
      exit 0
    fi
  done
  echo "Svarade inte inom 60 s. Kolla loggen: tail -50 $LOGG"
  exit 1
else
  exec caddy run --config verktyg/eneo/Caddyfile --adapter caddyfile
fi

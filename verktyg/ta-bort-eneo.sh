#!/usr/bin/env bash
# Tar bort Eneo ur namnrymden.
#
#   ./verktyg/ta-bort-eneo.sh                # allt, inklusive databasens volym
#   ./verktyg/ta-bort-eneo.sh --behall-data  # arbetslasterna bort, volymerna kvar
#
# Varför det behövs: Eneo kör i namnrymden, inte i den här podden. Stoppar du
# VS Code-tjänsten fortsätter Eneo att köra och att ta av kvoten — poddar och
# lagring — tills någon tar bort det. Det är inte ett fel, det är hela poängen
# med att inte köra det i podden, men det betyder att uppstädningen är ett eget
# steg som ingen påminner om.
#
# `kor.sh stoppa eneo` skalar till noll och behåller allt. Det här skriptet tar
# bort. Allt som raderas är märkt app.kubernetes.io/part-of=eneo — inget annat
# i namnrymden rörs.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
export PATH="$HOME/.local/bin:$PATH"

ETIKETT="app.kubernetes.io/part-of=eneo"
LABB="${WORKSPACE_DIR:-$HOME/work}/.labb"
BEHALL_DATA=nej
[ "${1:-}" = "--behall-data" ] && BEHALL_DATA=ja

command -v kubectl >/dev/null || { echo "kubectl saknas."; exit 1; }

# ── 1. Proxyn här i podden ────────────────────────────────────────────────

echo "1/3  Stoppar proxyn"
pkill -f "caddy run --config verktyg/eneo/Caddyfile" && echo "     stoppad" \
  || echo "     kördes inte"

# ── 2. Arbetslasterna ─────────────────────────────────────────────────────
#
# `all` i kubectl omfattar inte konfiguration och hemligheter, så de räknas
# upp för sig. Jobbet finns kvar efter att ha lyckats och måste också bort.

# Hemligheten följer med datan, inte med arbetslasterna: i den ligger
# databaslösenordet och ENCRYPTION_KEY. Behåller vi volymerna men slänger
# hemligheten får nästa installation nya värden — och kommer varken in i
# databasen eller åt de krypterade modellnycklarna.
SORTER="deployments,statefulsets,jobs,services,configmaps"
[ "$BEHALL_DATA" = "ja" ] || SORTER="$SORTER,secrets"

echo "2/3  Tar bort arbetslaster, tjänster och konfiguration"
kubectl delete "$SORTER" -l "$ETIKETT" --ignore-not-found --wait=false || exit 1

# ── 3. Volymerna ──────────────────────────────────────────────────────────
#
# Här ligger databasen. Det är det enda steget som förstör något som inte går
# att skapa om.

if [ "$BEHALL_DATA" = "ja" ]; then
  echo "3/3  Behåller volymerna"
  kubectl get pvc -l "$ETIKETT" \
    -o custom-columns=VOLYM:.metadata.name,STORLEK:.spec.resources.requests.storage 2>/dev/null
  echo
  echo "Volymerna och hemligheten ligger kvar och volymerna tar av lagringskvoten."
  echo "En ny installation monterar dem igen — databasen är kvar som den var, och"
  echo "inloggningen i ~/work/.labb/eneo-inloggning.txt gäller fortfarande."
else
  echo "3/3  Tar bort volymerna — databasen försvinner"
  kubectl delete pvc -l "$ETIKETT" --ignore-not-found || exit 1
  rm -f "$LABB/eneo-inloggning.txt"
  echo "     tog också bort $LABB/eneo-inloggning.txt (kontot finns inte längre)"
fi

echo
echo "Kvar i namnrymden med etiketten eneo:"
kubectl get all,pvc,configmap,secret -l "$ETIKETT" 2>/dev/null | grep -v '^$' || true
echo
echo "Installera igen med: verktyg/kor.sh installera eneo"

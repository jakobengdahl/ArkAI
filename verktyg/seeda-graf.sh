#!/usr/bin/env bash
# Ersätter den egna grafens data med en lokal graph.json.
#
#   verktyg/seeda-graf.sh <fil>          # frågar först
#   verktyg/seeda-graf.sh <fil> --ja     # frågar inte
#
# I VS Code: öppna filen och kör tasken "Grafen: seeda från öppen fil"
# (Ctrl+Shift+P → Tasks: Run Task).
#
# Till skillnad från startdatan i ~/work/graf-config — som bara används när
# ~/work/graf-data saknar en graf — byter det här ut grafen som den ser ut nu.
# Grafen som byts ut flyttas till ~/work/graf-data/arkiv/<tid>/, tillsammans
# med sina sidofiler: journalen, historiken och embeddings (graph.*). Blir
# journalen kvar spelas den upp ovanpå den nya grafen.
#
# Filen ska vara i appens exportformat: ett objekt med listorna nodes och edges.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

FIL="${1:-}"
JA=nej
[ "${2:-}" = "--ja" ] && JA=ja
ARBETE="${WORKSPACE_DIR:-$HOME/work}"
GRAF_DATA="${GRAF_DATA:-$ARBETE/graf-data}"
LABB="$ARBETE/.labb"
PORT="${GRAF_PORT:-8085}"

if [ -z "$FIL" ] || [ ! -s "$FIL" ]; then
  echo "Ange en graph.json att seeda grafen med:"
  echo "  verktyg/seeda-graf.sh <fil>"
  [ -n "$FIL" ] && echo "Hittar ingen fil (eller en tom fil) på $FIL."
  exit 1
fi
FIL="$(realpath "$FIL")"
case "$FIL" in
  "$GRAF_DATA"/graph.json) echo "Det där är grafen som kör. Välj en annan fil."; exit 1 ;;
esac

python3 - "$FIL" <<'PY' || exit 1
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except (OSError, ValueError) as fel:
    sys.exit(f"{sys.argv[1]} går inte att läsa som JSON: {fel}")
if not isinstance(d, dict) or not isinstance(d.get("nodes"), list) or not isinstance(d.get("edges"), list):
    sys.exit(f"{sys.argv[1]} ser inte ut som en graf: nycklarna nodes och edges ska vara listor")
print(f"Ny graf:     {len(d['nodes'])} noder, {len(d['edges'])} relationer  ({sys.argv[1]})")
PY

# Samma lås som kor.sh och panelen tar, så att ingen startar eller stoppar
# grafen medan filerna byts.
mkdir -p "$LABB/las"
exec 9>"$LABB/las/graf.lock"
flock -w 2 9 || {
  echo "Något körs redan för grafen (installation, start eller stopp). Försök igen strax."
  exit 3
}

if [ -s "$GRAF_DATA/graph.json" ]; then
  python3 -c "
import json,sys
d=json.load(open(sys.argv[1]))
print(f\"Nuvarande:   {len(d['nodes'])} noder, {len(d['edges'])} relationer\")" "$GRAF_DATA/graph.json" 2>/dev/null \
    || echo "Nuvarande:   (gick inte att läsa)"
else
  echo "Nuvarande:   ingen graf"
fi
echo
if [ "$JA" != "ja" ]; then
  read -r -p "Ersätt grafen? Den nuvarande arkiveras. [skriv ja] " SVAR
  [ "$SVAR" = "ja" ] || { echo "Avbrutet, inget ändrat."; exit 0; }
fi

KORDE=nej
if curl -sf "http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
  KORDE=ja
  verktyg/starta-graf.sh --stoppa 9>&-
fi

ARKIV="$GRAF_DATA/arkiv/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$ARKIV"
FLYTTADE=0
for f in "$GRAF_DATA"/graph.json "$GRAF_DATA"/graph.*; do
  [ -e "$f" ] || continue
  mv "$f" "$ARKIV/" && FLYTTADE=$((FLYTTADE + 1))
done
if [ "$FLYTTADE" -gt 0 ]; then
  echo "Tidigare graf ($FLYTTADE filer) flyttad till $ARKIV"
else
  rmdir "$ARKIV" 2>/dev/null
fi
cp "$FIL" "$GRAF_DATA/graph.json"
echo "Grafen kommer nu ur $FIL"

if [ "$KORDE" = "ja" ]; then
  echo
  verktyg/starta-graf.sh --bakgrund 9>&-
else
  echo "Grafen kördes inte. Den nya grafen läses när du startar: verktyg/kor.sh starta graf"
fi

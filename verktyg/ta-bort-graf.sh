#!/usr/bin/env bash
# Tar bort den egna grafen.
#
#   ./verktyg/ta-bort-graf.sh                # allt utom schemat, inklusive grafens data
#   ./verktyg/ta-bort-graf.sh --behall-data  # källkod och Python-miljö bort, grafen kvar
#
# Schemat i ~/work/graf-config rörs aldrig — det är någons arbete. En ny
# installation använder det igen.
#
# I namnrymden finns bara Servicen arkai-graf. Den väljs på etiketten
# app.kubernetes.io/part-of=arkai-graf, aldrig på namn: namnrymden delas med
# andra CommunityOverview-instanser (communityoverview-*).
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

ARBETE="${WORKSPACE_DIR:-$HOME/work}"
GRAF_DATA="${GRAF_DATA:-$ARBETE/graf-data}"
GRAF="$ARBETE/.labb/graf"
ETIKETT="app.kubernetes.io/part-of=arkai-graf"
BEHALL_DATA=nej
[ "${1:-}" = "--behall-data" ] && BEHALL_DATA=ja

echo "1/3  Stoppar grafen"
verktyg/starta-graf.sh --stoppa | sed 's/^/     /'

echo "2/3  Tar bort källkod, Python-miljö och Servicen"
rm -rf "$GRAF"
kubectl delete services,deployments,configmaps,secrets,pvc -l "$ETIKETT" \
  --ignore-not-found --wait=false 2>/dev/null | sed 's/^/     /'

if [ "$BEHALL_DATA" = "ja" ]; then
  echo "3/3  Behåller grafen i $GRAF_DATA"
else
  echo "3/3  Tar bort grafen i $GRAF_DATA, med arkiv"
  rm -rf "$GRAF_DATA"
fi

echo
echo "Schemat ligger kvar i $ARBETE/graf-config."
echo "Installera igen med: verktyg/kor.sh installera graf"

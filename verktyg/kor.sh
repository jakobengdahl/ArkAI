#!/usr/bin/env bash
# Kör en handling ur verktyg/labb.toml — installera, starta eller stoppa.
#
#   verktyg/kor.sh installera openwebui
#   verktyg/kor.sh starta openwebui
#   verktyg/kor.sh stoppa openwebui
#   verktyg/kor.sh uppsattning chatt-med-verktyg
#   verktyg/kor.sh lista
#
# Panelen anropar exakt det här skriptet. Det är avsiktligt: en installation du
# startade i terminalen ska låsa knappen i panelen, och tvärtom.
#
# Låset är icke-blockerande. Körs redan något för samma tjänst avslutas vi med
# kod 3 i stället för att starta en andra körning.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

LABB="${LABB_DIR:-${WORKSPACE_DIR:-$HOME/work}/.labb}"
mkdir -p "$LABB/logg" "$LABB/las" "$LABB/status"

fel()  { printf '\033[31m%s\033[0m\n' "$*" >&2; }
info() { printf '\033[34m%s\033[0m\n' "$*"; }
klar() { printf '\033[32m%s\033[0m\n' "$*"; }

manifest() { python3 verktyg/labb.py "$@" 2>/dev/null; }

anvandning() {
  cat <<'SLUT'
Användning:
  verktyg/kor.sh <installera|starta|stoppa> <tjänst>
  verktyg/kor.sh uppsattning <namn>
  verktyg/kor.sh status [tjänst]
  verktyg/kor.sh lista
SLUT
}

# ── Enskild handling ──────────────────────────────────────────────────────

utfor() { # utfor <handling> <tjänst>
  local handling=$1 tjid=$2
  local kmd; kmd=$(manifest kommando "$tjid" "$handling")

  if [ -z "$kmd" ]; then
    fel "Tjänsten '$tjid' har ingen handling '$handling' i verktyg/labb.toml."
    return 2
  fi

  local logg="$LABB/logg/$tjid-$handling.log"
  local las="$LABB/las/$tjid.lock"
  touch "$las"

  exec 9>"$las"
  if ! flock -n 9; then
    fel "Något körs redan för '$tjid'. Följ det i stället:"
    fel "  tail -f $LABB/logg/$tjid-*.log"
    return 3
  fi

  local bakgrund
  bakgrund=$(python3 - "$tjid" "$handling" <<'SLUTPY' 2>/dev/null
import sys
sys.path.insert(0, "verktyg")
import labb
print("ja" if labb.tjanst(sys.argv[1]).get(sys.argv[2] + "_bakgrund") else "nej")
SLUTPY
)

  status_skriv "$tjid" arbetar "$handling" "$logg"
  info "→ $handling $tjid"
  echo "  logg: $logg"
  {
    echo "── $(date -Iseconds)  $handling $tjid"
    echo "   $kmd"
  } >>"$logg"

  # 9>&- stänger låsdeskriptorn i barnprocessen. Utan det ärver en
  # bakgrundsdemon låset och håller kvar det långt efter att kor.sh dött —
  # då är tjänsten låst tills podden startas om.
  local kod=0
  if [ "$bakgrund" = "ja" ]; then
    # Kommandot återvänder inte av sig självt. Koppla loss det och vänta
    # i stället på att tjänsten svarar.
    setsid nohup bash -lc "$kmd" >>"$logg" 2>&1 9>&- &
    echo "  pid $!"
    vanta_pa "$tjid" 30 || kod=1
  else
    set -o pipefail
    bash -lc "$kmd" 2>&1 9>&- | tee -a "$logg"
    kod=${PIPESTATUS[0]}
  fi

  if [ "$kod" -eq 0 ]; then
    klar "✓ $handling $tjid"
    status_skriv "$tjid" klar "$handling" "$logg" 0
  else
    fel "✗ $handling $tjid misslyckades (kod $kod). Sista raderna:"
    tail -15 "$logg" >&2
    status_skriv "$tjid" fel "$handling" "$logg" "$kod"
  fi

  flock -u 9
  # mcp.json speglar vad som faktiskt kör.
  python3 verktyg/labb.py mcp-json >/dev/null 2>&1
  return "$kod"
}

vanta_pa() { # vanta_pa <tjänst> <sekunder>
  # Frågar efter livstecken, inte efter tillstånd: vi håller själva låset här,
  # och tillståndet skulle därför alltid svara "arbetar".
  local tjid=$1 sek=$2 i
  for ((i = 0; i < sek; i++)); do
    sleep 1
    python3 verktyg/labb.py levande "$tjid" 2>/dev/null && return 0
  done
  return 1
}

# Allt går inte att starta. En stdio-server startas av sin klient, och en
# fjärrtjänst kör redan någon annanstans — att de saknar startkommando är inte
# ett fel.
starta_om_mojligt() {
  local tjid=$1
  if [ -n "$(manifest kommando "$tjid" starta)" ]; then
    utfor starta "$tjid"
  else
    klar "  ✓ $tjid är klar (startas inte här)"
  fi
}

status_skriv() { # status_skriv <tjänst> <tillstånd> <handling> <logg> [kod]
  python3 - "$@" <<'PY' 2>/dev/null
import sys, time
sys.path.insert(0, "verktyg")
import labb
tjid, tillstand, handling, logg = sys.argv[1:5]
kod = int(sys.argv[5]) if len(sys.argv) > 5 else None
labb.skriv_korning(tjid, tillstand=tillstand, handling=handling, logg=logg,
                   kod=kod, tidpunkt=time.strftime("%Y-%m-%d %H:%M:%S"))
PY
}

# ── Uppsättning ───────────────────────────────────────────────────────────
#
# Installerar det som saknas och startar i manifestets ordning. Hoppar över
# det som redan kör — knapparna ska gå att trycka på två gånger.

kor_uppsattning() {
  local namn=$1
  local tjanster
  tjanster=$(python3 - "$namn" <<'SLUTPY' 2>/dev/null
import sys
sys.path.insert(0, "verktyg")
import labb
u = labb.uppsattningar().get(sys.argv[1])
print(" ".join(u["tjanster"]) if u else "")
SLUTPY
)

  if [ -z "$tjanster" ]; then
    fel "Okänd uppsättning: $namn"
    return 2
  fi

  info "Uppsättning: $namn"
  local tjid tillstand
  for tjid in $tjanster; do
    tillstand=$(manifest tillstand "$tjid")
    case "$tillstand" in
      kor)         klar "  ✓ $tjid kör redan" ;;
      arbetar)     info "  … $tjid arbetar redan, hoppar över" ;;
      saknas)      utfor installera "$tjid" && starta_om_mojligt "$tjid" ;;
      installerad) starta_om_mojligt "$tjid" ;;
      okand)       fel "  ! $tjid går inte att nå — saknas uppgifter i miljön?" ;;
      *)           info "  ? $tjid: tillstånd '$tillstand' — hoppar över" ;;
    esac
  done

  python3 verktyg/labb.py mcp-json >/dev/null 2>&1
  klar "Klart. Panelen visar vad som kör."
}

# ── Ingång ────────────────────────────────────────────────────────────────

case "${1:-}" in
  installera|starta|stoppa)
    [ $# -eq 2 ] || { anvandning; exit 2; }
    utfor "$1" "$2"
    ;;
  uppsattning)
    [ $# -eq 2 ] || { anvandning; exit 2; }
    # Egen logg, så att panelen kan visa hur det gick för uppsättningen som
    # helhet och inte bara för en av tjänsterna i den.
    set -o pipefail
    kor_uppsattning "$2" 2>&1 | tee -a "$LABB/logg/$2-uppsattning.log"
    exit "${PIPESTATUS[0]}"
    ;;
  status)
    if [ $# -eq 2 ]; then python3 verktyg/labb.py status "$2"; else python3 verktyg/labb.py alla; fi
    ;;
  tillstand)
    [ $# -eq 2 ] || { anvandning; exit 2; }
    python3 verktyg/labb.py tillstand "$2"
    ;;
  lista)
    python3 - <<'PY'
import sys
sys.path.insert(0, "verktyg")
import labb
print("Tjänster")
for tjid, t in labb.tjanster().items():
    print(f"  {tjid:<16} {t.get('namn','')}")
print("\nUppsättningar")
for uid, u in labb.uppsattningar().items():
    print(f"  {uid:<20} {u.get('namn','')}  ({', '.join(u['tjanster'])})")
PY
    ;;
  *)
    anvandning; exit 2 ;;
esac

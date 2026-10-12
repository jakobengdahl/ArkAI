#!/usr/bin/env bash
# Installerar labbet stegvis.
#
#   verktyg/labb-start.sh          # kör, i förgrunden
#   verktyg/labb-start.sh --folj   # följ en körning som redan pågår, annars kör
#
# Startskriptet (verktyg/onyxia-init.sh) startar det här frånkopplat när
# tjänsten startar, så att panelen och installationerna är igång innan någon
# öppnat VS Code. När VS Code sedan öppnas kör terminalen `--folj` och visar
# samma körning, i stället för att starta en till.
#
# Ingenting här blockerar något annat. Panelen startas först och kan användas
# medan resten installeras — den visar "arbetar" på det som inte är klart.
#
# Vad som installeras bestäms av manifestet (steg = "auto") och av profilen i
# ~/work/.labb/miljo.toml, som skrevs av startskriptet. Allt går via
# verktyg/kor.sh, alltså med samma lås och samma loggar som panelens knappar.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PATH="$HOME/.local/bin:$HOME/.local/node/bin:$PATH"

LABB="${LABB_DIR:-${WORKSPACE_DIR:-$HOME/work}/.labb}"
mkdir -p "$LABB/logg"
PIDFIL="$LABB/labb-start.pid"
STARTLOGG="$LABB/logg/labb-start.log"

pagaende() { [ -f "$PIDFIL" ] && kill -0 "$(cat "$PIDFIL" 2>/dev/null)" 2>/dev/null; }

if [ "${1:-}" = "--folj" ]; then
  if pagaende; then
    printf '\n  Labbet installeras redan i bakgrunden — startades när tjänsten startade.\n'
    printf '  Här följer du samma körning. Ctrl+C stänger bara följningen.\n\n'
    exec tail -n +1 --pid="$(cat "$PIDFIL")" -f "$STARTLOGG"
  fi
  if [ -s "$STARTLOGG" ] && grep -q "── Klart" "$STARTLOGG"; then
    printf '\n  Labbet installerades i bakgrunden när tjänsten startade:\n\n'
    cat "$STARTLOGG"
    exit 0
  fi
fi

if pagaende; then
  echo "En installation pågår redan (PID $(cat "$PIDFIL")). Följ den med:"
  echo "  verktyg/labb-start.sh --folj"
  exit 0
fi
echo $$ > "$PIDFIL"
trap 'rm -f "$PIDFIL"' EXIT

rubrik() { printf '\n\033[1m── %s\033[0m\n' "$*"; }
ok()     { printf '  \033[32m✓\033[0m %s\n' "$*"; }
info()   { printf '  \033[34m·\033[0m %s\n' "$*"; }

PROFIL=$(python3 - <<'SLUTPY' 2>/dev/null || echo bas
import sys
sys.path.insert(0, "verktyg")
import labb
print(" ".join(labb.miljo().get("profil", ["bas"])))
SLUTPY
)

cat <<SLUT

  ArkAI — labbmiljön
  Profil: ${PROFIL:-bas}

  Det här fönstret installerar det som saknas. Du behöver inte vänta på det:
  panelen startas först och visar status hela tiden.

SLUT

# ── Panelen ───────────────────────────────────────────────────────────────
# Den ska vara uppe innan installationerna börjar, så att du kan följa dem där.
rubrik "Panelen"
./verktyg/starta-panelen.sh --bakgrund

# ── Tjänster ──────────────────────────────────────────────────────────────
# steg = "auto" i manifestet, plus det profilen räknar upp. Profilen "minimal"
# hoppar över allt — då är panelen det enda som startas.
AUTO=$(python3 - $PROFIL <<'SLUTPY' 2>/dev/null
import sys
sys.path.insert(0, "verktyg")
import labb
val = sys.argv[1:]
if "minimal" not in val:
    # Det som avvecklas installeras aldrig automatiskt, inte ens när profilen
    # ber om det. Skripten finns kvar för den som vill köra dem för hand.
    print(" ".join(tjid for tjid, t in labb.synliga_tjanster().items()
                   if t.get("steg") == "auto" or tjid in val))
SLUTPY
)

if [ -z "${AUTO// /}" ]; then
  rubrik "Inget att förinstallera"
  info "Profilen ber inte om några tjänster. Installera det du behöver i panelen."
else
  rubrik "Installerar: $AUTO"
  for tjid in $AUTO; do
    TILLSTAND=$(python3 verktyg/labb.py tillstand "$tjid" 2>/dev/null)
    case "$TILLSTAND" in
      saknas)  ./verktyg/kor.sh installera "$tjid" ;;
      arbetar) info "$tjid installeras redan någon annanstans — hoppar över" ;;
      *)       ok "$tjid: $TILLSTAND" ;;
    esac
  done
fi

# ── Starta det som är installerat ─────────────────────────────────────────
# Det profilen bad om, plus det som redan låg installerat i namnrymden från en
# tidigare podd (Eneo överlever poddomstarten, men proxyn i podden gör det
# inte). Utan det här steget ger Onyxias portlänk 502 tills någon trycker
# Starta i panelen.
STARTA=$(python3 - $PROFIL <<'SLUTPY' 2>/dev/null
import sys
sys.path.insert(0, "verktyg")
import labb
val = sys.argv[1:]
if "minimal" not in val:
    print(" ".join(tjid for tjid, t in labb.synliga_tjanster().items()
                   if t.get("starta") and (tjid in val or t.get("typ") == "lokal"
                                           and t.get("egen_ingress"))))
SLUTPY
)
for tjid in $STARTA; do
  [ "$(python3 verktyg/labb.py tillstand "$tjid" 2>/dev/null)" = "installerad" ] || continue
  rubrik "Startar $tjid"
  ./verktyg/kor.sh starta "$tjid"
done

# ── Koppla in i Eneo ──────────────────────────────────────────────────────
# Samma som knapparna "Koppla in …" i panelen. Bara när Eneo svarar och
# nyckeln till plattformens modeller finns i miljön.
if python3 -c "import sys; sys.path.insert(0,'verktyg'); import labb; sys.exit(0 if labb.eneo_uppe() else 1)" 2>/dev/null \
   && [ -n "${OPENAI_API_KEY:-}" ]; then
  rubrik "Kopplar in modeller och verktyg i Eneo"
  KOPPLA=$(python3 - $PROFIL <<'SLUTPY' 2>/dev/null
import sys
sys.path.insert(0, "verktyg")
import labb
val = sys.argv[1:]
print(" ".join(tjid for tjid, t in labb.synliga_tjanster().items()
               if t.get("koppla_eneo")
               and (tjid == "eneo" or tjid in val or t.get("typ") == "fjarr")
               and labb.status(tjid)["tillstand"] == "kor"))
SLUTPY
)
  for tjid in $KOPPLA; do ./verktyg/kor.sh koppla_eneo "$tjid"; done
elif [ -z "${OPENAI_API_KEY:-}" ]; then
  rubrik "Modellerna kopplas inte in"
  info "OPENAI_API_KEY saknas i miljön. Lägg den i Vault-hemligheten arkai-hemligheter"
  info "(docs/60-miljo/starta-labbet.md) och starta om tjänsten, eller tryck"
  info "\"Koppla in modellerna\" på Eneos kort i panelen."
fi

# ── Sammanfattning ────────────────────────────────────────────────────────
PANEL=$(python3 - <<'SLUTPY' 2>/dev/null
import sys
sys.path.insert(0, "verktyg")
import labb
print(labb.proxy_url(labb.panelport()) or f"http://127.0.0.1:{labb.panelport()}/")
SLUTPY
)

cat <<SLUT

  ── Klart ────────────────────────────────────────────────────────────────

  Panelen:  $PANEL

  Öppna den i VS Code:  Ctrl+Shift+P → "Simple Browser: Show" → klistra in URL:en
  Därifrån startar du tjänster, läser dokumentationen och ser vad som kör.

  I terminalen gör du samma sak med:
    verktyg/kor.sh lista
    verktyg/kor.sh uppsattning eneo-plattform

SLUT

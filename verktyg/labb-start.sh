#!/usr/bin/env bash
# Installerar labbet stegvis, i ett synligt terminalfönster.
#
# Körs automatiskt när VS Code öppnas (se verktyg/onyxia-init.sh), men går lika
# bra att köra för hand:
#
#   verktyg/labb-start.sh
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

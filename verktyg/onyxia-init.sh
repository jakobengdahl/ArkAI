#!/usr/bin/env bash
# Startskript för Onyxia — det som körs när tjänsten startas via labbets URL.
#
#   Fältet heter "init script" i startformuläret (init.personalInit), och tar en
#   URL till ett skript. Argument läggs i init.personalInitArgs:
#
#       init.personalInit      https://raw.githubusercontent.com/jakobengdahl/ArkAI/main/verktyg/onyxia-init.sh
#       init.personalInitArgs  bas
#
# Skriptet gör med flit ingenting tungt. Allt det gör tar ett par sekunder, för
# tjänsten blir inte tillgänglig förrän det är klart. Installationerna startas
# frånkopplat i bakgrunden och fortsätter efter att skriptet avslutats — utan
# att någon behöver öppna VS Code. Öppnar man VS Code följer terminalen samma
# körning. Se verktyg/labb-start.sh och docs/60-miljo/starta-labbet.md.
#
# Avslutar alltid med 0. Ett trasigt startskript ska inte kunna hindra tjänsten
# från att starta; panelen får i stället visa vad som saknas.
set -uo pipefail

ARBETE="${WORKSPACE_DIR:-$HOME/work}"
LABB="$ARBETE/.labb"
PROFIL="${*:-bas}"
mkdir -p "$LABB/logg" "$LABB/las" "$LABB/status"
INITLOGG="$LABB/init.log"

logg() { printf '%s  %s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$INITLOGG"; }

logg "── Startskript, profil: $PROFIL"

# ── 1. Hitta repot ────────────────────────────────────────────────────────
# Onyxia klonar normalt repot åt oss. Kör skriptet före det steget klonar vi
# själva — det är ett publikt repo, ingen token behövs.
REPO="$ARBETE/ArkAI"
if [ ! -f "$REPO/verktyg/labb.toml" ]; then
  # Djup 3: <arbetskatalog>/<repo>/verktyg/labb.toml. Har någon klonat repot
  # under ett annat namn hittas det ändå, i stället för att vi klonar en kopia.
  TRAFF=$(find "$ARBETE" -maxdepth 3 -name labb.toml -path '*/verktyg/*' 2>/dev/null | head -1)
  if [ -n "$TRAFF" ]; then
    REPO=$(dirname "$(dirname "$TRAFF")")
  else
    logg "Klonar ArkAI till $REPO"
    git clone --quiet https://github.com/jakobengdahl/ArkAI.git "$REPO" \
      >>"$INITLOGG" 2>&1 || logg "  kloningen misslyckades — panelen startas inte"
  fi
fi
logg "Repo: $REPO"

# ── 2. Skriv ner hur tjänsten startades ───────────────────────────────────
# Panelen läser det här för att kunna säga "porten du behöver exponerades inte".
{
  echo "# Skrivet av verktyg/onyxia-init.sh. Ändra inte för hand."
  echo "startad = \"$(date -Iseconds)\""
  echo "repo = \"$REPO\""
  printf 'profil = ['
  for ord in $PROFIL; do printf '"%s", ' "$ord"; done
  echo "]"
  echo "namnrymd = \"${KUBERNETES_NAMESPACE:-}\""
  echo "podd = \"${HOSTNAME:-}\""
} > "$LABB/miljo.toml"

# ── 3. Tasks som öppnar en synlig terminal när VS Code öppnas ─────────────
# Mappen VS Code öppnar är $WORKSPACE_DIR, inte repot — därför skrivs filen dit.
VSK="$ARBETE/.vscode"
mkdir -p "$VSK"
if [ -f "$VSK/tasks.json" ] && ! grep -q 'ArkAI-labbet' "$VSK/tasks.json" 2>/dev/null; then
  cp "$VSK/tasks.json" "$VSK/tasks.json.fore-arkai"
  logg "Sparade din tidigare tasks.json som tasks.json.fore-arkai"
fi
cat > "$VSK/tasks.json" <<SLUT
{
  "version": "2.0.0",
  "_kommentar": "ArkAI-labbet: genererad av verktyg/onyxia-init.sh",
  "tasks": [
    {
      "label": "Labbet: installera",
      "type": "shell",
      "command": "$REPO/verktyg/labb-start.sh --folj",
      "presentation": { "reveal": "always", "panel": "dedicated", "group": "labb", "focus": false },
      "runOptions": { "runOn": "folderOpen" },
      "problemMatcher": []
    },
    {
      "label": "Labbet: panelen",
      "type": "shell",
      "command": "$REPO/verktyg/starta-panelen.sh",
      "presentation": { "reveal": "always", "panel": "dedicated", "group": "labb", "focus": false },
      "runOptions": { "runOn": "folderOpen" },
      "problemMatcher": []
    }
  ]
}
SLUT
logg "Skrev $VSK/tasks.json"

# ── 4. Låt automatiska tasks köra utan att fråga ──────────────────────────
INST="$HOME/.local/share/code-server/User/settings.json"
if command -v jq >/dev/null 2>&1 && [ -f "$INST" ]; then
  if jq -e '."task.allowAutomaticTasks" == "on"' "$INST" >/dev/null 2>&1; then
    logg "task.allowAutomaticTasks är redan on"
  elif TMP=$(mktemp) && jq '. + {"task.allowAutomaticTasks":"on"}' "$INST" >"$TMP" 2>/dev/null \
       && [ -s "$TMP" ]; then
    cp "$INST" "$INST.fore-arkai" 2>/dev/null
    mv "$TMP" "$INST"
    logg "Satte task.allowAutomaticTasks = on"
  else
    rm -f "${TMP:-}"
    logg "Kunde inte skriva $INST — VS Code frågar då om lov första gången"
  fi
fi

# ── 5. Starta panelen och installationen ──────────────────────────────────
# Båda frånkopplade: skriptet väntar inte in dem. labb-start.sh startar själv
# panelen först, men panelen startas också direkt här — den ska vara uppe
# även om installationen fastnar.
if [ -f "$REPO/verktyg/panel/panel.py" ]; then
  ( cd "$REPO" && setsid nohup bash verktyg/starta-panelen.sh --bakgrund \
      >>"$LABB/logg/panel-start.log" 2>&1 & )
  logg "Panelen startas i bakgrunden"
fi
if [ -x "$REPO/verktyg/labb-start.sh" ]; then
  : > "$LABB/logg/labb-start.log"
  ( cd "$REPO" && setsid nohup bash verktyg/labb-start.sh \
      >>"$LABB/logg/labb-start.log" 2>&1 < /dev/null & )
  logg "Installationen startas i bakgrunden — logg: $LABB/logg/labb-start.log"
fi

logg "Klart. VS Code-terminalen följer installationen om du öppnar den."
exit 0

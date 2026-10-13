#!/usr/bin/env bash
# Installerar en egen instans av grafappen (CommunityOverview) här i podden.
#
#   verktyg/installera/graf.sh       # idempotent — kör om när du vill
#
# Appen körs från källkod, på samma commit som prod-imagen byggdes från. Allt
# ligger under ~/work och överlever en omstart av podden:
#
#   ~/work/graf-config/      schemat — redigeras i VS Code
#   ~/work/graf-data/        grafen (graph.json med journal och historik)
#   ~/work/.labb/graf/       källkod, Python-miljö och byggd frontend
#
# Varför inte som egen arbetslast i namnrymden, som Eneo: det var första
# försöket, och det föll på att klustrets lagring inte skapade någon volym
# (PVC:n stod i Pending, även en tom provvolym). Se docs/60-miljo/egen-graf.md.
# Här i podden behövs ingen ny volym — ~/work är redan en.
#
# Eneo når appen genom en Service, arkai-graf, som pekar på den här podden.
# Det kräver kubernetes.role=edit; utan den når Eneo appen bara via ingressen.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
export PATH="$HOME/.local/bin:$HOME/.local/node/bin:$PATH"

# Commiten prod-imagen (taggen latest) byggdes från, enligt imagens etikett
# org.opencontainers.image.revision. Pythonberoendena i CommunityOverview är
# inte låsta, så de löses som de såg ut när imagen byggdes (--exclude-newer).
GRAF_COMMIT="${GRAF_COMMIT:-021685b690150c87bb3b3d78d70c88539a9f4544}"
GRAF_BYGGD="${GRAF_BYGGD:-2026-09-16T06:00:00Z}"
# Profilen ~/work/graf-config fylls med första gången: default, stat-metadata, scb, test.
GRAF_PROFIL="${GRAF_PROFIL:-default}"
# torch och sentence-transformers: embeddings för nya noder. Utan dem fungerar
# appen, men semantisk sökning bara på förberäknade embeddings.
GRAF_ML="${GRAF_ML:-ja}"
ARBETE="${WORKSPACE_DIR:-$HOME/work}"
GRAF_KONFIG="${GRAF_KONFIG:-$ARBETE/graf-config}"
GRAF_DATA="${GRAF_DATA:-$ARBETE/graf-data}"
LABB="$ARBETE/.labb"
GRAF="$LABB/graf"
KOD="$GRAF/kod"
VENV="$GRAF/venv"
STAMPEL="$GRAF/installerad"
REPO_URL="https://github.com/jakobengdahl/CommunityOverview.git"

mkdir -p "$GRAF" "$GRAF_DATA"

# ── 1. Källkoden ──────────────────────────────────────────────────────────

echo "1/5  Källkoden (CommunityOverview ${GRAF_COMMIT:0:7})"
if [ "$(git -C "$KOD" rev-parse HEAD 2>/dev/null)" = "$GRAF_COMMIT" ]; then
  echo "     finns redan på rätt commit"
else
  rm -rf "$KOD" && mkdir -p "$KOD"
  git -C "$KOD" init --quiet
  git -C "$KOD" remote add origin "$REPO_URL"
  git -C "$KOD" fetch --quiet --depth 1 origin "$GRAF_COMMIT" || {
    echo "Kunde inte hämta $GRAF_COMMIT från $REPO_URL"; exit 1; }
  git -C "$KOD" checkout --quiet FETCH_HEAD
  rm -f "$STAMPEL"
  echo "     hämtad till $KOD"
fi

ONSKAT="$GRAF_COMMIT ml=$GRAF_ML"
if [ "$(cat "$STAMPEL" 2>/dev/null)" = "$ONSKAT" ] \
   && [ -x "$VENV/bin/python" ] && [ -f "$KOD/frontend/web/dist/index.html" ]; then
  echo "2/5  Python-miljön — finns redan"
  echo "3/5  Frontenden — finns redan"
else
  # ── 2. Python ───────────────────────────────────────────────────────────
  # Imagen kör Python 3.11. Podden har en nyare, så uv hämtar 3.11 till
  # hemkatalogen — samma lösning som för Open WebUI.
  echo "2/5  Python-miljön (3.11, beroenden som de var $GRAF_BYGGD)"
  command -v uv >/dev/null || { echo "uv saknas — kör: verktyg/kor.sh installera grund"; exit 1; }
  [ -x "$VENV/bin/python" ] || uv venv --quiet --python 3.11 "$VENV" || exit 1
  uv pip install --quiet --python "$VENV/bin/python" --exclude-newer "$GRAF_BYGGD" \
    -r "$KOD/backend/requirements.txt" || exit 1
  if [ "$GRAF_ML" = "ja" ]; then
    echo "     torch och sentence-transformers (CPU) — tar några minuter första gången"
    uv pip install --quiet --python "$VENV/bin/python" --exclude-newer "$GRAF_BYGGD" \
      --index-strategy unsafe-best-match -r "$KOD/backend/requirements-ml.txt" || exit 1
  fi

  # ── 3. Frontenden ───────────────────────────────────────────────────────
  # Samma två arbetsytor som imagens Dockerfile bygger, och inget mer.
  echo "3/5  Frontenden"
  command -v npm >/dev/null || { echo "npm saknas — kör: verktyg/kor.sh installera grund"; exit 1; }
  ( cd "$KOD" \
    && npm ci --ignore-scripts --no-audit --no-fund --loglevel=error \
         --workspace @community-graph/web --workspace @community-graph/widget \
         --include-workspace-root \
    && npm run --silent build:web && npm run --silent build:widget ) >"$GRAF/bygge.log" 2>&1 || {
    echo "Bygget misslyckades. Sista raderna ur $GRAF/bygge.log:"; tail -20 "$GRAF/bygge.log"; exit 1; }
  echo "$ONSKAT" > "$STAMPEL"
fi

# ── 4. Schemat ────────────────────────────────────────────────────────────
#
# Filer som redan finns rörs inte — de är någons arbete. Bara det som saknas
# kopieras, ur profilen och annars ur default, som appen själv gör.

echo "4/5  Schemat i $GRAF_KONFIG"
mkdir -p "$GRAF_KONFIG"
for fil in schema_config.json federation_config.json graph.json; do
  if [ -s "$GRAF_KONFIG/$fil" ]; then
    echo "     $fil finns, rörs inte"
    continue
  fi
  for kalla in "$GRAF_PROFIL" default; do
    # graph.json har ingen fallback: default har ingen startdata.
    [ "$fil" = "graph.json" ] && [ "$kalla" = "default" ] && [ "$GRAF_PROFIL" != "default" ] && break
    if [ -s "$KOD/config/$kalla/$fil" ]; then
      cp "$KOD/config/$kalla/$fil" "$GRAF_KONFIG/$fil"
      echo "     $fil kopierad ur profilen $kalla"
      break
    fi
  done
done
[ -s "$GRAF_KONFIG/schema_config.json" ] || { echo "Ingen schema_config.json — appen startar inte utan."; exit 1; }
[ -f "$GRAF_KONFIG/LAS-MIG.md" ] || cat > "$GRAF_KONFIG/LAS-MIG.md" <<SLUT
# Schemat för den egna grafen

Den här katalogen är grafappens konfiguration. Den skapades av
verktyg/installera/graf.sh ur profilen \`$GRAF_PROFIL\` i CommunityOverview
(commit ${GRAF_COMMIT:0:7}). Redigera filerna här — installationen skriver aldrig
över en fil som finns.

| Fil | Vad |
|---|---|
| \`schema_config.json\` | nodtyper, relationer, färger, prompter. Krävs |
| \`federation_config.json\` | federering mot andra grafer. Valfri |
| \`graph.json\` | startdata. Används **bara** när ~/work/graf-data saknar en graf |

Formatet: docs/PROFILES.md i CommunityOverview.

Ändrat schemat? Appen läser det när den startar. Starta om den: Stoppa + Starta
på grafens kort i panelen, eller tasken "Grafen: starta om (läs in schemat)".

Vill du byta ut grafen nu, mot graph.json här eller någon annan fil: öppna filen
och kör tasken "Grafen: seeda från öppen fil", eller

    verktyg/seeda-graf.sh <fil>

Det som byts ut sparas i ~/work/graf-data/arkiv/.
SLUT

# ── 5. Token och Service ──────────────────────────────────────────────────

echo "5/5  Token och vägen in för Eneo"
TOKENFIL="$LABB/graf-token"
if [ ! -s "$TOKENFIL" ]; then
  ( umask 077; openssl rand -hex 32 > "$TOKENFIL" )
  echo "     ny MCP-token i $TOKENFIL"
fi
# Servicen pekar på den podd som kör just nu — starta-graf.sh håller den aktuell.
if [ "$(kubectl auth can-i create services 2>/dev/null)" = "yes" ]; then
  verktyg/starta-graf.sh --service || exit 1
else
  echo "     rollen tillåter inte Services — Eneo når grafen bara via ingressen"
fi

echo
echo "Klart."
echo "  schema   $GRAF_KONFIG/schema_config.json"
echo "  data     $GRAF_DATA"
echo "Starta med: verktyg/kor.sh starta graf"

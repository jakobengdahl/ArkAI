#!/usr/bin/env bash
# Grundinstallation: PATH, Node och GitHub CLI — allt under ~/.local.
#
# Ingenting här kräver sudo, och ingenting installeras med apt. Det är avsiktligt:
# apt-installationer försvinner när podden startas om, medan ~/.local ligger på
# den persistenta volymen. Andra gången du startar en tjänst är det här skriptet
# därför klart på ett par sekunder.
#
# Idempotent. Kör om det när du vill.
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 1

NODE_GREN="${NODE_GREN:-latest-v24.x}"    # OpenClaw kräver Node 22.22.3+/24.15+
LOKALT="$HOME/.local"
BIN="$LOKALT/bin"
mkdir -p "$BIN"
export PATH="$BIN:$PATH"

steg() { printf '\n\033[1m%s\033[0m\n' "$*"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
hoppa(){ printf '  \033[34m·\033[0m %s\n' "$*"; }
varn() { printf '  \033[33m!\033[0m %s\n' "$*"; }

# ── PATH i ~/.bashrc ──────────────────────────────────────────────────────
steg "PATH"
if grep -q 'ArkAI: PATH' "$HOME/.bashrc" 2>/dev/null; then
  hoppa "~/.bashrc är redan uppdaterad"
else
  cat >>"$HOME/.bashrc" <<'SLUT'

# ArkAI: PATH till verktyg som installerats i hemkatalogen (överlever omstart)
export PATH="$HOME/.local/bin:$HOME/.local/node/bin:$PATH"
SLUT
  ok "~/.local/bin och ~/.local/node/bin tillagda i ~/.bashrc"
fi
export PATH="$HOME/.local/node/bin:$PATH"

# ── Node ──────────────────────────────────────────────────────────────────
steg "Node"
nodeversion() {
  command -v node >/dev/null 2>&1 || { echo 0; return; }
  node --version 2>/dev/null | tr -d 'v' | cut -d. -f1
}
if [ "$(nodeversion)" -ge 24 ] 2>/dev/null; then
  hoppa "node $(node --version) finns redan"
else
  FIL=$(curl -fsSL "https://nodejs.org/dist/$NODE_GREN/" 2>/dev/null \
        | grep -o 'node-v[0-9.]*-linux-x64\.tar\.xz' | head -1)
  if [ -z "$FIL" ]; then
    varn "Kunde inte läsa nodejs.org/dist/$NODE_GREN/ — hoppar över Node."
    varn "MCP-servrar som distribueras via npm och OpenClaw fungerar då inte."
  else
    mkdir -p "$LOKALT/node"
    if curl -fsSL "https://nodejs.org/dist/$NODE_GREN/$FIL" \
        | tar -xJ -C "$LOKALT/node" --strip-components=1; then
      ok "$("$LOKALT/node/bin/node" --version) installerad i ~/.local/node"
    else
      varn "Nedladdningen av $FIL misslyckades."
    fi
  fi
fi

# Länka in Nodes binärer i ~/.local/bin. Ett icke-interaktivt skal läser inte
# ~/.bashrc, medan ~/.profile lägger till ~/.local/bin — och det är i ett sådant
# skal som panelens sonderingar och manifestets kommandon körs. Utan länkarna
# finns node för dig i terminalen men inte för labbet.
if [ -d "$LOKALT/node/bin" ]; then
  for b in node npm npx corepack; do
    [ -e "$LOKALT/node/bin/$b" ] && ln -sf "../node/bin/$b" "$BIN/$b"
  done
  ok "node, npm och npx länkade i ~/.local/bin"
fi

# ── GitHub CLI ────────────────────────────────────────────────────────────
steg "GitHub CLI"
if command -v gh >/dev/null 2>&1; then
  hoppa "gh $(gh --version | head -1 | awk '{print $3}') finns redan"
else
  TAGG=$(curl -fsSL https://api.github.com/repos/cli/cli/releases/latest 2>/dev/null \
         | grep -m1 '"tag_name"' | cut -d'"' -f4)
  V="${TAGG#v}"
  if [ -z "$V" ]; then
    varn "Kunde inte slå upp senaste gh-versionen. Hoppar över."
  else
    TMP=$(mktemp -d)
    if curl -fsSL "https://github.com/cli/cli/releases/download/$TAGG/gh_${V}_linux_amd64.tar.gz" \
        | tar -xz -C "$TMP" --strip-components=1; then
      install -m 755 "$TMP/bin/gh" "$BIN/gh"
      mkdir -p "$LOKALT/share/man/man1"
      cp -r "$TMP/share/man/man1/." "$LOKALT/share/man/man1/" 2>/dev/null || true
      ok "gh $V installerad i ~/.local/bin"
    else
      varn "Nedladdningen av gh $V misslyckades."
    fi
    rm -rf "$TMP"
  fi
fi

# ── Git-autentisering ─────────────────────────────────────────────────────
steg "Git"
if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    hoppa "gh är redan inloggad som $(gh api user --jq .login 2>/dev/null)"
  else
    ./verktyg/satt-upp-git-auth.sh >/dev/null 2>&1 \
      && ok "gh inloggad, token borta ur remote-URL:en" \
      || varn "Automatisk inloggning gick inte. Kör ./verktyg/satt-upp-git-auth.sh"
  fi
else
  varn "gh saknas — hoppar över git-autentiseringen."
fi

steg "Klart"
echo "  Grundmiljön är på plats. Öppna en ny terminal för att få rätt PATH,"
echo "  eller kör:  export PATH=\"\$HOME/.local/bin:\$HOME/.local/node/bin:\$PATH\""

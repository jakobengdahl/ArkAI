#!/usr/bin/env bash
# Installerar Open WebUI som ett uv-verktyg under ~/.local.
#
# Tar ~4 minuter första gången. Kör i bakgrunden eller i en egen terminal —
# ingenting annat i labbet behöver vänta på det.
#
# Open WebUI kräver Python 3.11; imagen har 3.13. uv hämtar rätt version utan
# att röra systemets Python. Se minnesbanken.
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"

if command -v open-webui >/dev/null 2>&1; then
  echo "open-webui finns redan ($(open-webui --version 2>/dev/null | head -1))."
  echo "Tvinga ominstallation med: uv tool install --force --python 3.11 open-webui"
  exit 0
fi

command -v uv >/dev/null || { echo "uv saknas — det ska finnas i imagen."; exit 1; }

echo "1/2  Hämtar Python 3.11 (imagen har $(python3 -V | awk '{print $2}'))"
uv python install 3.11 || exit 1

echo "2/2  Installerar open-webui — det här är den långa delen"
uv tool install --python 3.11 open-webui || exit 1

echo
echo "Klart: $(command -v open-webui)"
echo "Starta med: verktyg/kor.sh starta openwebui"

#!/usr/bin/env bash
# Startar labbpanelen.
#
#   verktyg/starta-panelen.sh              # förgrunden, eller följ loggen om den redan kör
#   verktyg/starta-panelen.sh --bakgrund
#   verktyg/starta-panelen.sh --stoppa
#
# Panelen binder till 127.0.0.1 med flit. Den kan starta processer, och ska
# därför bara gå att nå av den som har den här VS Code-sessionen — via
# code-servers proxy. Se docs/60-miljo/panelen.md.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
export PATH="$HOME/.local/bin:$PATH"

LABB="${LABB_DIR:-${WORKSPACE_DIR:-$HOME/work}/.labb}"
LOGG="$LABB/logg/panel.log"
mkdir -p "$LABB/logg"

PORT=$(python3 -c "
import sys; sys.path.insert(0,'verktyg'); import labb; print(labb.panelport())" 2>/dev/null || echo 8082)

kor() { timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/$PORT" 2>/dev/null; }

if [ "${1:-}" = "--stoppa" ]; then
  pkill -f "panel/panel.py" && echo "Panelen stoppad." || echo "Panelen körde inte."
  exit 0
fi

# Två startare kan komma samtidigt: onyxia-init.sh startar panelen och
# labb-start.sh direkt efter varandra, och båda anropar det här skriptet. Utan
# lås ser båda att porten är ledig innan någon hunnit binda den, och båda
# startar. Den som förlorar har dessutom kunnat bli hängande på uv:s cachelås
# medan installationerna körde, och dog långt senare med "Address already in
# use" i loggen. Låset hålls tills panelen svarar; panelen själv ärver det inte.
exec 9>"$LABB/panel-start.lock"
flock -w 30 9 || true

if kor; then
  exec 9>&-
  echo "Panelen kör redan på port $PORT."
  python3 -c "
import sys; sys.path.insert(0,'verktyg'); import labb
u = labb.proxy_url($PORT)
print('  ' + (u or 'http://127.0.0.1:$PORT/'))"
  # I bakgrundsläge (från startskriptet) ska vi bara konstatera det och avsluta.
  # Kör någon skriptet för hand är det däremot loggen hen vill se.
  [ "${1:-}" = "--bakgrund" ] && exit 0
  echo
  echo "Följer loggen. Ctrl+C avslutar följningen — panelen fortsätter köra."
  exec tail -n 20 -f "$LOGG"
fi

if [ "${1:-}" = "--bakgrund" ]; then
  setsid nohup uv run --quiet verktyg/panel/panel.py >>"$LOGG" 2>&1 9>&- &
  for _ in $(seq 1 20); do
    sleep 0.5
    kor && { echo "Panelen kör på port $PORT. Logg: $LOGG"; exit 0; }
  done
  echo "Panelen svarade inte. Kolla loggen: tail -30 $LOGG"
  exit 1
fi

exec 9>&-
exec uv run --quiet verktyg/panel/panel.py

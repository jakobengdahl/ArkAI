#!/usr/bin/env bash
# Installerar Eneo som riktiga tjänster i namnrymden.
#
# Eneo dokumenterar bara docker compose, och det finns ingen containerruntime i
# labbtjänsten. Det här skriptet gör i stället samma sak med kubectl: databas,
# kö, migrering, backend, worker och frontend som egna arbetslaster, plus en
# Caddy i den här podden som lägger frontend och backend på *samma* origin.
#
# Tar 10–15 minuter första gången — imagerna är stora och migreringen tar tid.
# Kör om den när du vill: allt är idempotent, och hemligheterna skapas bara en
# gång.
#
# Kräver att tjänsten startades med kubernetes.role=edit och port 8084
# exponerad. Ingetdera går att ändra i efterhand — se docs/60-miljo/eneo.md.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"
export PATH="$HOME/.local/bin:$PATH"

# Imagerna är pinnade till digesterna som taggen 2.2.2 pekade på när vi bytte
# (taggen i GHCR saknar "v", till skillnad från releasen på GitHub). En digest
# kan inte flyttas.
#
# Byte från 2.1.x till 2.2.x är inte ett digestbyte: 2.2 kräver en
# engångsmigrering av fil- och ikoninnehåll med stoppade tjänster. Vi har inte
# provat den vägen — vi tog bort och installerade om. Se docs/60-miljo/eneo.md.
ENEO_VERSION="2.2.2"
BACKEND_IMAGE="ghcr.io/eneo-ai/eneo-backend@sha256:2a332becf682875da6dbf3c7482176c6cb3971bac44cf897f9a58620e7c8d22a"
FRONTEND_IMAGE="ghcr.io/eneo-ai/eneo-frontend@sha256:97b833c54b937635054e60c1f67c955efff8684df76dd71e1ceb78fbc630d005"
DB_IMAGE="pgvector/pgvector:pg16"
REDIS_IMAGE="redis:7-alpine"
DB_STORLEK="${ENEO_DB_STORLEK:-20Gi}"
CADDY_VERSION="2.11.4"
ENEO_PORT="${ENEO_PORT:-8084}"
# Inloggningen är medvetet enkel och står i klartext här: labbet har en enda
# användare, och ett slumpat lösenord i en fil utanför repot var mest i vägen.
# Porten är däremot publik — se docs/60-miljo/eneo.md. Sätt ENEO_ADMIN_EPOST och
# ENEO_ADMIN_LOSEN före installationen om du vill ha något annat.
#
# Sedan 2.2 kräver Eneo minst 12 tecken. Ett kortare lösenord stoppar inte
# migreringen — init_db.py loggar felet och avslutar ändå med 0, och då finns
# det ingen användare att logga in med. Därför kontrolleras loggen i steg 5.
ADMIN_EPOST="${ENEO_ADMIN_EPOST:-arkai@arkai.se}"
ADMIN_NAMN="${ENEO_ADMIN_NAMN:-arkai}"
ADMIN_LOSEN="${ENEO_ADMIN_LOSEN:-arkai@arkai.se}"

export ENEO_VERSION BACKEND_IMAGE FRONTEND_IMAGE DB_IMAGE REDIS_IMAGE \
       DB_STORLEK ADMIN_EPOST ADMIN_NAMN

rendera() {  # rendera <mallfil> — skriver färdig yaml till stdout
  python3 - "$1" <<'PY'
import os, pathlib, string, sys
mall = pathlib.Path(sys.argv[1]).read_text()
sys.stdout.write(string.Template(mall).substitute(os.environ))
PY
}

# ── 1. Förutsättningar ────────────────────────────────────────────────────

echo "1/6  Kontrollerar förutsättningarna"

command -v kubectl >/dev/null || { echo "kubectl saknas — det ska finnas i imagen."; exit 1; }

if [ "$(kubectl auth can-i create deployments 2>/dev/null)" != "yes" ]; then
  cat <<'MEDD'
Tjänsten är startad med Kubernetes-rollen view, och då går det inte att
deploya något. Rollen sätts när tjänsten startar och går inte att ändra i
efterhand — starta en ny tjänst med kubernetes.role=edit.
Start-URL:en står i docs/60-miljo/eneo.md.
MEDD
  exit 1
fi

PUBLIC_ORIGIN="$(python3 verktyg/labb.py ingress "$ENEO_PORT" 2>/dev/null)"
PUBLIC_ORIGIN="${PUBLIC_ORIGIN%/}"
if [ -z "$PUBLIC_ORIGIN" ]; then
  cat <<MEDD
Port $ENEO_PORT är inte exponerad i den här tjänsten. Eneo behöver ett publikt
värdnamn: både inloggningen och frontendens SSR bygger URL:er av det.
Portar exponeras när tjänsten startar — se docs/60-miljo/eneo.md.
MEDD
  exit 1
fi
export PUBLIC_ORIGIN
echo "     roll edit, port $ENEO_PORT exponerad"
echo "     Eneo kommer att ligga på $PUBLIC_ORIGIN"

# ── 2. Caddy ──────────────────────────────────────────────────────────────

echo "2/6  Proxyn (Caddy $CADDY_VERSION)"
if command -v caddy >/dev/null 2>&1; then
  echo "     finns redan: $(caddy version | head -1)"
else
  mkdir -p "$HOME/.local/bin"
  URL="https://github.com/caddyserver/caddy/releases/download/v${CADDY_VERSION}/caddy_${CADDY_VERSION}_linux_amd64.tar.gz"
  curl -fsSL "$URL" | tar -xz -C "$HOME/.local/bin" caddy || {
    echo "Kunde inte hämta Caddy från $URL"; exit 1; }
  chmod +x "$HOME/.local/bin/caddy"
  echo "     installerad i ~/.local/bin — överlever en omstart av podden"
fi

# ── 3. Hemligheter ────────────────────────────────────────────────────────
#
# Skapas en gång. Ligger de redan i namnrymden rör vi dem inte: databasen är
# krypterad med ENCRYPTION_KEY, och ett nytt värde gör gamla modellnycklar
# oläsbara.

echo "3/6  Hemligheter"
if kubectl get secret eneo-hemligheter >/dev/null 2>&1; then
  echo "     eneo-hemligheter finns redan — lämnas orörd"
else
  kubectl create secret generic eneo-hemligheter \
    --from-literal=POSTGRES_PASSWORD="$(openssl rand -hex 16)" \
    --from-literal=JWT_SECRET="$(openssl rand -hex 32)" \
    --from-literal=URL_SIGNING_KEY="$(openssl rand -hex 32)" \
    --from-literal=ENCRYPTION_KEY="$(python3 -c 'import base64,os;print(base64.urlsafe_b64encode(os.urandom(32)).decode())')" \
    --from-literal=ENEO_SUPER_API_KEY="$(openssl rand -hex 32)" \
    --from-literal=DEFAULT_USER_PASSWORD="$ADMIN_LOSEN" >/dev/null || exit 1
  kubectl label secret eneo-hemligheter app.kubernetes.io/part-of=eneo >/dev/null

  echo "     skapade eneo-hemligheter"
fi

# ── 4. Databas och kö ─────────────────────────────────────────────────────

echo "4/6  Databas och kö"
rendera verktyg/eneo/01-data.yaml | kubectl apply -f - || exit 1
echo "     väntar på att postgres och redis svarar (första gången: bildhämtning)"
kubectl rollout status statefulset/eneo-db --timeout=900s || exit 1
kubectl rollout status statefulset/eneo-redis --timeout=600s || exit 1

# ── 5. Migrering och första användaren ────────────────────────────────────
#
# Jobbet är immutabelt i Kubernetes, så ett gammalt måste bort innan ett nytt
# kan läggas på. init_db.py är säker att köra om — finns tenant och användare
# redan hoppar den över dem.

echo "5/6  Migrering och första användaren"
kubectl delete job eneo-db-init --ignore-not-found >/dev/null
rendera verktyg/eneo/02-init.yaml | kubectl apply -f - || exit 1
if ! kubectl wait --for=condition=complete job/eneo-db-init --timeout=900s; then
  echo
  echo "Migreringen blev inte klar. Loggen:"
  kubectl logs job/eneo-db-init --tail=40
  exit 1
fi
if kubectl logs job/eneo-db-init 2>/dev/null | grep -q "Error adding tenant and user"; then
  echo
  echo "Migreringen gick igenom, men första användaren skapades inte:"
  kubectl logs job/eneo-db-init | grep "Error adding tenant and user"
  echo "Rätta DEFAULT_USER_PASSWORD i eneo-hemligheter (eller ENEO_ADMIN_LOSEN"
  echo "före en ny installation) och kör installationen igen."
  exit 1
fi

# ── 6. Backend, worker och frontend ───────────────────────────────────────

echo "6/6  Backend med worker, och frontend"
rendera verktyg/eneo/03-app.yaml | kubectl apply -f - || exit 1
kubectl rollout status deployment/eneo-backend --timeout=900s || exit 1
kubectl rollout status deployment/eneo-frontend --timeout=600s || exit 1

echo
echo "Klart. Tjänsterna kör i namnrymden:"
kubectl get pods -l app.kubernetes.io/part-of=eneo \
  -o custom-columns=NAMN:.metadata.name,STATUS:.status.phase,STARTAD:.status.startTime
echo
echo "Logga in på $PUBLIC_ORIGIN med"
echo "  e-post    $ADMIN_EPOST"
echo "  lösenord  $ADMIN_LOSEN"
echo
echo "Starta proxyn och öppna gränssnittet med:"
echo "  verktyg/kor.sh starta eneo"

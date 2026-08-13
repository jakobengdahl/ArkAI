#!/usr/bin/env bash
# Installerar OpenClaw — en självhostad gateway som kopplar agenter till
# verktyg, filer och kanaler.
#
# Den finns här som experimentobjekt, inte som byggkloss. Kontrasten mot
# Open WebUI är poängen: samma modell och samma MCP-verktyg, men agenten når
# filsystem och kommandon och kan drivas utifrån i stället för av någon som
# sitter vid ett chattfönster.
#
# Kanaldelen (WhatsApp, Slack, Telegram …) lämnar vi utanför labbet.
set -uo pipefail
export PATH="$HOME/.local/bin:$HOME/.local/node/bin:$PATH"

if command -v openclaw >/dev/null 2>&1; then
  echo "openclaw finns redan ($(openclaw --version 2>/dev/null | head -1))."
  exit 0
fi

# OpenClaw kräver Node 22.22.3+ / 24.15+ (26 rekommenderas av projektet).
MAJOR=$(node --version 2>/dev/null | tr -d 'v' | cut -d. -f1)
if [ -z "${MAJOR:-}" ] || [ "$MAJOR" -lt 24 ] 2>/dev/null; then
  echo "Node 24 eller senare krävs (hittade: ${MAJOR:-inget})."
  echo "Kör först: verktyg/installera/bas.sh"
  exit 1
fi

# Installationsskriptet hämtas från projektet och körs. Läs det först om du är
# osäker:  curl -fsSL https://openclaw.ai/install.sh | less
curl -fsSL https://openclaw.ai/install.sh | bash || exit 1

echo
echo "Klart. Nästa steg görs interaktivt och kräver att du väljer modell:"
echo "  openclaw onboard"
echo
echo "Peka den mot plattformens LLM-API när den frågar efter leverantör:"
echo "  bas-URL   \$OPENAI_BASE_URL   (sätts av Vault-hemligheten)"
echo "  modell    \$OPENAI_MODEL"
echo
echo "Starta sedan gatewayen: verktyg/kor.sh starta openclaw"

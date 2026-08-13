#!/usr/bin/env bash
# Installerar mcpo — bryggan som gör MCP-servrar tillgängliga som OpenAPI.
#
# Open WebUI pratar verktygsservrar över OpenAPI, inte MCP. Utan den här
# bryggan går det inte att koppla in våra MCP-servrar i chatten. Att det
# behövs ett mellanlager är i sig värt att notera när man jämför tekniker.
set -uo pipefail
export PATH="$HOME/.local/bin:$PATH"

if command -v mcpo >/dev/null 2>&1; then
  echo "mcpo finns redan ($(command -v mcpo))."
  exit 0
fi

command -v uv >/dev/null || { echo "uv saknas — det ska finnas i imagen."; exit 1; }

# mcp<2 är inte kosmetiskt: mcpo importerar streamablehttp_client, som flyttades
# i MCP:s Python-SDK 2.0. Utan pinningen installeras 2.0 och mcpo kraschar med
# ImportError vid start. Se minnesbanken (mcp-sdk-2-bytte-api).
uv tool install mcpo --with "mcp<2" || exit 1

echo
echo "Klart: $(command -v mcpo)"
echo "Bryggan läser ~/work/.labb/mcp.json och exponerar det som finns där."

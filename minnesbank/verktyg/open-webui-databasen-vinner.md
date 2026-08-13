---
namn: open-webui-databasen-vinner
beskrivning: Open WebUI läser miljövariabler bara när databasen saknar värdet — efter första starten är det databasen som gäller.
typ: verktyg
uppdaterad: 2026-08-13
---

Open WebUI:s konfiguration är beständig i databasen. Miljövariabler som
`OPENAI_API_BASE_URL`, `OPENAI_API_KEY` och `TOOL_SERVER_CONNECTIONS` används som
**förval första gången** — finns nyckeln redan i tabellen `config` i `webui.db`
läses miljön inte om, hur många gånger du än startar om.

**Varför:** vi förkonfigurerade modellkopplingen med miljövariabler och den slog
igenom direkt. När hemligheten sedan ändrades hände ingenting vid omstart, och
det såg ut som att startskriptet var trasigt. Det var det inte — värdet låg redan
i databasen. Samma sak gäller verktygsservrar som läggs till efter första starten.

**Så använder du det:** `verktyg/konfigurera-openwebui.py` gör båda delarna.
`--env` ger export-rader för den första starten, `--skriv` skriver direkt i
`webui.db` för alla följande. Startskriptet kör båda, och panelen har knappen
*Koppla in* för att göra om det när du installerat en ny MCP-server eller bytt
nyckel. Nycklarna i `config`-tabellen: `openai.enable`, `openai.api_base_urls`,
`openai.api_keys`, `ui.default_models`, `tool_server.connections` — verifierade
mot `open_webui/config.py`, och de har bytt namn förr.

Relaterat: [[open-webui-pratar-inte-mcp]], [[api-nycklar-i-hemkatalogen]]

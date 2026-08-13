---
namn: open-webui-pratar-inte-mcp
beskrivning: Open WebUI kopplar in verktyg som OpenAPI-servrar, inte som MCP — det krävs en brygga (mcpo) för att nå våra MCP-servrar därifrån.
typ: verktyg
uppdaterad: 2026-08-13
---

Open WebUI kan inte prata MCP direkt. Dess verktygsstöd bygger på **OpenAPI**-
servrar, så en MCP-server måste gå via en brygga — `mcpo` — som översätter.
Räkna med ett mellanlager när du planerar ett upplägg där chatten ska nå våra
egna verktyg.

**Varför:** det är lätt att anta att "MCP är standarden" betyder att allt talar
MCP. Antagandet gjorde att uppsättningen "chattbot + verktyg" först saknade en
komponent. Kodagenter (Claude Code, opencode) och agent-gateways talar MCP direkt;
chattgränssnitt gör det inte nödvändigtvis.

**Så använder du det:** `verktyg/kor.sh installera mcpo`, och peka Open WebUI mot
`http://127.0.0.1:8083`. Bryggan läser `~/work/.labb/mcp.json`, som genereras ur
`verktyg/labb.toml` och speglar vad som faktiskt kör.

**mcpo kräver `mcp<2`.** Installerar du utan pinning drar uv in MCP-SDK 2.0 och
mcpo kraschar direkt med `ImportError: cannot import name 'streamablehttp_client'`.
Verifierat 2026-08-13. Installationsskriptet kör därför
`uv tool install mcpo --with "mcp<2"`.

**Så långt är det verifierat:** bryggan startar och exponerar hello-mcps tre
verktyg som OpenAPI-slutpunkter (`/lista_minnen`, `/las_minne`, `/sok_minnen` på
`http://127.0.0.1:8083/hello-mcp/`). Att Open WebUI faktiskt anropar dem och
låter modellen använda svaret är ännu inte provat — skriv ner det när någon gjort
det.

Relaterat: [[mcp-sdk-2-bytte-api]]

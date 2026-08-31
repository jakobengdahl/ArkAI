---
namn: eneo-mcp-kraver-streamable-http
beskrivning: Eneo kopplar bara in MCP-servrar över Streamable HTTP, och når bara det som ligger på en exponerad port.
typ: verktyg
uppdaterad: 2026-08-31
---

Eneo har inga verktyg från början. Adminen lägger upp MCP-servrar per organisation,
och två saker begränsar vad som går att lägga upp:

**Bara Streamable HTTP.** DTO:n heter `MCPServerCreate` och tar `http_url` — det
finns ingen stdio och ingen SSE. En stdio-server måste alltså köras över HTTP för
att gå att koppla in. `/mcp/sse` svarar 405 på den POST Eneo gör.

**Bara det Eneos egen podd når.** Eneo kör som arbetslaster i namnrymden, inte i
VS Code-podden. `127.0.0.1` betyder Eneos podd, inte din — en server här måste
ligga på en exponerad port, alltså ett publikt värdnamn, och behöver då en token.

**Varför:** Hello-MCP pratade bara stdio, vilket räcker för Claude Code och
Continue eftersom de startar servern själva. Eneo gör inte det, och felet syns
först som "0 verktyg hittade" — inte som ett anslutningsfel.

**Så använder du det:** token läggs i `http_auth_config_schema` som
`{"token": "…"}` med `http_auth_type: "bearer"`. Svaret på skapandet innehåller
`connection.tools_discovered`, som är det enda kvittot på att Eneo verkligen nådde
servern — noll verktyg betyder att den inte gjorde det.
`verktyg/koppla-mcp-till-eneo.py` gör det och skriver ut siffran.

En server som redan kör någon annanstans kan mycket väl ha båda transporterna på
olika sökvägar: metadatagrafen svarar på `/mcp/sse` för SSE-klienter och `/mcp/`
för Streamable HTTP. Prova roten innan du drar slutsatsen att den inte går att
koppla in.

Relaterat: [[exponerad-port-kraver-inloggning]], [[mcp-sdk-2-bytte-api]],
[[namnrymden-overlever-podden]], [[open-webui-pratar-inte-mcp]]

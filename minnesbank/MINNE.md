# Minnesindex

Läses först. En rad per post. Hämta enskilda poster vid behov — lägg inte in hela
minnesbanken i kontexten.

Håll raderna korta och sorterade under sin rubrik. Lägg till en rad när du lägger till
en fil; ta bort raden när du tar bort filen.

## Arbetssätt

- [Skriv ner det som inte funkade](arbetssatt/dokumentera-negativa-resultat.md) — negativa resultat är billigare att läsa än att upprepa
- [Index först, detaljer vid behov](arbetssatt/index-fore-innehall.md) — hur vi lägger kunskap i kontexten utan att fylla den

## Verktyg och miljö

- [Behörigheter sätts när tjänsten startar](verktyg/onyxia-behorigheter-satts-vid-start.md) — k8s-roll, portar, AI-assistent. Starta om hellre än att kämpa emot
- [Port 8080 är upptagen i Onyxia-tjänster](verktyg/onyxia-port-8080-upptagen.md) — code-server sitter där, använd 8081+
- [Onyxia bakar in git-token i remote-URL:en](verktyg/onyxia-token-i-remote-url.md) — flytta den till gh:s credential helper
- [API-nycklar ligger i klartext i hemkatalogen](verktyg/api-nycklar-i-hemkatalogen.md) — rensa innan du delar konfigurationsfiler
- [SSP Cloud har egen LLM-inferens](verktyg/sspcloud-llm-inferens.md) — OpenAI-kompatibelt API, personlig nyckel
- [Open WebUI kräver Python 3.11](verktyg/openwebui-kraver-python-311.md) — imagen har 3.13, lös det med uv
- [Webbappar fungerar inte bakom code-servers /proxy/](verktyg/spa-fungerar-inte-bakom-sokvagsproxy.md) — exponera porten med eget värdnamn vid start
- [Query-strängen överlever proxyn](verktyg/query-strang-overlever-proxyn.md) — bygger du själv slipper du portexponering helt
- [MCP:s Python-SDK bytte API i 2.0](verktyg/mcp-sdk-2-bytte-api.md) — FastMCP heter MCPServer, nätets exempel är föråldrade
- [Open WebUI pratar inte MCP](verktyg/open-webui-pratar-inte-mcp.md) — verktyg kopplas in som OpenAPI, det krävs en brygga
- [Startskriptet får inte blockera](verktyg/startskript-far-inte-blockera.md) — installationer hör hemma i en synlig VS Code-terminal, inte i init.personalInit
- [Installera i hemkatalogen, inte med apt](verktyg/installera-i-hemkatalogen-inte-med-apt.md) — Node och gh som tarball i ~/.local överlever omstart
- [Sondera tillstånd, läs det inte](verktyg/sondera-tillstand-las-det-inte.md) — statusfiler ljuger efter en poddomstart

## Domänkunskap

*(tomt — skriv avidentifierat, se [RIKTLINJER-INNEHALL.md](../RIKTLINJER-INNEHALL.md))*

## Beslut

- [Repot är publikt](beslut/publikt-repo.md) — vad det innebär för vad vi skriver

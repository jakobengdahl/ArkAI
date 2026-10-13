# Minnesindex

Läses först. En rad per post. Hämta enskilda poster vid behov — lägg inte in hela
minnesbanken i kontexten.

Håll raderna korta och sorterade under sin rubrik. Lägg till en rad när du lägger till
en fil; ta bort raden när du tar bort filen.

## Arbetssätt

- [Skriv ner det som inte funkade](arbetssatt/dokumentera-negativa-resultat.md) — negativa resultat är billigare att läsa än att upprepa
- [Index först, detaljer vid behov](arbetssatt/index-fore-innehall.md) — hur vi lägger kunskap i kontexten utan att fylla den
- [Utforskande spår lämnar över](arbetssatt/utforskande-spar-lamnar-over.md) — i någon annans verksamhet slutar vi i ett underlag, aldrig i ett förslag

## Verktyg och miljö

- [Behörigheter sätts när tjänsten startar](verktyg/onyxia-behorigheter-satts-vid-start.md) — k8s-roll, portar, AI-assistent. Starta om hellre än att kämpa emot
- [Port 8080 är upptagen i Onyxia-tjänster](verktyg/onyxia-port-8080-upptagen.md) — code-server sitter där, använd 8081+
- [Onyxia bakar in git-token i remote-URL:en](verktyg/onyxia-token-i-remote-url.md) — flytta den till gh:s credential helper
- [API-nycklar ligger i klartext i hemkatalogen](verktyg/api-nycklar-i-hemkatalogen.md) — rensa innan du delar konfigurationsfiler
- [SSP Cloud har egen LLM-inferens](verktyg/sspcloud-llm-inferens.md) — OpenAI-kompatibelt API, personlig nyckel
- [Kontextlängden syns bara i felmeddelandet](verktyg/kontextlangd-syns-bara-i-felet.md) — /models säger inget, för hög max_tokens avslöjar max_model_len
- [Open WebUI kräver Python 3.11](verktyg/openwebui-kraver-python-311.md) — imagen har 3.13, lös det med uv
- [Webbappar fungerar inte bakom code-servers /proxy/](verktyg/spa-fungerar-inte-bakom-sokvagsproxy.md) — exponera porten med eget värdnamn vid start
- [Query-strängen överlever proxyn](verktyg/query-strang-overlever-proxyn.md) — bygger du själv slipper du portexponering helt
- [MCP:s Python-SDK bytte API i 2.0](verktyg/mcp-sdk-2-bytte-api.md) — FastMCP heter MCPServer, nätets exempel är föråldrade
- [Open WebUI pratar inte MCP](verktyg/open-webui-pratar-inte-mcp.md) — verktyg kopplas in som OpenAPI, det krävs en brygga
- [Eneo kopplar bara in MCP över Streamable HTTP](verktyg/eneo-mcp-kraver-streamable-http.md) — inte stdio, inte SSE, och bara det Eneos egen podd når
- [Eneos backend och worker måste dela /tmp](verktyg/eneo-backend-och-worker-delar-tmp.md) — uppladdningen lämnas över som en sökväg, separata poddar ger tyst fel
- [Open WebUI:s databas vinner över miljön](verktyg/open-webui-databasen-vinner.md) — miljövariabler gäller bara första starten, sedan är det webui.db
- [Startskriptet får inte blockera](verktyg/startskript-far-inte-blockera.md) — installationer hör hemma i en synlig VS Code-terminal, inte i init.personalInit
- [Installera i hemkatalogen, inte med apt](verktyg/installera-i-hemkatalogen-inte-med-apt.md) — Node och gh som tarball i ~/.local överlever omstart
- [Sondera tillstånd, läs det inte](verktyg/sondera-tillstand-las-det-inte.md) — statusfiler ljuger efter en poddomstart
- [Exponerad port kräver inloggning](verktyg/exponerad-port-kraver-inloggning.md) — publikt värdnamn, och Open WebUI godtar bara värdet True
- [CSS-variabler i SVG blir svarta bilder](verktyg/svg-css-variabler-blir-svarta.md) — figurernas färger hör hemma i presentationsattribut
- [En ingressregel per exponerad port](verktyg/en-ingress-regel-per-port.md) — flera portar delar ingress, ett värdnamn per regel
- [Två portar är två origins](verktyg/tva-portar-ar-tva-origins.md) — frontend och API hör ihop, proxya på sökväg i podden
- [Förbjudet är inte samma sak som saknas](verktyg/forbjudet-ar-inte-saknat.md) — klusterbreda kubectl-frågor svarar Forbidden, fråga med api-resources
- [Namnrymden överlever podden](verktyg/namnrymden-overlever-podden.md) — det du deployat kör vidare och äter kvot när tjänsten stoppas
- [Namnrymden delas med andras grafer](verktyg/namnrymden-delas-med-andras-grafer.md) — våra resurser heter arkai-*, ta bort på etikett, aldrig på namn
- [En ny volym kan fastna i Pending](verktyg/ny-volym-kan-fastna-i-pending.md) — klustrets provisioner, inte manifestet. Prova en provvolym, bygg hellre på ~/work

## Domänkunskap

*(tomt — skriv avidentifierat, se [RIKTLINJER-INNEHALL.md](../RIKTLINJER-INNEHALL.md))*

## Beslut

- [Repot är publikt](beslut/publikt-repo.md) — vad det innebär för vad vi skriver

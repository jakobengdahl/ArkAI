# hello-mcp

En minimal MCP-server som exponerar [minnesbanken](../../../minnesbank/) för
AI-verktyg. Tänkt att läsas, köras och kopieras.

Servern har tre verktyg, som tillsammans visar mönstret nästan alla nyttiga
MCP-servrar följer:

| Verktyg | Vad det gör |
|---|---|
| `lista_minnen()` | Ge modellen en billig överblick — indexet |
| `sok_minnen(sokord)` | Hitta rätt post |
| `las_minne(namn)` | Hämta en enskild post i sin helhet |

Poängen är uppdelningen: **modellen får veta vad som finns utan att allt läggs i
kontexten**, och hämtar sedan det den behöver. Samma princip som minnesbanken själv
bygger på — se
[index före innehåll](../../../minnesbank/arbetssatt/index-fore-innehall.md).

En server som i stället hade haft ett enda `hamta_hela_minnesbanken()` hade varit
enklare att skriva och sämre att använda.

## Kör

```bash
cd exempel/mcp/hello-mcp
uv sync
uv run python server.py --lista     # snabbtest utan MCP-klient
uv run python server.py             # som MCP-server över stdio
```

Eller, med labbets vanliga knappar och lås:

```bash
verktyg/kor.sh installera hello-mcp
verktyg/kor.sh starta hello-mcp        # HTTP-läget, port 8081
verktyg/kor.sh koppla_eneo hello-mcp   # lägger upp den som verktygsserver i Eneo
verktyg/kor.sh stoppa hello-mcp
```

`--lista` anropar funktionerna direkt. Använd det när du ändrat något — det är
mycket snabbare än att felsöka via en klient.

Startar du den utan flaggor ser det ut som att den hängt sig. Den väntar på
JSON-RPC på stdin, vilket är precis vad den ska göra.

## Koppla in i ett verktyg

Sökvägarna nedan förutsätter att repot ligger i `/home/onyxia/work/ArkAI`.

### Continue (finns i Onyxias image)

Lägg till i `~/.continue/config.yaml` under `mcpServers`. Där finns redan en
DuckDB-server som du kan använda som förlaga:

```yaml
mcpServers:
  - name: ArkAI-minnesbank
    command: uv
    args:
      - --directory
      - /home/onyxia/work/ArkAI/exempel/mcp/hello-mcp
      - run
      - python
      - server.py
```

### Claude Code

```bash
claude mcp add arkai-minnesbank -- \
  uv --directory /home/onyxia/work/ArkAI/exempel/mcp/hello-mcp run python server.py
```

### opencode

Se konfigurationsformatet i `~/.config/opencode/opencode.jsonc` och
[opencode.ai](https://opencode.ai).

### Eneo — och därför HTTP-läget

Eneo kör i namnrymden, inte i den här podden, och kan därför inte starta servern
åt sig. Den pratar dessutom **bara Streamable HTTP** — varken stdio eller SSE. Det
är hela skälet till att servern har två transporter:

```bash
verktyg/starta-hello-mcp.sh --bakgrund
```

Skriptet startar `server.py --http`, som lyssnar på port 8081 och lägger
MCP-slutpunkten på `/mcp`. Tre saker skiljer HTTP-läget från stdio-läget:

- **Token krävs.** Porten är exponerad, alltså ett publikt värdnamn. Servern vägrar
  starta utan `HELLO_MCP_TOKEN`, och startskriptet skapar den i
  `~/work/.labb/hello-mcp-token` (läge 0600) första gången.
- **Host-huvudet kontrolleras.** MCP-SDK:n skyddar mot DNS-rebinding genom att
  jämföra `Host` mot en lista. Bakom en ingress är värdnamnet inte vårt eget, så
  startskriptet skickar med det.
- **Ingen session.** `stateless_http=True` — varje anrop står för sig, så en klient
  bakom en proxy inte behöver hamna på samma process två gånger.

`/halsa` svarar utan token, så att panelen kan se om servern lever utan att ha
tokenet.

Att koppla in den i Eneo är sedan ett kommando:

```bash
verktyg/kor.sh koppla_eneo hello-mcp
```

Se [docs/60-miljo/eneo.md](../../../docs/60-miljo/eneo.md#verktyg-mcp-i-eneo).

## Vad som är värt att titta på i koden

**Docstringarna är prompten.** Det är dem modellen läser för att avgöra om ett
verktyg ska användas och med vilka argument. Skriv dem för en läsare som ska välja
verktyg, inte för en utvecklare som ska underhålla koden. En vag docstring är den
vanligaste orsaken till att en MCP-server "inte fungerar".

**Verktygen returnerar text, inte datastrukturer.** Det som kommer tillbaka hamnar i
modellens kontext. Håll det kort och läsbart.

**Felmeddelanden är också prompt.** `las_minne` svarar "Ingen post heter X. Kör
lista_minnen för att se vad som finns" i stället för att kasta ett undantag — då kan
modellen rätta sig själv i stället för att gissa vidare.

## Fallgrop: SDK:n bytte API i 2.0

Nästan alla exempel du hittar på nätet importerar `FastMCP`:

```python
from mcp.server.fastmcp import FastMCP     # 1.x — finns inte längre
```

I `mcp` 2.0 heter klassen `MCPServer`:

```python
from mcp.server.mcpserver import MCPServer  # 2.x
```

Dekoratorn `@mcp.tool()` fungerar likadant. Klientsidan har också bytt från
camelCase till snake_case (`server_info`, `input_schema`).

Testat mot `mcp` 2.0.0 den 2026-08-12.

## Nästa steg

Kopiera katalogen och byt ut funktionerna mot något som är nyttigt i ditt arbete.
Att exponera ett befintligt CLI eller API är oftast mindre arbete än man tror — se
[docs/20-tekniker/mcp.md](../../../docs/20-tekniker/mcp.md).

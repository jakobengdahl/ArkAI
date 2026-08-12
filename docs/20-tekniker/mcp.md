# MCP — Model Context Protocol

Ett öppet protokoll för att koppla verktyg och datakällor till AI-applikationer. En
**MCP-server** exponerar funktioner; en **MCP-klient** (Claude Code, Continue, Open
WebUI, en egen app) kan upptäcka och anropa dem.

## Vad det löser

Utan MCP skriver du integrationen mot varje AI-verktyg för sig. Fem verktyg som
behöver samma funktion betyder fem integrationer, i fem olika format, som går sönder
var för sig.

Med MCP skriver du funktionen en gång och alla klienter som talar protokollet kan
använda den. Det är ett tråkigt problem att lösa, men det är precis det slags
tråkiga problem som avgör om något går att förvalta.

Det är också värt att se vad MCP *inte* är: det gör inte modellen bättre och det
löser inte behörighetsfrågan. Det standardiserar kopplingen.

## Hur det fungerar

En server erbjuder tre sorters saker:

| | Vad | Exempel |
|---|---|---|
| **Tools** | Funktioner modellen kan anropa | `sok_i_registret(fråga)` |
| **Resources** | Data klienten kan läsa | ett dokument, en tabell |
| **Prompts** | Färdiga instruktionsmallar | "granska den här arkitekturbeskrivningen" |

Servern kan köras lokalt (klienten startar en process, kommunikation över stdio)
eller som en tjänst över HTTP. Lokalt är enklast att komma igång med; HTTP behövs när
flera användare ska dela samma server — vilket är precis skillnaden mellan ett
personligt verktyg och något gemensamt.

**Verktygsbeskrivningen är prompten.** Namn, beskrivning och parametrar är allt
modellen har att gå på när den avgör om verktyget ska användas. En dåligt beskriven
funktion anropas inte, eller anropas fel. Det här är den vanligaste orsaken till att
en MCP-server "inte fungerar" — problemet är sällan koden.

## Redan i miljön

Continue är förkonfigurerad med en MCP-server för DuckDB:

```yaml
mcpServers:
  - name: DuckDB
    command: uvx
    args: [mcp-server-motherduck, --allow-switch-databases, --read-write, ...]
```

Det är ett körande exempel att titta på innan du bygger eget. Se
[../60-miljo/ai-verktyg-i-imagen.md](../60-miljo/ai-verktyg-i-imagen.md).

## Bygga en egen

[`exempel/mcp/hello-mcp/`](../../exempel/mcp/hello-mcp/) är en minimal server i
Python med instruktioner för hur du kopplar in den i Continue, Claude Code och Open
WebUI. Räkna med en halvtimme för att få den att svara första gången.

De flesta MCP-servrar distribueras via npm och körs med `npx`, så Node behövs — se
[../60-miljo/verktygslada.md](../60-miljo/verktygslada.md).

## När det passar

- Flera AI-verktyg behöver samma funktion
- Modellen behöver läsa något som ändras — ett register, en katalog, en status
- Du vill att modellen ska *göra* något, inte bara beskriva hur det görs
- Funktionen finns redan som CLI eller API och bara behöver exponeras

## När det inte passar

- **Engångsuppgifter.** Att skriva en MCP-server för något du gör en gång är dyrare
  än att göra det för hand.
- **Stora datamängder.** Verktygsresultat hamnar i kontexten. En funktion som
  returnerar tiotusen rader förstör sessionen. Låt servern sammanfatta eller
  paginera.
- **Där behörighet är hela problemet.** MCP-servern kör med de rättigheter du gett
  den. Ska olika användare se olika saker måste det lösas i servern — protokollet
  hjälper inte.
- **När ett skript räcker.** Om människan ändå ska köra det, kör det.

## Vad det kostar

Att skriva servern: timmar. Att skriva den så att modellen faktiskt använder den
rätt: iterationer. Att förvalta den när klienterna uppdateras: löpande.

Kontextkostnad: varje inkopplad server lägger sina verktygsbeskrivningar i
kontexten vid varje anrop. Tio servrar med tjugo verktyg vardera är inte gratis —
och gör dessutom modellen sämre på att välja rätt.

## Vad vi har provat

| Experiment | Vad vi lärde oss |
|---|---|
| — | *(inget än)* |

## Vad vi ännu inte vet

- Hur många verktyg kan kopplas in innan modellen börjar välja fel?
- Vad krävs för att köra en delad MCP-server över HTTP i den här miljön, med
  behörigheter per användare?
- Går det att exponera våra befintliga API:er via MCP utan att skriva om något?
- Hur granskar man vad en agent faktiskt anropade? (Langfuse finns i katalogen)

## Vidare läsning

- <https://modelcontextprotocol.io>
- [exempel/mcp/hello-mcp/](../../exempel/mcp/hello-mcp/)
- [chattbot-plus-verktyg.md](chattbot-plus-verktyg.md)

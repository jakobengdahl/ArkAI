# Exempel

Körbar kod. Allt här ska gå att köra i labbmiljön utan förberedelser utöver det som
står i respektive README.

| Exempel | Vad det visar |
|---|---|
| [mcp/hello-mcp/](mcp/hello-mcp/) | En minimal MCP-server som exponerar minnesbanken |
| [skills/granska-teknikbeskrivning/](skills/granska-teknikbeskrivning/) | En skill som kodifierar ett arbetssätt |

## Regler

**Ska gå att köra.** Ett exempel som inte startar är sämre än inget exempel — det tar
tid att felsöka och lär ut fel saker. Testa innan du commitar, och skriv i README:n
vilken version du testade mot.

**Ska vara litet.** Exemplen finns för att läsas och kopieras. Ett exempel som gör
fem saker lär ut ingenting.

**Ska kommentera *varför*, inte *vad*.** Koden visar vad som händer. Kommentarerna
ska förklara valen — varför verktyget delades upp i tre funktioner, varför
felmeddelandet är formulerat som det är.

**Inga hemligheter.** Läs från miljövariabler, dokumentera vilka som behövs i
[`.env.example`](../.env.example).

## Vad som saknas

Idéer till exempel som vore nyttiga. Ta något.

- En MCP-server över HTTP i stället för stdio — vad krävs för att flera ska dela den?
- Ett Open WebUI-verktyg (deras eget format) som gör samma sak som hello-mcp, för
  jämförelse
- Ett minimalt skript som anropar
  [plattformens LLM-inferens](../docs/60-miljo/sspcloud-llm.md) och mäter
  tokenförbrukning
- Ett exempel på hur minnesbanken laddas in i en session, med och utan index

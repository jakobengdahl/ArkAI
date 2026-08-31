# Metadatagrafen

I samma namnrymd kör en pilot som representerar metadata som en graf: vilka begrepp,
register och variabler som finns, och hur de hänger ihop. Den har ett webbgränssnitt
för att utforska grafen, ett REST-API och en **MCP-server** — vilket är det som gör
den intressant här.

Vi installerar den inte. Vi kopplar upp oss mot instansen som redan kör.

## Varför den hör hemma i det här repot

Grafen kommer ur ett eget innovationsspår med ett eget behov: att få ordning på den
metadata som används i verksamheten. Kopplingen hit handlar inte om att slå ihop
spåren, utan om att de svarar på samma fråga från olika håll:

> Grafen är ett **domänminne** — vad som finns och hur det hänger ihop.
> [Minnesbanken](../20-tekniker/minnesbank.md) är ett **processminne** — vad vi lärt
> oss om att arbeta. Båda ska nås av samma agenter, genom samma MCP-rör.

Om de ska vara två system eller ett är precis den sortens fråga repot finns för att
besvara — och den går inte att svara på i teorin. Kör
[grafen inkopplad i Eneo](eneo.md#verktyg-mcp-i-eneo) och ställ samma fråga till båda.

Grafen är också en påminnelse om skillnaden mellan ett experiment och en pilot. Den
har riktiga användare och ett inloggningsskydd. Det vi gör i det här repot har
varken eller — och därför får ingenting härifrån behandlas som en komponent i något
som ska förvaltas.

## Koppla upp dig

Uppgifterna kommer ur [Vault-hemligheten](starta-labbet.md), aldrig ur repot:

| Variabel | Vad |
|---|---|
| `METADATAGRAF_URL` | adressen till instansen |
| `METADATAGRAF_TOKEN` | bearer-token till MCP-servern |
| `METADATAGRAF_BASIC` | `användare:lösenord` till webbgränssnittet |

Webbgränssnittet och API:et ligger bakom ett gemensamt inloggningsskydd som alla
pilotanvändare delar. Innehållet är inte känsligt, men instansen har en inbyggd
AI-assistent som använder plattformens LLM-API — och den ska inte stå öppen.

Panelen visar grafen som *kör* utan att ha några uppgifter alls. Hälsokontrollen
(`/health`) svarar utan inloggning, allt annat svarar `401`. Det räcker för att
kunna säga "den är uppe" utan att panelen behöver hantera hemligheter.

## MCP-servern

```
$METADATAGRAF_URL/mcp/sse
```

Den hamnar automatiskt i `~/work/.labb/mcp.json` när panelen ser att grafen svarar,
och därifrån läser klienterna den:

- **Claude Code och andra kodagenter** — peka `.mcp.json` mot filen
- **OpenClaw** — samma fil i gatewayens konfiguration
- **Open WebUI** — via [MCP-bryggan](../20-tekniker/mcp.md), eftersom Open WebUI
  pratar verktygsservrar över OpenAPI och inte MCP

Bearer-token skickas som `Authorization: Bearer $METADATAGRAF_TOKEN`.

## Vad som är värt att prova

1. **Samma fråga, två gränssnitt.** Grafen i en chatt och grafen hos en agent.
   Skillnaden i vem som initierar är större än skillnaden i svar.
2. **Graf kontra vektorsökning.** Metadata är starkt strukturerad. Det är en av de
   få gångerna där man kan mäta vad en graf tillför jämfört med en
   embedding-baserad sökning — se [rag-och-vektor.md](../20-tekniker/rag-och-vektor.md).
3. **Två minnen samtidigt.** Ge en agent både grafen och minnesbanken och se om den
   väljer rätt källa. Går det inte är det ett resultat värt att skriva ner.
4. **Vad kostar det att fråga?** Grafen svarar med noder, inte med text. Jämför
   tokenåtgången med att lägga motsvarande underlag i kontexten.

## Om du behöver köra en egen instans

Det behövs normalt inte, och vi klonar inte projektet hit. Ska du ändra schemat
eller profilerna hör det hemma i det projektets eget repo, inte i labbet.

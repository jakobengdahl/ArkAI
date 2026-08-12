# Skills

Ett paket med instruktioner — och ofta hjälpfiler eller skript — som ett AI-verktyg
laddar in när uppgiften kräver det.

## Vad det löser

Man vill att assistenten ska kunna vårt sätt att göra saker: hur en
arkitekturbeskrivning ska se ut, vad en granskning ska omfatta, vilka steg som ingår
i en viss analys.

Att lägga allt det i systemprompten fungerar för en sak och slutar fungera vid fem.
Kontexten fylls av instruktioner som är irrelevanta för det man gör just nu, och
kvaliteten sjunker — modellen får svårare att prioritera, inte lättare.

Skills löser det genom att laddas **selektivt**. Beskrivningen ligger alltid framme;
innehållet hämtas bara när det behövs. Samma princip som
[index före innehåll](../../minnesbank/arbetssatt/index-fore-innehall.md) i
minnesbanken.

## Hur det fungerar

En skill är i grunden en katalog med en instruktionsfil och en beskrivning av när den
ska användas. Verktyget läser beskrivningen, avgör om den är relevant för uppgiften,
och laddar då in resten.

**Beskrivningen är det som avgör om den används.** En bra skill med vag beskrivning
laddas aldrig. Skriv den som ett svar på "när ska det här användas?", inte som en
rubrik.

Skills kan innehålla mer än text — mallar, exempel, skript som verktyget kan köra.
Det gör dem till ett sätt att paketera ett helt arbetssätt, inte bara instruktioner.

Formaten skiljer sig mellan verktyg. Claude Code har `.claude/skills/`, andra verktyg
har sina motsvarigheter. Grundidén är densamma.

## När det passar

- Arbetsmoment som återkommer och har en form vi bryr oss om
- När resultatet ska följa en mall eller en checklista
- Kunskap som är för lång för en prompt men för specifik för minnesbanken
- När flera personer ska få samma resultat av samma uppgift

Den sista är den intressanta för oss: en skill är ett sätt att dela ett arbetssätt,
inte bara kunskap. Det ligger nära det vi vill uppnå med minnesbanken.

## När det inte passar

- **Engångsuppgifter.** Skriv en prompt.
- **Sådant som ändras ofta.** En skill som är inaktuell är sämre än ingen skill, för
  den följs.
- **Där omdöme krävs.** En skill kodifierar ett arbetssätt. Är arbetssättet "det
  beror på" blir skillen antingen tom eller fel.
- **Som ersättning för dokumentation.** En skill är skriven för en modell. Människor
  behöver fortfarande sin version — även om de ofta kan vara samma text.

## Skillnad mot närliggande saker

| | Vad det är | Laddas |
|---|---|---|
| **Systemprompt** | Stående instruktioner | Alltid |
| **Skill** | Arbetssätt för en uppgiftstyp | När den behövs |
| **Minnespost** | Ett faktum värt att minnas | Via index, vid behov |
| **MCP-verktyg** | En funktion som kan anropas | Verktygslistan alltid, anropet vid behov |

Gränsen mellan skill och minnespost är i praktiken: **skill = hur man gör något**,
**minnespost = något man behöver veta**.

## Vad det kostar

Att skriva en skill är att skriva ner ett arbetssätt tillräckligt tydligt för att
någon annan ska kunna följa det. Det är nyttigt arbete oavsett AI — och det är också
därför det tar tid.

Löpande: de måste hållas aktuella, och det finns ingen som säger till när de blivit
fel.

## Testa i labbet

Ta ett arbetsmoment som görs ofta och har en form. Skriv en skill. Låt någon annan
köra samma uppgift med och utan den.

Mätpunkten är inte om svaret blev bättre — det är om **två personer fick jämförbara
resultat**. Det är den effekt skills faktiskt ger, och den som är värd något för oss.

## Vad vi har provat

| Experiment | Vad vi lärde oss |
|---|---|
| — | *(inget än)* |

## Vad vi ännu inte vet

- Hur många skills kan finnas innan verktyget väljer fel?
- Går samma skill att använda i flera verktyg, eller får vi underhålla parallella
  varianter?
- Var går gränsen mot minnesbanken i praktiken?
- Kan skills versionshanteras och granskas som kod? (De borde kunna det — de *är* text)

## Vidare läsning

- [minnesbank.md](minnesbank.md)
- [kodagenter.md](kodagenter.md)

# Minnesbank

Strukturerad, beständig kunskap som medvetet läggs in i kontexten i kommande
sessioner. Skriven för att läsas av en modell, kurerad av människor.

Det här är den teknik vi har störst egen erfarenhet av att bygga — se
[minnesbank/](../../minnesbank/), som både är vårt arbetsverktyg och vårt experiment.

## Vad det löser

En modell minns ingenting mellan sessioner. Utan minne börjar varje session om från
noll: samma bakgrund, samma förklaringar, samma missförstånd.

De inbyggda minnesfunktionerna i dagens verktyg löser det — **per person**. Det du
lärt din assistent vet inte min assistent. Vi bygger upp samma kunskap parallellt, i
var sitt verktyg, i format vi inte kommer åt eller kan granska.

Det är samma problem personliga anteckningsböcker hade före wikin.

## Hur det fungerar

**En post = en fil = ett faktum.** Varje post har en beskrivningsrad som räcker för
att avgöra relevans, och ett `MINNE.md` som index.

Nyckelmekanismen är att **indexet läggs i kontexten, inte innehållet**. Modellen ser
vad som finns och hämtar de poster den behöver. Ett index på 40 rader kostar nästan
ingenting; hela minnesbanken kostar mycket och gör svaren sämre, inte bättre — se
[minnesbanken om varför](../../minnesbank/arbetssatt/index-fore-innehall.md).

Format och konventioner: [minnesbank/README.md](../../minnesbank/README.md).

## Skillnaden mot RAG

Den här förväxlingen är den vanligaste, och den kostar tid.

| | RAG | Minnesbank |
|---|---|---|
| Innehåll | dokument som redan finns | poster skrivna för ändamålet |
| Urval | automatiskt, per fråga | kurerat av människor |
| Svarar på | "vad står det om X?" | "vad brukar vi göra?" |
| Kvalitet | beror på källmaterialet | beror på disciplinen |
| Fel yttrar sig som | hittar fel stycke | posten är inaktuell |
| Underhåll | indexering | skrivande och rensning |

De utesluter inte varandra. Ett rimligt upplägg är RAG över dokumentationen och en
minnesbank för lärdomarna om hur man tolkar den.

## När det passar

- Kunskap som inte står någonstans — hur vi gör, varför vi valde så, vad som gick fel
- Flera personer som behöver samma bakgrund
- Sådant som ska överleva att en person slutar
- När du märker att du förklarar samma sak för modellen upprepade gånger

Den sista är den bästa signalen. Tredje gången du skriver samma bakgrund i en prompt
är det en minnespost.

## När det inte passar

- **Sådant som redan står i koden eller dokumentationen.** Länka i stället. En
  minnespost som duplicerar en sanning kommer att bli fel när den andra ändras.
- **Stora mängder faktauppgifter.** Det är RAG:s eller en databas område.
- **Sådant som ändras varje vecka.** Underhållet blir större än nyttan.
- **När ingen äger den.** En minnesbank utan någon som rensar blir en soptipp och
  slutar användas — och en minnesbank ingen litar på är sämre än ingen alls.

## Vad det kostar

Främst disciplin. Tekniken är triviala textfiler; det svåra är att faktiskt skriva
posten när man är klar med något, och att ta bort den när den blivit fel.

Räkna med att en tredjedel av arbetet är att rensa. Det kommer att kännas som
bortkastad tid och är det inte.

## Skalgränsen

Filbaserat med markdown-index fungerar bra upp till en viss storlek. Vår gissning är
att gränsen ligger kring 50–100 poster, men vi vet inte — det är en av frågorna vi
vill besvara.

Efter den gränsen behövs semantisk sökning
([rag-och-vektor.md](rag-och-vektor.md)) eller relationer
([grafminne.md](grafminne.md)). Sannolikt båda: sökning för att hitta rätt post,
grafen för att hitta det som hänger ihop med den.

## Vad vi har provat

| Experiment | Vad vi lärde oss |
|---|---|
| Minnesbanken själv | Uppstartad 2026-08-12. Se [minnesbank/](../../minnesbank/) |

## Vad vi ännu inte vet

- Var går skalgränsen för filbaserat på riktigt?
- Vad händer med kvaliteten när AI får skriva poster? Volymen ökar säkert — blir
  minnet bättre eller bara större?
- Vad ska vara delat och vad ska förbli personligt?
- Håller ett format för både människa och modell, eller behövs två representationer?
- Hur märker vi att en post blivit fel, innan någon förlitar sig på den?

Den sista är den som oroar mest. En felaktig minnespost är sämre än ingen post, för
den ser lika trovärdig ut.

## Vidare läsning

- [minnesbank/README.md](../../minnesbank/README.md) — vårt upplägg
- [agentupplagg.md](agentupplagg.md) — Hermes bygger minne automatiskt, som jämförelse
- [grafminne.md](grafminne.md)

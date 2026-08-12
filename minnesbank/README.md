# Den delade minnesbanken

Det här är vårt gemensamma långtidsminne. Det är både ett arbetsverktyg och det
experiment vi lär oss mest av.

## Problemet den löser

Alla AI-verktyg har någon form av minne numera — Claude Code har sitt, ChatGPT har
sitt, Open WebUI har sitt. De är alla **personliga**. Det du lärt din assistent om
hur vi jobbar vet inte min assistent något om. Vi bygger upp samma kunskap parallellt,
i var sitt verktyg, i format vi inte kommer åt.

Det är samma problem som personliga anteckningsböcker hade före wikin. Lösningen är
densamma: lägg minnet på en delad, versionshanterad plats — och skriv det så att både
människor och modeller kan läsa det.

## Hur det fungerar

**En post = en fil = ett faktum.**

Inte ett dokument per ämne. En fil per sak som är värd att komma ihåg. Det låter
smått, men det är hela poängen: en modell (eller en människa) ska kunna hämta *just*
det som är relevant, utan att dra in tre sidor runtomkring.

```
minnesbank/
├── MINNE.md              ← index. Läses först. En rad per post.
├── MALL-minnespost.md
├── arbetssatt/           ← hur vi jobbar, vad som visat sig fungera
├── domankunskap/         ← om vår verksamhet, avidentifierat
├── verktyg/              ← hur våra verktyg och miljöer faktiskt beter sig
└── beslut/               ← vad vi bestämt, och varför
```

`MINNE.md` är index och den enda filen som är tänkt att alltid läsas. Resten hämtas
vid behov. Ett index på 40 rader kostar nästan ingen kontext men gör att modellen
vet vad som *finns* — och kan be om rätt fil.

## Formatet

```markdown
---
namn: kort-kebab-case-slug
beskrivning: En rad som gör att man kan avgöra om posten är relevant.
typ: arbetssatt | domankunskap | verktyg | beslut
uppdaterad: 2026-08-12
---

Själva faktumet. Kort. Ett stycke, inte en uppsats.

**Varför:** vad som ledde fram till det här. Utan varför blir posten en regel
utan grund, och den första som tycker annorlunda kommer att ändra den.

**Så använder du det:** vad man konkret ska göra, nästa gång det är aktuellt.

Relaterat: [[annan-post]], [[tredje-post]]
```

`beskrivning` är det viktigaste fältet. Det är det som avgör om posten hittas.
Skriv den som ett sökresultat, inte som en rubrik.

`[[hakparenteser]]` länkar till en annan posts `namn`. Länka gärna till poster som
inte finns än — det markerar något som är värt att skriva.

## Vad som hör hemma här

Frågan att ställa: **skulle nästa person spara tid på att veta det här innan de
börjar?**

Skriv en post när:

- Något visade sig fungera på ett sätt som inte var uppenbart
- Något gick fel på ett sätt som kommer att gå fel igen
- Vi bestämde något, och skälet är värt att minnas
- Ett verktyg beter sig annorlunda än dokumentationen påstår

Skriv **inte** en post för:

- Sådant som finns i koden eller i dokumentationen — länka i stället
- Sådant som bara var sant en gång
- Sammanfattningar av ett experiment — det hör hemma i `docs/30-experiment/`.
  Minnesposten är den *lärdom* som överlever experimentet.

Det sista är den vanligaste missen. Ett experiment är en berättelse om något som
hände. En minnespost är en instruktion till framtiden.

## Regler som gör att det håller

**Rensa lika ofta som du skriver.** En minnesbank som bara växer blir en soptipp och
slutar användas. Är en post inaktuell — ta bort den. Git kommer ihåg åt oss.

**En post ska kunna läsas utan de andra.** Länkar är bra, beroenden är inte det.

**Repot är publikt.** Minnesbanken är inte undantagen från
[RIKTLINJER-INNEHALL.md](../RIKTLINJER-INNEHALL.md). Verksamhetskunskap skrivs
avidentifierad, som mönster.

**Ändringar går via PR.** Att någon annan läser är hela skillnaden mot ett personligt
minne. Det är också den enda spärren mot att en AI-assistent skriver in något
felaktigt som sedan blir sanning för alla.

## Använda den med ett AI-verktyg

Peka verktyget på katalogen och låt det läsa `MINNE.md` först. I Claude Code räcker en
rad i `AGENTS.md` eller `CLAUDE.md`. I Open WebUI kan du ladda upp katalogen som en
kunskapsbas.

Det viktiga är ordningen: **index först, enskilda poster vid behov.** Att lägga hela
minnesbanken i kontexten fungerar tills den blir stor, och blir sedan aktivt sämre —
modellen får svårare att hitta det relevanta, inte lättare.

## Vad vi vill ta reda på

Minnesbanken är också ett experiment. Öppna frågor:

1. **Var går gränsen för filbaserat?** Vid 30 poster är ett index i markdown
   optimalt. Vid 300? Då behövs sannolikt semantisk sökning eller en graf —
   se [grafminne](../docs/20-tekniker/grafminne.md).
2. **Håller det att skriva för både människa och modell?** Eller behöver vi två
   representationer av samma kunskap?
3. **Vad händer med kvaliteten när AI får skriva poster?** Volymen ökar säkert.
   Blir minnet bättre eller bara större?
4. **Vad ska vara delat och vad ska vara personligt?** Allt är inte gemensamt.
   Var går gränsen?

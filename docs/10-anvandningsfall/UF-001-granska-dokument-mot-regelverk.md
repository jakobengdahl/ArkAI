# UF-001 · Granska ett underlag mot ett regelverk

**Steg:** Skiss
**Ägare:** —
**Uppdaterad:** 2026-08-12

> **Det här är ett konstruerat exempel.** Det finns här för att visa formen på ett
> användningsfall, inte för att beskriva ett verkligt uppdrag. Ersätt det gärna med
> något riktigt — avidentifierat enligt
> [RIKTLINJER-INNEHALL.md](../../RIKTLINJER-INNEHALL.md).

## Vad det handlar om

Ett underlag på 20–40 sidor ska granskas mot ett regelverk innan det går vidare.
Granskningen ska svara på om underlaget uppfyller ett antal krav, och peka ut vad
som saknas.

## Hur det går till idag

1. Den som granskar läser igenom underlaget en gång för att få en helhetsbild
2. Går igenom regelverket punkt för punkt och letar upp motsvarande avsnitt
3. Antecknar avvikelser och otydligheter
4. Skriver ihop ett granskningsutlåtande
5. Stämmer i oklara fall av med en kollega

Tar en halv till en hel arbetsdag. Sker några gånger i månaden. Görs av ett fåtal
personer som kan regelverket väl.

## Vad som gör det svårt

Inte att det är intellektuellt krävande — steg 2 är mekaniskt letande. Svårigheten är
att:

- det är lätt att missa en punkt när man gått igenom regelverket många gånger
- olika granskare lägger ribban olika, särskilt i gränsfall
- kunskapen sitter hos några få personer och är svår att föra vidare
- resonemanget bakom en bedömning skrivs sällan ner, bara slutsatsen

Notera att bara det första är ett volymproblem. De övriga är
konsistens- och kunskapsöverföringsproblem — och de pekar mot andra tekniker.

## Vad som skulle vara bättre

Granskaren börjar från ett utkast där de mekaniska delarna redan är gjorda: varje
krav i regelverket parat med det ställe i underlaget som verkar svara mot det, plus
en markering av vad som inte gick att hitta.

Granskaren gör då bedömningen, inte letandet.

## Hur vi ser att det blev bra

- Granskaren behåller eller höjer sin träffsäkerhet på missade punkter
- Tiden för steg 2 minskar märkbart
- Två granskare som utgår från samma utkast kommer närmare varandra i bedömningen
- Granskaren litar tillräckligt mycket på utkastet för att använda det frivilligt
  efter tredje gången

Den sista är den avgörande. Ett verktyg folk slutar öppna har inte lyckats, oavsett
vad mätningarna visar.

## Underlaget

| | |
|---|---|
| Format | text, ibland med tabeller och bilagor |
| Ungefärlig mängd | 20–40 sidor per granskning |
| Hur ofta det ändras | varje underlag är nytt; regelverket ändras sällan |
| Känslighet | avgör var det får behandlas — måste klaras ut innan pilot |

## Vem bedömer svaret

Granskaren, som kan regelverket. Bedömningen är snabb **om** utkastet hänvisar till
var i underlaget varje påstående kommer ifrån. Utan hänvisningar måste allt
kontrolleras om, och då är verktyget värdelöst — sannolikt sämre än inget.

Det gör källhänvisning till ett krav, inte en förbättring.

## Vad som skulle behövas

- Regelverket i maskinläsbar form, uppdelat per krav
- Ett antal tidigare granskningar att utvärdera mot (med kända svar)
- Besked om var underlaget får behandlas
- En granskare som kan avsätta tid för utvärdering

## Möjliga tekniker

| Teknik | Varför den skulle kunna passa | Provat? |
|---|---|---|
| [RAG](../20-tekniker/rag-och-vektor.md) | Hitta rätt ställe i underlaget per krav. Ger källhänvisning. | — |
| [Chattbot + verktyg](../20-tekniker/chattbot-plus-verktyg.md) | Granskaren driver, verktyget slår upp | — |
| [Skills](../20-tekniker/skills.md) | Kodifiera granskningens form → jämnare bedömningar | — |
| [Minnesbank](../20-tekniker/minnesbank.md) | Fånga resonemang från gränsfall som annars inte skrivs ner | — |

Värt att notera: RAG löser bara det första problemet. Konsistensen mellan granskare
är ett skills-problem, och kunskapsöverföringen ett minnesbanksproblem. Ett verktyg
som bara gör det första kommer att uppfattas som en besvikelse trots att det gör
precis vad det ska.

## Öppna frågor

- Klarar embeddingmodellerna vår terminologi på svenska?
- Hur presenteras "det här kravet hittade jag inget om" utan att granskaren slutar
  läsa själv?
- Hur undviker vi att granskaren börjar lita på utkastet mer än det förtjänar?

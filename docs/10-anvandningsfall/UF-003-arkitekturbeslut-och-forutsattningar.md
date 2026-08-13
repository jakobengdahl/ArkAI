# UF-003 · Arkitekturbeslut och arkitekturförutsättningar

**Typfall:** [D · Generativt stöd i interna processer](typfall.md)
**Spår:** Eget
**Steg:** Skiss
**Ägare:** —
**Uppdaterad:** 2026-08-13

> **Exempel, inte beslut.** Fallet finns här för att visa formen på ett riktigt
> användningsfall och för att ge något konkret att diskutera kring. Att det står
> beskrivet betyder inte att det är valt.

## Vad det handlar om

Att ta fram arkitekturförutsättningar och att fatta och dokumentera arkitekturbeslut
är en av de processer vi lägger mest tid på. En stor del av den tiden går inte åt
till att tänka, utan till att hålla ordning: vad har vi redan beslutat, vad är
beslutat men aldrig nedskrivet, och vad gör andra som vi borde väga in?

Underlaget finns i tre lager som beter sig olika. Explicita beslut i skrivna ADR:er
och principer. Implicita beslut som lever som praxis och som bara några personer kan
återge. Och en omvärld — andra myndigheter, andra statistikverksamheter,
internationella ramverk — där utvecklingen sker oberoende av oss.

## Hur det går till idag

1. Ett behov kommer upp: ett initiativ behöver veta vad som gäller
2. Leta rätt på vad som redan är beslutat i ADR:er, principer, målbilder och
   tidigare underlag
3. Reda ut vad som faktiskt är beslutat och vad som är praxis ingen skrivit ner
4. Skaffa en bild av hur andra löst samma sak
5. Formulera alternativ med konsekvenser, och skriva ihop ett diskussionsunderlag
6. Diskutera, landa, skriva ADR:n
7. Uppdatera de modeller och beskrivningar som beslutet påverkar

Steg 2–3 tar oproportionerligt lång tid i förhållande till vad de tillför, och steg 7
är det som oftast blir kvar att göra "sen".

## Vad som gör det svårt

- **Letande.** Besluten finns, men utspridda över dokument skrivna vid olika
  tillfällen av olika personer.
- **Implicita beslut.** Det viktigaste är ofta det som aldrig formulerades, för det
  var självklart för dem som var med.
- **Samband.** "Vad påverkas om vi ändrar det här?" är den fråga som är svårast att
  besvara och lättast att svara fel på.
- **Konsistens över tid.** Motsäger det vi säger nu något vi sagt tidigare? Ofta
  upptäcks det av någon annan, långt senare.
- **Omvärlden.** Att hålla koll kostar tid även när inget händer.

Fem svårigheter, och bara den första är ett letandeproblem. Det är värt att hålla i
huvudet: ett stöd som bara gör steg 2 snabbare kommer att uppfattas som en besvikelse
trots att det gör precis vad det ska.

## Nivåerna på det här fallet

Fallet är ett bra exempel på att samma användning kan dras olika långt. Se
[nivåstegen](../20-tekniker/byggstenar.md#nivåstegen-språket-som-håller-i-ett-möte).

| Nivå | Vad det skulle innebära här | Vad det förutsätter |
|---|---|---|
| **1** | Hjälp att formulera och strama upp en text vi redan tänkt färdigt | Ingenting utöver åtkomst |
| **2** | Svar grundade i våra egna beslut och principer: "vad har vi sagt om det här?" med hänvisning | Att besluten finns i en form som går att söka i |
| **3** | Ett utkast till diskussionsunderlag: relevanta tidigare beslut, alternativ, konsekvenser, motstridigheter som upptäckts | Granskning, spårbarhet, en tydlig markering av vad som är hämtat och vad som är genererat |
| **4** | Uppdaterar modeller och beskrivningar när ett beslut fattats, och flaggar vad som blivit inaktuellt | Behörigheter, avgränsat mandat, loggning |

Nivå 2 är den som gör mest nytta per insats, och arbetet med den — att få våra egna
beslut i sökbar form — är samma arbete som nivå 3 och 4 sedan vilar på.

## Vad som skulle vara bättre

Den som förbereder ett beslut börjar från ett underlag där det mekaniska redan är
gjort: vad vi tidigare sagt i frågan, med hänvisning till var; vilka beslut som
gränsar till den; och vad som verkar motsäga vad.

Vi lägger då tiden på avvägningen, inte på arkeologin.

## Hur vi ser att det blev bra

- Tiden från "vi behöver reda ut det här" till "vi har ett underlag att diskutera"
  minskar märkbart
- Underlaget innehåller minst en relevant tidigare koppling som vi annars hade missat
- Ingen behöver kontrollera om hänvisningarna stämmer efter tredje gången
- Vi använder det frivilligt även när det är bråttom

Den sista är den avgörande. Ett stöd som bara används när man har gott om tid har
inte lyckats.

## Underlaget

| | |
|---|---|
| Format | text: beslut, principer, målbilder, underlag. Modeller i strukturerad form |
| Ungefärlig mängd | växande samling; enskilda dokument från några sidor till några tiotal |
| Hur ofta det ändras | nya beslut löpande, gamla revideras sällan men det händer |
| Känslighet | internt material — avgör var det får behandlas och måste klaras ut innan något körs på riktigt underlag |

I labbet arbetar vi med konstruerade beslut med samma form. Det räcker längre än man
tror för att svara på om ansatsen håller.

## Vem bedömer svaret

Vi själva, och vi kan det här materialet väl. Det gör fallet till en ovanligt bra
kandidat: bedömningen är snabb, och felaktiga svar är irriterande snarare än
allvarliga.

Villkoret är hänvisningar. Ett påstående om vad vi tidigare beslutat måste gå att
slå upp direkt, annars måste allt kontrolleras om — och då är stödet värdelöst.

## Vad som skulle behövas

- Konstruerade beslut och principer i tillräcklig mängd att söka i
- Ett antal frågor med kända svar, att mäta mot
- Beslut om var det riktiga materialet får behandlas, innan steget dit
- En form för ADR:er som är konsekvent nog att kunna kodifieras

## Möjliga tekniker

| Teknik | Varför den skulle kunna passa | Provat? |
|---|---|---|
| [RAG](../20-tekniker/rag-och-vektor.md) | "Vad har vi sagt om det här?" med hänvisning till var | — |
| [Grafminne](../20-tekniker/grafminne.md) | Samband mellan beslut — vad påverkas om vi ändrar något | — |
| [Minnesbank](../20-tekniker/minnesbank.md) | Fånga de implicita besluten allt eftersom de kommer upp i diskussion | — |
| [Skills](../20-tekniker/skills.md) | Kodifiera formen på ett underlag och på en ADR | — |

Fördelningen speglar svårigheterna: RAG löser letandet, grafen sambanden,
minnesbanken det som aldrig skrevs ner. De tre är inte alternativ till varandra.

## Öppna frågor

- Går implicita beslut att fånga löpande, eller kräver det ett eget arbetspass som
  ingen kommer att prioritera?
- Hur skiljer man i ett underlag på "det här har vi beslutat" och "det här verkar
  följa av det vi beslutat"? Blandas de ihop är stödet farligare än inget.
- Hur mycket omvärld är rimligt att lägga in, och vem håller den aktuell?
- Är det här ett fall för graf, eller räcker text? Se
  [beslutsguiden](../40-matchning/beslutsguide.md) — bygg textminnet först och låt
  gränsen visa vad som behövs.

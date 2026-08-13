# UF-004 · Omvärldsbevakning och mappning av metadatastandarder

**Typfall:** [D · Generativt stöd i interna processer](typfall.md)
**Spår:** Eget
**Steg:** Skiss
**Ägare:** —
**Uppdaterad:** 2026-08-13

> **Exempel, inte beslut.** Fallet finns här för att visa formen och för att ge något
> konkret att diskutera kring. Att det står beskrivet betyder inte att det är valt.

## Vad det handlar om

En del av vårt uppdrag är att ha koll på de standarder och ramverk som styr hur
statistikverksamhet beskriver sina processer, sin information och sina data — GSBPM,
GSIM, SDMX, DDI, länkade data — och att kunna översätta utvecklingen där till vad den
betyder för arbetet innanför väggarna.

Det är inte bevakning för bevakningens skull. Frågan som ska besvaras är återkommande
och konkret: *hur förhåller sig det vi gör till det som andra gör, och vad följer av
det för oss?*

## Hur det går till idag

1. Följa vad som händer i ramverkens egna kanaler och i samarbeten mellan
   statistikmyndigheter
2. Läsa in nytt eller uppdaterat material — ofta omfattande och skrivet för
   specialister
3. Avgöra vad som faktiskt är nytt jämfört med tidigare version
4. Mappa mot de begrepp och modeller vi använder internt
5. Formulera vad det innebär för oss, och föra det vidare dit det hör hemma

Steg 3 och 4 är där tiden går, och de görs sällan systematiskt — de görs när någon
råkar behöva svaret.

## Vad som gör det svårt

- **Volym.** Materialet är stort, och det mesta i en uppdatering är oförändrat.
- **Överlappande modeller.** Ramverken beskriver delvis samma verklighet med olika
  begrepp. Mappningen mellan dem är kunskapsarbete, inte uppslagning.
- **Aktualitet.** En bild av läget som är två år gammal är sämre än ingen bild, för
  den används ändå.
- **Kunskapsöverföring.** Mappningarna sitter i huvudet på dem som gjort dem.
- **Översättningen inåt.** "Vad betyder det här för oss" är den svåra delen, och den
  är den som aldrig hinns med.

## Varför det är en bra kandidat att börja med

**Materialet är öppet.** Ramverken är publicerade och innehåller ingenting känsligt.
Det gör att fallet går att prova var som helst, utan att först reda ut var underlaget
får behandlas — vilket annars är det som stoppar experiment tidigast. Se
[beslutsguiden fråga 4](../40-matchning/beslutsguide.md).

**Vi kan bedöma svaren.** Vi är den grupp som kan de här modellerna. Ett fel är
uppenbart för oss och ofarligt för alla andra.

**Det är ett rent letande- och sambandsproblem.** Därmed prövar det två byggstenar
tydligt åtskilda från varandra — hämtning respektive samband — vilket gör resultatet
läsbart. Se [kartan](../40-matchning/typfall-och-byggstenar.md).

Sammantaget är det förmodligen det billigaste sättet vi har att ta reda på om
hämtning mot eget material håller på den sortens facktext vi arbetar med.

## Vad som skulle vara bättre

Två saker, i den ordningen:

Att kunna fråga "vad säger de olika ramverken om det här begreppet, och var skiljer
de sig?" och få ett svar med hänvisning till var det står.

Att en uppdatering av ett ramverk resulterar i en sammanställning av vad som ändrats
och vilka av våra egna begrepp som berörs — i stället för att någon läser om allt.

## Hur vi ser att det blev bra

- Svaren pekar på rätt ställe i rätt dokument, tillräckligt ofta för att vi ska
  sluta dubbelkolla
- Modellen klarar terminologin utan att blanda ihop begrepp som ligger nära varandra
- En mappning som tidigare tog en dag går att göra på en förmiddag, med samma kvalitet
- Vi kan säga något grundat om var hämtning fungerar och var den inte gör det

Det sista är ett resultat även om de tre första uteblir.

## Underlaget

| | |
|---|---|
| Format | text: specifikationer, modellbeskrivningar, rapporter. Delvis strukturerat |
| Ungefärlig mängd | flera ramverk, vart och ett från tiotals till hundratals sidor |
| Hur ofta det ändras | versionsvis — sällan, men omfattande när det sker |
| Känslighet | öppet publicerat material, inga begränsningar |

## Vem bedömer svaret

Vi själva, snabbt, förutsatt hänvisningar. Det är den enklaste bedömningssituationen
vi har i något av våra fall.

## Vad som skulle behövas

- De publicerade ramverken i en form som går att indexera
- Tio till tjugo frågor med kända svar — inklusive några där svaret är att ramverken
  faktiskt skiljer sig åt
- En beskrivning av våra egna begrepp att mappa mot

Den mittersta punkten är det egentliga arbetet, och den håller även om tekniken byts.

## Möjliga tekniker

| Teknik | Varför den skulle kunna passa | Provat? |
|---|---|---|
| [RAG](../20-tekniker/rag-och-vektor.md) | Letandet i stora, stabila dokumentsamlingar med källhänvisning | — |
| [Grafminne](../20-tekniker/grafminne.md) | Mappningen mellan modeller *är* relationer — se även [metadatagrafen](../60-miljo/metadatagrafen.md) | — |
| [Chattbot + verktyg](../20-tekniker/chattbot-plus-verktyg.md) | Vi driver dialogen; uppgiften är utforskande till sin natur | — |
| [Minnesbank](../20-tekniker/minnesbank.md) | Bevara mappningarna och skälen bakom dem | — |

## Öppna frågor

- Hur bra fungerar embeddingmodellerna på den här sortens facktext, och skiljer det
  sig mellan svenska och engelska? Det är en fråga hela repot behöver svar på.
- Går "vad är nytt i den här versionen" att lösa med hämtning, eller är det en
  jämförelseuppgift som kräver något annat?
- Var går gränsen mellan att mappa begrepp och att tolka dem? Det andra vill vi göra
  själva.

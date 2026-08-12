# Matchningsmatrisen

Kopplingen mellan användningsfall och tekniker. Det här är repots mest värdefulla
dokument när det väl har innehåll — och det mest missvisande om det fylls med
gissningar.

## Regeln

**Bara rader som bygger på ett genomfört experiment.**

Att tro att RAG passar ett användningsfall är inte kunskap, det är en hypotes. Håll
hypoteserna i användningsfallets egen fil under "Möjliga tekniker". Flytta dem hit
när någon faktiskt provat.

Utan den regeln blir matrisen en sammanställning av våra förutfattade meningar, med
ett trovärdigt utseende. Det är sämre än en tom tabell.

## Bekräftat

| Användningsfall | Teknik | Utfall | Experiment |
|---|---|---|---|
| — | — | *(inget än)* | — |

Utfall skrivs som **Fungerar** / **Delvis** / **Fungerar inte**, med en rad om varför.
"Fungerar inte" är lika värdefullt som "fungerar" och ska stå kvar.

## Hypoteser som väntar på prövning

Härifrån plockar man sitt nästa experiment.

| Användningsfall | Teknik | Hypotes | Vem |
|---|---|---|---|
| [UF-001](../10-anvandningsfall/UF-001-granska-dokument-mot-regelverk.md) | [RAG](../20-tekniker/rag-och-vektor.md) | Hittar rätt ställe per krav och kan ge källhänvisning | — |
| [UF-001](../10-anvandningsfall/UF-001-granska-dokument-mot-regelverk.md) | [Skills](../20-tekniker/skills.md) | Jämnare bedömningar mellan granskare | — |
| [UF-001](../10-anvandningsfall/UF-001-granska-dokument-mot-regelverk.md) | [Minnesbank](../20-tekniker/minnesbank.md) | Fångar resonemang från gränsfall som annars inte skrivs ner | — |

## Mönster vi börjar se

Fylls på när vi har underlag. Det här är den egentliga behållningen — enskilda rader
i tabellen ovan är bara belägg.

Två observationer redan från arbetet med att beskriva UF-001, som är värda att pröva
mot fler fall:

**Ett användningsfall har oftast flera svårigheter, och de kräver olika tekniker.**
UF-001 har ett volymproblem, ett konsistensproblem och ett
kunskapsöverföringsproblem. RAG löser bara det första. En lösning som bara adresserar
den mest uppenbara svårigheten kommer att uppfattas som en besvikelse trots att den
gör exakt vad den ska.

**Frågan "kan användaren bedöma svaret?" verkar avgöra mer än teknikvalet.** Kan de
inte det är det inte en teknikfråga längre — då måste lösningen först göras
granskningsbar, oavsett vilken teknik som används. Det är en hypotes, men den har
hållit i varje diskussion så här långt.

## Hur man läser matrisen

Den svarar på "har någon provat det här?" — inte på "vad ska vi välja?". För det
senare, se [beslutsguide.md](beslutsguide.md).

En tom rad betyder att ingen provat, inte att det inte fungerar.

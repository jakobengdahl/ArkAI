# Matchningsmatrisen

Kopplingen mellan användningsfall och tekniker. Det här är repots mest värdefulla
dokument när det väl har innehåll — och det mest missvisande om det fylls med
gissningar.

## Regeln

**Bara rader som bygger på ett genomfört experiment.**

Att tro att RAG passar ett användningsfall är inte kunskap, det är en hypotes. Håll
hypoteserna i användningsfallets egen fil under "Möjliga tekniker", eller i
[typfall-och-byggstenar.md](typfall-och-byggstenar.md) när de gäller en hel klass av
användning. Flytta dem hit när någon faktiskt provat.

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
| [UF-002](../10-anvandningsfall/UF-002-stod-vid-byte-av-arbetsplattform.md) | [Kodagenter](../20-tekniker/kodagenter.md) | Klarar flerstegsarbete i en kodbas med granskningsbart resultat | — |
| [UF-002](../10-anvandningsfall/UF-002-stod-vid-byte-av-arbetsplattform.md) | [RAG](../20-tekniker/rag-och-vektor.md) + [skills](../20-tekniker/skills.md) | Eget kunskapsunderlag betyder mer för kvaliteten än modellvalet | — |
| [UF-003](../10-anvandningsfall/UF-003-arkitekturbeslut-och-forutsattningar.md) | [RAG](../20-tekniker/rag-och-vektor.md) | "Vad har vi sagt om det här?" med hänvisning till var | — |
| [UF-003](../10-anvandningsfall/UF-003-arkitekturbeslut-och-forutsattningar.md) | [Grafminne](../20-tekniker/grafminne.md) | Svarar på vad som påverkas när ett beslut ändras | — |
| [UF-003](../10-anvandningsfall/UF-003-arkitekturbeslut-och-forutsattningar.md) | [Minnesbank](../20-tekniker/minnesbank.md) | Fångar de implicita besluten allt eftersom de kommer upp | — |
| [UF-004](../10-anvandningsfall/UF-004-omvarldsbevakning-metadatastandarder.md) | [RAG](../20-tekniker/rag-och-vektor.md) | Håller på facktext och terminologi, med källhänvisning | — |
| [UF-004](../10-anvandningsfall/UF-004-omvarldsbevakning-metadatastandarder.md) | [Grafminne](../20-tekniker/grafminne.md) | Mappning mellan ramverk är relationer, inte likhet | — |
| [UF-005](../10-anvandningsfall/UF-005-metadata-som-graf.md) | [Grafminne](../20-tekniker/grafminne.md) vs [RAG](../20-tekniker/rag-och-vektor.md) | Graf tillför mätbart mer än text på starkt strukturerad metadata | — |

## Mönster vi börjar se

Fylls på när vi har underlag. Det här är den egentliga behållningen — enskilda rader
i tabellen ovan är bara belägg.

Tre observationer redan från arbetet med att beskriva användningsfallen, värda att
pröva mot fler fall:

**Ett användningsfall har oftast flera svårigheter, och de kräver olika tekniker.**
[UF-003](../10-anvandningsfall/UF-003-arkitekturbeslut-och-forutsattningar.md) har ett
letandeproblem, ett sambandsproblem och ett problem med beslut som aldrig skrevs ner.
RAG löser bara det första. En lösning som bara adresserar den mest uppenbara
svårigheten kommer att uppfattas som en besvikelse trots att den gör exakt vad den ska.

**Var materialet får behandlas avgör vad som går att prova först.**
[UF-004](../10-anvandningsfall/UF-004-omvarldsbevakning-metadatastandarder.md) bygger på
öppet publicerat material och kan köras var som helst, medan de andra fallen kräver att
frågan reds ut först. Det är inget skäl att välja bort de andra — men ordningen man tar
dem i blir sällan den man först tänkte sig.

**Frågan "kan användaren bedöma svaret?" verkar avgöra mer än teknikvalet.** Kan de
inte det är det inte en teknikfråga längre — då måste lösningen först göras
granskningsbar, oavsett vilken teknik som används. Det är en hypotes, men den har
hållit i varje diskussion så här långt.

## Hur man läser matrisen

Den svarar på "har någon provat det här?" — inte på "vad ska vi välja?". För det
senare, se [beslutsguide.md](beslutsguide.md).

En tom rad betyder att ingen provat, inte att det inte fungerar.

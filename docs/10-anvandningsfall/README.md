# Användningsfall

Vad vi faktiskt gör, och var det finns arbete som AI skulle kunna ta.

Det här är den del av repot som är svårast att skriva och lättast att hoppa över.
Frestelsen är att gå direkt på teknikerna — de är roligare. Men utan
användningsfallen har vi inget att matcha mot, och då blir slutsatsen alltid
"tekniken är imponerande" i stället för "det här löser vårt problem".

## Repot är publikt

Skriv avidentifierat. Beskriv **formen** på arbetet, inte vilket system eller vilken
process det gäller:

> Ett underlag på 20–40 sidor granskas mot ett regelverk. Granskningen görs av en
> person, tar en halvdag, och samma frågor återkommer varje gång.

Det är fullt tillräckligt för att kunna resonera om vilken teknik som passar — och
det säger ingenting om vår verksamhet. Se
[RIKTLINJER-INNEHALL.md](../../RIKTLINJER-INNEHALL.md).

Behöver du de riktiga detaljerna för att tänka: skriv dem i `lokalt/` (gitignorerad)
och lyft ut den generella beskrivningen.

## Namngivning

`UF-NNN-kort-namn.md`, löpnummer. Numren är bara till för att kunna hänvisa i en
diskussion — återanvänd inte ett nummer.

## Vad som gör ett användningsfall användbart

Fyll i mallen, men lägg tiden på de här tre:

**Hur arbetet går till idag.** Konkret. "Det är manuellt" räcker inte — vad görs, i
vilken ordning, av vem, hur länge?

**Vad som gör det svårt.** Volym? Att det är tråkigt? Att det kräver kunskap få har?
Att det är lätt att missa något? Svaret avgör vilken teknik som är relevant, och det
är oftast inte det man först tror.

**Hur man ser att det blev bra.** Om vi inte kan säga det innan vi börjar kan vi inte
säga det efteråt heller. Det är den enskilt vanligaste orsaken till att en pilot
varken går vidare eller läggs ner — ingen kan avgöra om den lyckades.

## Att välja vad som ska provas först

Bra kandidater:

- Återkommande arbete med igenkännbar form
- Där underlaget är text
- Där ett fel är irriterande men inte allvarligt
- Där den som gör jobbet idag kan bedöma om AI:ns svar är rätt

Den sista är viktigast och underskattas nästan alltid. Kan användaren inte avgöra om
svaret stämmer har vi flyttat arbete, inte minskat det — och vi har dessutom skapat
en risk.

Dåliga kandidater att börja med:

- Där ett fel får konsekvenser
- Där underlaget innehåller sådant som inte får lämna huset
- Där ingen äger frågan om vad som ska hända sedan
- Där själva svårigheten är att komma överens, inte att producera något

## Statusen

Sätt [mognadssteget](../00-oversikt/mognadstrappa.md) överst i varje fil. En rad,
men den gör diskussionen konkret.

## Filer

| Fil | Steg | Kort |
|---|---|---|
| [UF-001-granska-dokument-mot-regelverk.md](UF-001-granska-dokument-mot-regelverk.md) | Skiss | Exempel — visar formen |

Ersätt gärna exemplet med riktiga användningsfall när de börjar komma in.

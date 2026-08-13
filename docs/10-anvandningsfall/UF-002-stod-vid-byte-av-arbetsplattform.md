# UF-002 · Stöd vid byte av arbetsplattform

**Typfall:** D · Generativt stöd i interna processer — men i verksamhet nära produktionen
**Spår:** Utforskande
**Steg:** Skiss
**Ägare:** — (frågan ägs inte av oss; se nedan)
**Uppdaterad:** 2026-08-13

> **Utforskande spår.** Vi äger inte det här arbetet. Syftet med att ha med fallet är
> att bygga upp egen kunskap om vad som krävs på de högre nivåerna av AI-stöd, så att
> vi kan bidra med underlag när frågan blir aktuell hos dem som äger den. Resultatet
> är ett underlag, inte en lösning. Se
> [de två spåren](../00-oversikt/vision-och-mal.md#två-spår).

## Vad det handlar om

En verksamhet flyttar sina produktionslösningar till en ny gemensam plattform. Bytet
är inte bara tekniskt: arbetet ska bli mer strukturerat och spårbart, med tydligare
kontext, tydligare ansvar och tydligare hantering av kod, data och körningar. Många
behöver ta till sig flera nya begrepp och arbetssätt samtidigt.

Det skapar ett förändringstryck som är svårt att möta med utbildning och mallar
ensamt, eftersom behovet uppstår i stunden och ser olika ut för var och en.

## Hur det går till idag

1. Den som ska flytta en lösning läser in sig på plattformens begrepp och krav
2. Går igenom sin befintliga lösning och försöker avgöra vad som motsvarar vad
3. Skriver om kod och struktur, ofta med äldre skript som utgångspunkt
4. Reder ut fel som beror på nya arbetssätt snarare än på själva koden
5. Uppdaterar dokumentation och metadata så att de speglar den nya lösningen
6. Frågar den lilla grupp som redan kan plattformen när det tar stopp

Steg 4 och 6 är de som skalar sämst. Ju fler som migrerar samtidigt, desto längre
kö till samma få personer.

## Vad som gör det svårt

- **Volym och samtidighet.** Många lösningar ska flyttas inom samma period.
- **Kunskapsöverföring.** Det som krävs sitter hos ett fåtal som redan är hårt
  belastade av att svara på frågor.
- **Konsistens.** Utan stöd blir varje migrerad lösning strukturerad lite olika,
  vilket ger en förvaltningskostnad som betalas i tio år.
- **Gränsytan mellan kod, dokumentation och metadata.** Det är där det blir fel, och
  det är det moment som lättast glöms när tiden är knapp.

Bara den första är ett volymproblem. Det är värt att notera, för det är den enda
svårighet som en snabbare assistent löser.

## Vad som skulle vara bättre

Den som migrerar utgår från ett förslag i stället för från ett tomt blad: en analys
av den befintliga lösningen, en plan för hur den kan struktureras om, ett utkast, och
en beskrivning av vad som ändrats och hur det kan verifieras.

Vinsten är inte främst tid. Den är att lösningarna blir mer lika varandra, och att
den som migrerar behåller förståelsen för sin egen lösning i stället för att kopiera
ett mönster den inte förstår.

## Hur vi ser att det blev bra

I det utforskande spåret mäter vi inte verksamhetsnytta — vi har ingen verksamhet
att mäta på. Vi mäter vad vi lärde oss:

- Vi kan beskriva vad [nivå 3](../20-tekniker/byggstenar.md#nivåstegen-språket-som-håller-i-ett-möte)
  konkret kräver, med belägg från något vi kört
- Vi kan visa var gränsen går mot nivå 4, och vilken styrning steget faktiskt
  förutsätter
- Vi kan svara på hur mycket av kvaliteten som kom från kunskapsunderlaget och hur
  mycket från modellen
- Vi har ett underlag som går att lägga fram för den som äger frågan, formulerat som
  observationer och inte som ett förslag på vad de borde göra

## Underlaget

| | |
|---|---|
| Format | kod, konfiguration, dokumentation, metadata |
| Ungefärlig mängd | en produktionslösning i taget; från några filer till många |
| Hur ofta det ändras | löpande under migreringen, därefter per omgång |
| Känslighet | i labbet: konstruerade lösningar, inga riktiga data. Skarpt läge kräver en egen bedömning |

Att stödet i huvudsak rör kod, dokumentation och metadata — inte innehållet i data —
är det som gör fallet möjligt att utforska alls.

## Vem bedömer svaret

Den som migrerar. Bedömningen är rimlig **om** förslaget redovisar vad som ändrats
och hur det kan verifieras. Ett utkast som bara presenterar ett resultat flyttar
arbetet från att skriva om till att granska om — och det är inte säkert att det är en
vinst.

Det gör "beskriv vad du ändrat och hur jag kontrollerar det" till en del av
lösningen, inte en trevlig extrafunktion.

## Vad som skulle behövas

- En konstruerad exempellösning med samma form som en verklig, att köra experimenten mot
- Ett kunskapsunderlag: riktlinjer, mallar och mönster i en form ett AI-stöd kan använda
- En [kodagent](../20-tekniker/kodagenter.md) med tillräcklig åtkomst i labbmiljön
- Kontakt med den som äger frågan **innan** något visas upp, inte efter

Den sista punkten är inte artighet. Ett underlag som kommer oanmält uppfattas som ett
förslag, och ett förslag om någon annans verksamhet är svårt att ta emot hur bra det
än är.

## Möjliga tekniker

| Teknik | Varför den skulle kunna passa | Provat? |
|---|---|---|
| [Kodagenter](../20-tekniker/kodagenter.md) | Flerstegsarbete i en kodbas är precis vad de är byggda för | — |
| [Skills](../20-tekniker/skills.md) | Kodifiera plattformens mönster → jämnare struktur mellan lösningar | — |
| [RAG](../20-tekniker/rag-och-vektor.md) | Grunda svaren i det egna kunskapsunderlaget i stället för i modellens allmänbildning | — |
| [MCP](../20-tekniker/mcp.md) | Nå metadata och gemensamma tjänster — förutsättningen för nivå 4 | — |
| [Grafminne](../20-tekniker/grafminne.md) | "Vad påverkas om den här delen ändras?" | — |

## Öppna frågor

- Hur mycket av resultatet kommer från kunskapsunderlaget och hur mycket från
  modellen? Det avgör var insatsen ska läggas, och svaret går att mäta.
- Går det att hålla isär "föreslå" och "utföra" på ett sätt som håller när någon har
  bråttom?
- Vad krävs för att ett förslag ska gå att granska på mindre tid än det tar att göra
  jobbet själv?
- Vilken sorts underlag skulle faktiskt vara användbart för den som äger frågan — och
  vet vi det, eller gissar vi?

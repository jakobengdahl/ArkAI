# Byggstenar och nivåer

En AI-lösning är inte en produkt, den är ett antal byggstenar satta i ett upplägg.
Modellen är en av dem, och sällan den som avgör om det blir användbart.

Den här sidan finns av två skäl. Dels för att kunna resonera om *vad* ett förslag
faktiskt består av innan man diskuterar produkter. Dels för att kunna prata om det
med verksamheten utan att införa nio nya begrepp — se
[nivåstegen](#nivåstegen-språket-som-håller-i-ett-möte) längst ned, som är den del
som fungerar i ett möte.

## Byggstenarna

Ingen lösning använder alla. Poängen med listan är att kunna se vilka ett förslag
saknar, för det är där de obehagliga överraskningarna sitter.

| Byggsten | Vad den gör | Där i repot |
|---|---|---|
| **Modellen** | Resonemang och generering. Egen, öppen eller inköpt — valet styr språkstöd, kostnad, insyn och var data hamnar | [../60-miljo/sspcloud-llm.md](../60-miljo/sspcloud-llm.md) |
| **Applikationslagret** | Det användaren möter: chatt, editor, arbetsflöde. Inloggning, loggning, gränssnitt | [chattbot-plus-verktyg.md](chattbot-plus-verktyg.md) |
| **API-lagret** | Den kontrollerade vägen in till modellen. Gör det möjligt att byta modell eller driftform utan att bygga om resten | [../60-miljo/sspcloud-llm.md](../60-miljo/sspcloud-llm.md) |
| **Orkestrering** | Håller ihop flera steg: vilken prompt, vilket verktyg, i vilken ordning, vad som förs vidare | [agentupplagg.md](agentupplagg.md) |
| **Kontext och minne** | Får rätt information in i kontexten vid rätt tillfälle — hämtning, kurerat minne, samband | [rag-och-vektor.md](rag-och-vektor.md), [minnesbank.md](minnesbank.md), [grafminne.md](grafminne.md) |
| **Verktygslagret** | Låter modellen *göra* saker: slå upp, beräkna, skriva, anropa ett system | [mcp.md](mcp.md) |
| **Arbetssätt som paket** | Kodifierade arbetssätt som laddas när de behövs i stället för att ligga i vägen | [skills.md](skills.md) |
| **Säkerhet och behörighet** | Åtkomst, loggning, filtrering. Avgör vad lösningen får se och vad den kan ställa till med | [../50-fran-poc-till-produktion/styrning-och-risk.md](../50-fran-poc-till-produktion/styrning-och-risk.md) |
| **Driftmiljön** | Var det körs. Styr latens, kostnad, kontroll över data och modellversioner | [../60-miljo/](../60-miljo/) |
| **Utvärdering** | Sättet att veta om en ändring hjälpte. Kända fall, mätning, regressionstest | [../40-matchning/beslutsguide.md](../40-matchning/beslutsguide.md) fråga 5 |
| **Mänsklig översyn** | Vem granskar vad, när, och hur mycket. En konstruktionsfråga, inte en instruktion | [../50-fran-poc-till-produktion/styrning-och-risk.md](../50-fran-poc-till-produktion/styrning-och-risk.md) |
| **Livscykelhantering** | Versionshantering av modell, prompter, index och konfiguration; vad som händer vid byte | [../50-fran-poc-till-produktion/checklista.md](../50-fran-poc-till-produktion/checklista.md) |

De fyra sista är de som saknas i nästan varje demo, och de fyra som avgör om något
kan förvaltas. Det är inte en slump att de också är de tråkigaste att bygga.

## Tre missförstånd som listan reder ut

**"Vilken modell ska vi välja?"** är sällan den viktiga frågan. Två lösningar med
samma modell kan skilja sig totalt i användbarhet, för att den ena har verktyg,
hämtning och utvärdering och den andra inte har det. Modellvalet blir viktigt igen
när det gäller språk, kostnad och var data får behandlas — men då är det inte en
kvalitetsfråga utan en förutsättningsfråga.

**Verktygslagret är ett protokollval, inte en förmåga.** MCP är rör. Det avgör hur
något kopplas in, inte vad det gör. Nästan allt annat på listan kan levereras
igenom det.

**Hämtning, minne och samband är tre olika saker.** De blandas ihop oftare än något
annat på listan:

- hämtning (RAG) svarar på *"vad står det om X i våra dokument?"*
- minnesbanken svarar på *"vad brukar vi göra i sådana här lägen?"*
- grafen svarar på *"vad hänger ihop med det här?"*

En lösning som känns nästan rätt men aldrig blir användbar har nästan alltid fått
fel av de tre.

## Nivåstegen: språket som håller i ett möte

Byggstenslistan är rätt karta för oss och fel karta för ett verksamhetsmöte. Där
fungerar en stege med fyra steg bättre, för den beskriver **hur mycket arbete
lösningen tar över** — vilket är det verksamheten faktiskt vill veta.

| Nivå | Vad den gör | Vad den kräver av oss | Vad den kräver av användaren |
|---|---|---|---|
| **1 · Allmänt stöd** | Generell assistent i de verktyg man redan använder. Förklarar, föreslår, skriver utkast | I princip inget utöver åtkomst | Att kunna bedöma svaret |
| **2 · Stöd som kan vårt** | Samma sak, men grundat i våra egna riktlinjer, mallar och begrepp | Att underlaget finns, är korrekt och hålls aktuellt | Att kunna bedöma svaret |
| **3 · Stöd som gör** | Arbetar igenom flera moment: analyserar, föreslår en plan, tar fram ett utkast som granskas | Kontrollpunkter, granskning, spårbarhet | Att granska och godkänna |
| **4 · Stöd som gör i systemen** | Får dessutom utföra åtgärder i gemensamma system inom givna ramar | Behörighetsmodell, loggning, avgränsat mandat | Att övervaka och kunna ingripa |

Två saker gör stegen användbar:

**Nivåerna bygger på varandra.** Arbetet med nivå 2 — att göra våra egna riktlinjer
och mallar användbara för ett AI-stöd — är inte bortkastat om man senare vill till
nivå 3. Det är förutsättningen för att nivå 3 ska bli bra. Det är ett argument som
brukar landa, för det gör en försiktig start till en investering i stället för en
omväg.

**Kraven växer snabbare än nyttan.** Steget från 3 till 4 är litet i funktion och
stort i styrning: nu ska något utföra åtgärder i system som annars hanteras via
etablerade roller och processer. Det är rätt ställe att ha ett samtal om mandat,
inte om teknik.

Det är också en ärlig stege. Nivå 1 ger sällan mätbar effekt på ledtider — den
sänker trösklar. Att lova annat är att bygga in en besvikelse.

## Hur vi använder det här

I ett användningsfall: skriv vilken nivå förslaget avser och vilka byggstenar det
förutsätter. Det gör två annars osynliga saker synliga — vad som saknas, och vad
förslaget inte lovar.

I matchningen: se
[../40-matchning/typfall-och-byggstenar.md](../40-matchning/typfall-och-byggstenar.md),
som är vår karta över vilka byggstenar olika slags användning brukar kräva. Den
kartan är hypoteser tills experimenten har prövat dem.

## Vad vi ännu inte vet

- Håller nivåstegen i verkliga samtal, eller kollapsar den till "chattbot eller
  agent"?
- Var går den faktiska gränsen mellan nivå 2 och 3 i arbete som vårt — är det
  autonomin eller granskningsbarheten som avgör?
- Hur mycket av nivå 2:s arbete är innehållsarbete (skriva om våra egna underlag så
  att de går att använda) snarare än teknik? Misstanken är: det mesta.

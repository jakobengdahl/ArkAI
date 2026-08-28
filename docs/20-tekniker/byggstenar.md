# Byggstenar och nivåer

En AI-lösning är inte en produkt, den är ett antal byggstenar satta i ett upplägg.
Modellen är en av dem, och sällan den som avgör om det blir användbart.

Den här sidan finns av två skäl. Dels för att kunna resonera om *vad* ett förslag
faktiskt består av innan man diskuterar produkter. Dels för att kunna prata om det
med verksamheten utan att införa nio nya begrepp — se
[nivåstegen](#nivåstegen-språket-som-håller-i-ett-möte) längst ned, som är den del
som fungerar i ett möte.

## Byggstenarna

![Användaren möter applikationslagret, som går vidare till orkestreringen och
modellen. Orkestreringen drar in kontext och minne, verktygslagret och arbetssätt som
paket, vilka i sin tur når källsystem, register och dokument. Runt om alltihop ligger
behörighet, loggning och mänsklig översyn; under ligger driftmiljö, utvärdering och
livscykelhantering.](../bilder/anatomi.svg)

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

## När modellen inte räcker

Språkmodellen ligger i botten av varje AI-lösning och är sällan mycket mer än botten.
Den kan formulera, resonera och sammanfatta. Den vet inget om vår verksamhet, den kan
inte göra något, och den har inga spärrar. Allt sådant byggs på ovanpå, i lager — och
det är påbyggnaden, inte modellvalet, som avgör vad lösningen klarar.

![Sex lager staplade på varandra. Nederst språkmodellen, därefter kontext och
hämtning, verktyg, arbetssätt som paket, orkestrering och överst kontroller och
spärrar. Till höger står vad varje påbyggnad svarar mot.](../bilder/pabyggnad.svg)

Riktningen i bilden är hela poängen: man börjar inte med att välja teknik, man börjar
med att konstatera vad som saknas. Varje lager finns för att svara mot en brist som
går att peka på.

| Det som inte räcker | Det man bygger på med | Vad påbyggnaden kostar |
|---|---|---|
| Modellen svarar utifrån vad den råkar minnas | Kontext och hämtning — [RAG](rag-och-vektor.md) mot egna dokument, [metadata](grafminne.md), [kurerade lärdomar](minnesbank.md) | Innehållsarbete. Underlaget måste vara korrekt och hållas aktuellt, annars förstärks felet |
| Modellen kan inte slå upp, räkna eller utföra | Verktyg — tool-calling, [MCP](mcp.md) | Varje verktyg är en integration som ska beskrivas, felhanteras och förvaltas |
| Samma uppgift görs olika varje gång | Arbetssätt som paket — [skills](skills.md), mallar, kontrollsteg | Att skriva ner arbetssättet, vilket oftare är svårare än att koda det |
| Uppgiften har flera steg som måste hänga ihop | Orkestrering — [agentupplägg](agentupplagg.md) | Fler rörliga delar, och svårare att se vilken av dem som gick sönder |
| Ingen kan lita på, förklara eller begränsa det | Kontroller — behörighet, loggning, utvärdering, [mänsklig översyn](../50-fran-poc-till-produktion/styrning-och-risk.md) | Mest arbete, minst demo. Det är också det som avgör om något får användas |

### Fyra skäl att bygga på — och inget av dem är "mer avancerat"

**Säkerhet.** Behörighet per användare i stället för en teknisk användare, filtrering
av vad som får skickas till modellen, loggning av vad som faktiskt hände. Det här är
det vanligaste skälet till att en lösning som fungerar ändå inte får användas.

**Precision.** Hämtning och verktyg flyttar svaret från *vad modellen minns* till
*vad systemet vet*. Det tar inte bort hallucinationer, men det gör dem
kontrollerbara — och det är kontrollerbarheten som gör ett svar användbart.

**Effektivitet och kostnad.** Påbyggnad är inte alltid dyrare. En mindre modell med
bra hämtning kan vara både billigare och bättre än en stor utan. Skills laddar
instruktioner först när de behövs i stället för att ligga i kontexten hela tiden, och
orkestrering låter enkla steg köras av enkla medel.

**Spårbarhet.** Att kunna svara på *varför blev det så här?* kräver att anropen,
kontexten och modellversionen sparats. Det byggs in i förväg eller inte alls — se
[styrning-och-risk.md](../50-fran-poc-till-produktion/styrning-och-risk.md).

### Hur mycket som behövs bestäms av sammanhanget

Hur många lager som behövs avgörs av var lösningen ska köras, inte av hur avancerad
man vill vara. En PoC klarar sig med modellen, ett par dokument och en prompt. Ska
samma sak användas av andra tillkommer loggning, mätning och en ägare. Rör den
känsliga uppgifter tillkommer behörighet, filtrering, gallring och en väg att
eskalera — och då är modellen en liten del av det som ska byggas och förvaltas. Se
[mognadstrappan](../00-oversikt/mognadstrappa.md#samma-funktion-olika-mängd-byggstenar).

Det leder till en regel som är lätt att skriva och svår att följa: **bygg på när
bristen är konstaterad, inte innan.** Att lägga in behörighetsmodell och regressionstest
i steg 1 är ett dyrt sätt att lära sig att idén inte höll. Att låta bli att fråga
*vad skulle krävas här?* är ett dyrt sätt att upptäcka det vid införandet.

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

![Fyra allt högre trappsteg: allmänt stöd, stöd som kan vårt, stöd som gör, och stöd
som gör i systemen. Över varje steg står vilka byggstenar som tillkommer, från modell
och gränssnitt på steg 1 till behörighet, loggning och avgränsat mandat på steg
4.](../bilder/nivastegen.svg)

Stegen har två namn därför att de har två publiker. *Allmänt stöd* och *stöd som gör*
säger vad lösningen tar över, vilket är verksamhetens fråga; *grundläggande
ai-assistent* och *use-case-anpassad ai-agent* säger vad den är, vilket är vår. Det
är samma trappa.

| Nivå | Vad den gör | Vad den kräver av oss | Vad den kräver av användaren |
|---|---|---|---|
| **1 · Allmänt stöd**<br>*grundläggande ai-assistent* | Generell assistent i de verktyg man redan använder. Förklarar, föreslår, skriver utkast | I princip inget utöver åtkomst | Att kunna bedöma svaret |
| **2 · Stöd som kan vårt**<br>*use-case-anpassad ai-assistent* | Samma sak, men grundat i våra egna riktlinjer, mallar och begrepp | Att underlaget finns, är korrekt och hålls aktuellt | Att kunna bedöma svaret |
| **3 · Stöd som gör**<br>*use-case-anpassad ai-agent* | Arbetar igenom flera moment: analyserar, föreslår en plan, tar fram ett utkast som granskas | Kontrollpunkter, granskning, spårbarhet | Att granska och godkänna |
| **4 · Stöd som gör i systemen**<br>*use-case-integrerad ai-agent* | Får dessutom utföra åtgärder i gemensamma system inom givna ramar | Behörighetsmodell, loggning, avgränsat mandat | Att övervaka och kunna ingripa |

Två saker gör stegen användbar:

**Nivåerna bygger på varandra.** Arbetet med nivå 2 — att göra våra egna riktlinjer
och mallar användbara för ett AI-stöd — är inte bortkastat om man senare vill till
nivå 3. Det är förutsättningen för att nivå 3 ska bli bra. Det är ett argument som
brukar landa, för det gör en försiktig start till en investering i stället för en
omväg. Det är samma påbyggnad som beskrivs i
[När modellen inte räcker](#när-modellen-inte-räcker), sedd från verksamhetens håll.

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
- Stämmer ordningen i påbyggnaden, eller går flera av lagren att hoppa över för våra
  användningsfall? Den billigaste prövningen är att ta bort ett lager och se om det
  slutar fungera — se [../40-matchning/typfall-och-byggstenar.md](../40-matchning/typfall-och-byggstenar.md).

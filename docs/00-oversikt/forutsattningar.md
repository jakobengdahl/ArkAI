# Förutsättningar

Labbet är inte en fri yta. Det finns redan en styrning för AI i vår typ av
verksamhet — policy, riktlinjer, informationsklassning, riskanalys, beslutsvägar —
och den gäller även det vi gör här.

Det här dokumentet återger inte regelverken. Det svarar på två frågor som annars
ställs för sent: **var i den bilden ligger det vi gör**, och **hur skriver vi
resultaten så att de går att använda av dem som ska besluta?**

Två skäl till att det står först i repot:

**Det som stoppar en lösning är sällan tekniken.** Det är oklarhet om var underlaget
får behandlas, vem som äger frågan, vad som ska loggas och vem som svarar när det
blir fel. Alla de frågorna går att besvara innan man börjar, och de är billiga då.

**Vi behöver kunna prata med verksamheten på deras språk.** Den som ska bedöma ett
förslag tänker i tillämpning, informationsklass och risknivå — inte i RAG och
verktygsanrop. Kan vi inte översätta åt båda hållen blir våra resultat obrukbara,
hur bra experimenten än var.

## Vad som styr, i grova drag

Mönstret ser ungefär likadant ut i hela offentlig sektor. Nivåerna nedan är
oberoende av varandra: en lösning kan vara oproblematisk enligt en och stoppas av en
annan.

| Nivå | Vad den avgör | Vad det betyder i labbet |
|---|---|---|
| **AI-förordningen** (EU 2024/1689) | Risknivå för systemet och vilken roll organisationen har | Vi ska kunna säga vilken risknivå ett förslag hamnar i, och varför |
| **Dataskydd, sekretess, allmänna handlingar** | Vad som får behandlas var, och vad som blir en handling | Vi arbetar inte med riktiga data alls — det är en avgränsning, inte en bedömning |
| **Organisationens AI-policy** | Principerna: ansvarsfull, säker, effektiv användning | Våra resultat ska gå att läsa mot dem utan omskrivning |
| **AI-riktlinjer** | Tillämpningskategori, krav på riskanalys och mänsklig översyn | Avgör vilken sorts underlag ett förslag behöver |
| **Informationssäkerhet och informationsklassning** | Vilken tjänst som får användas till vilket material | Styr valet av miljö innan tekniken diskuteras |
| **Beslutsvägar** — linjen eller förvaltningsobjektens styrgrupper | Vem som får initiera, prioritera och finansiera | Vi initierar inte. Vi levererar underlag till dem som gör det |

Ingen av raderna är vår att tolka självständigt. Att kunna referera till dem korrekt
är däremot en del av arbetet.

## Fyra tillämpningar

Riktlinjerna delar in AI-användning efter **var i verksamheten den sitter**, inte
efter vilken teknik som används. Det är en indelning värd att låna, för risknivån
följer platsen betydligt tydligare än den följer tekniken.

| Tillämpning | Vad det är | Var vi står |
|---|---|---|
| **1 · I statistikproduktionen** | AI som integrerad del av produktionsprocessen | Vi äger den inte. Vi kan resonera om den, inte bygga i den |
| **2a · Interna processer nära produktionen** | Stöd i arbete som gränsar till produktionen — kod, återkommande moment | Utforskande spår. Där ligger de intressantaste frågorna |
| **2b · Administrativa och organisatoriska uppgifter** | Internt arbete utan påverkan på produktionen | Här ligger vårt eget arbete, och här kan något gå hela vägen |
| **3 · Externa gränssnitt** | System som möter uppgiftslämnare, dataleverantörer eller användare av statistiken | Inte i labbet. Kräver ordinarie ordning från början |

Gränsen mellan 2a och 1 är en försiktighetsfråga: finns risk för påverkan på
produktionen gäller de strängare kraven. Det är en bedömning man gör i förväg, inte
i efterhand.

Se [vision-och-mal.md](vision-och-mal.md) för vad "utforskande spår" innebär och var
vårt mandat slutar.

## Fyra saker som gäller allt vi gör

**Inga riktiga data.** Konstruerade exempel med samma form. Det gör att vi slipper
den tyngsta delen av bedömningen och kan arbeta snabbt — men det betyder också att
inget vi mäter här är ett bevis för hur något beter sig på riktigt underlag.

**Allt vi producerar är underlag.** Ett experiment är inte ett beslut, en
rekommendation eller ett åtagande. Också när svaret är "det här fungerar bra" är det
någon annan som avgör om det ska göras.

**Mänsklig granskning är inte en fas, den är ett krav.** Resultat från ett AI-system
ska granskas av en människa som kan bedöma dem. Det gäller även i labbet — särskilt
när vi skriver in något i [minnesbanken](../../minnesbank/), som andra sedan bygger
vidare på.

**Repot är publikt.** Se [RIKTLINJER-INNEHALL.md](../../RIKTLINJER-INNEHALL.md).

## Vad någon kommer att fråga

Ett AI-initiativ bedöms i vår typ av organisation med ungefär de här frågorna. Ett
experiment som besvarar dem i förbifarten är oändligt mycket mer värt än ett som
lämnar dem öppna — det är skillnaden mellan ett resultat och ett underlag.

1. Vilket behov ska det lösa, och hur ser det önskade läget ut?
2. Ligger användningen inom organisationens uppdrag?
3. Vad gör lösningen? Interagerar den med människor eller genererar den nytt innehåll?
4. Vilken information hanteras, och varför just den?
5. Behandlas personuppgifter?
6. Behandlas uppgifter som omfattas av sekretess?
7. Vilken informationsklass har materialet?
8. Vilken kompetens och vilka resurser krävs för att använda och förvalta det?
9. Överstiger nyttan kostnaden för införande **och** förvaltning?
10. Vilka risker föll ut av riskanalysen?

De flesta av dem går att besvara ungefärligt redan under ett experiment. Fråga 4–7
avgör oftast om något överhuvudtaget kan provas och var — ta dem först. Se
[beslutsguiden fråga 4](../40-matchning/beslutsguide.md).

## Risknivå enligt AI-förordningen

Fyra nivåer, och de flesta av våra idéer landar i de två lägsta. Att kunna säga
vilken, och varför, är en liten insats som gör ett förslag mycket lättare att ta
vidare.

| Nivå | Vad som kännetecknar den | Typiskt för oss |
|---|---|---|
| Oacceptabel risk | Förbjuden användning | Ska inte förekomma |
| Hög risk | Bland annat rekrytering och arbetsledning; omfattande krav | Ovanligt i vårt arbete, men bedöm hellre än anta |
| Begränsad risk | Transparenskrav — system som interagerar direkt med människor, genererat innehåll | Chattbotar och genererade utkast hamnar här |
| Minimal eller ingen risk | Inga särskilda krav enligt förordningen | Mycket av det interna stödarbetet |

Bedömningen görs utifrån **hur systemet används**, inte bara hur det är byggt. Samma
teknik kan hamna på olika nivåer i olika sammanhang — vilket är hela poängen med att
beskriva tillämpningen innan tekniken.

Organisationens roll spelar också in: att använda ett inköpt system är inte samma
sak som att släppa ut ett eget på marknaden, och kraven skiljer sig därefter.

## Miljö- och klimataspekten

Både träning och användning av modeller kostar energi. Den rimliga slutsatsen för
oss är inte att avstå, utan att **välja liten modell där en liten modell räcker** —
en rekommendation som återkommer i internationella riktlinjer för statistikmyndigheter.

Det är också en teknisk fråga vi kan besvara i labbet: vilka av våra uppgifter klarar
en mindre modell lika bra? Det är ett experiment ingen har gjort än, och det svarar
på en kostnadsfråga samtidigt.

## Vad det här dokumentet inte är

Det är inte juridisk vägledning och ersätter inte de ordinarie processerna för
informationssäkerhet, dataskydd, programvarugodkännande eller arkitekturstyrning.
Det är en karta över vilka frågor som finns, så att vi kan besvara dem i tid i
stället för att bli överraskade av dem.

## Vidare läsning

- [vision-och-mal.md](vision-och-mal.md) — vad labbet ska åstadkomma, och de två spåren
- [ordlista.md](ordlista.md) — begreppen, inklusive de som kommer från styrningen
- [../50-fran-poc-till-produktion/styrning-och-risk.md](../50-fran-poc-till-produktion/styrning-och-risk.md) — samma frågor, men för något som ska bli skarpt
- [../40-matchning/beslutsguide.md](../40-matchning/beslutsguide.md) — frågorna i den ordning de bör ställas

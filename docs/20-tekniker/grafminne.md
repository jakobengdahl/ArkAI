# Grafminne

Kunskap lagrad som noder och relationer i stället för som textstycken. Frågor
besvaras genom att följa kopplingar, inte genom att hitta liknande text.

## Vad det löser

Vektorsökning hittar det som *liknar* frågan. Den är dålig på det som *hänger ihop*
med frågan.

"Vilka system påverkas om vi ändrar den här definitionen?" är inte en likhetsfråga.
Svaret finns inte i ett stycke text som liknar frågan — det finns i kedjan av
kopplingar från definitionen till det som använder den. Fråga en RAG-lösning och du
får de stycken som råkar nämna definitionen. Fråga en graf och du får kedjan.

För arkitekturarbete är det här inte en randfråga. Beroenden, informationsflöden,
begreppsmodeller, konsekvensanalyser — det är grafproblem, och vi behandlar dem
ofta som dokumentproblem.

## Hur det fungerar

Kunskapen modelleras som **noder** (begrepp, system, personer, beslut) och **kanter**
(använder, ersätter, beror på, beslutades av). En modell kan sedan:

- slå upp en nod och få dess grannar
- följa en kedja flera steg
- ställa frågor som "vad står mellan A och B"

I praktiken kombineras det ofta med vektorsökning: sök fram ingångsnoden semantiskt,
navigera därifrån via relationerna. Semantisk sökning för att *hitta*, grafen för att
*förstå sammanhanget*.

## När det passar

- Beroenden och konsekvensanalys
- Begreppsmodeller där relationerna mellan begreppen är poängen
- Spårbarhet — vilket beslut ledde till vad
- När "vad hänger ihop med det här?" är en fråga folk faktiskt ställer
- När minnesbanken vuxit förbi vad ett textindex klarar

## När det inte passar

- **Litet innehåll.** En graf med 40 noder är krångligare än en katalog med 40 filer,
  utan att ge något tillbaka.
- **När relationerna inte är stabila.** Modelleringen är arbetet. Ändras strukturen
  hela tiden får du underhållsarbete utan nytta.
- **Som första steg.** Bygg textminnet först, se var det tar slut, och låt gränserna
  visa vilka relationer som faktiskt behövs. Att modellera i förväg leder nästan
  alltid till en modell ingen använder.
- **Om ingen kan Cypher eller motsvarande.** Frågespråket är ett verkligt hinder —
  även om en LLM kan skriva frågorna behöver någon kunna avgöra om de är rätt.

## Vad det kostar

Modelleringen, framför allt. Att välja nodtyper och relationstyper är
arkitekturarbete i sig — vilket gör det till en intressant övning för oss, men det är
inte gratis.

Sedan tillkommer en tjänst att förvalta (Neo4j finns i Onyxias katalog), och
kunskapen att ställa frågor mot den.

## Testa i labbet

Neo4j startas från Onyxias katalog. Se
[../60-miljo/sspcloud-onyxia.md](../60-miljo/sspcloud-onyxia.md) — kom ihåg
Kubernetes-rollen och portinställningen vid start.

Ett rimligt första experiment är litet: ta 20–30 poster ur
[minnesbanken](../../minnesbank/), modellera dem som noder och relationer, och
ställ tre frågor som textindexet inte klarar. Går det inte att formulera tre sådana
frågor är det ett svar i sig — då är vi inte där än.

## Vad vi har provat

| Experiment | Vad vi lärde oss |
|---|---|
| — | *(inget än)* |

## Vad vi ännu inte vet

- Vilka nodtyper och relationstyper behöver vi faktiskt? (Börja tomt, låt behovet styra)
- Kan en LLM underhålla grafen själv, eller blir den obrukbar utan mänsklig kuratering?
- Hur får man in en graf i kontexten på ett vettigt sätt? Ett delgrafsutdrag som text?
- Är det en graf vi behöver, eller bara bättre länkar mellan textfiler? Det är den
  ärliga frågan att ställa först.

## Vidare läsning

- [minnesbank.md](minnesbank.md)
- [rag-och-vektor.md](rag-och-vektor.md)

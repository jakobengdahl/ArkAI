# Labbet

En experimentyta för att ta reda på vad AI faktiskt kan göra i vårt arbete — och
vad som krävs för att ta något hela vägen från demo till drift.

Den här sidan är startsidan i [labbpanelen](60-miljo/panelen.md). Blocken nedan är
tomma när du läser filen på GitHub och fyllda när du läser den i panelen.

## Kartan: en lösning är byggstenar, inte en produkt

![Användaren möter applikationslagret, som går vidare till orkestreringen och
modellen. Orkestreringen drar in kontext och minne, verktygslagret och arbetssätt som
paket, vilka i sin tur når källsystem, register och dokument. Runt om alltihop ligger
behörighet, loggning och mänsklig översyn; under ligger driftmiljö, utvärdering och
livscykelhantering.](bilder/anatomi.svg)

Ingen lösning använder alla. Poängen med kartan är att kunna se vilka ett förslag
saknar, för det är där de obehagliga överraskningarna sitter — och de fyra nedersta
(driftmiljö, utvärdering, mänsklig översyn, livscykelhantering) är de som saknas i
nästan varje demo. Hela resonemanget står i
[byggstenar.md](20-tekniker/byggstenar.md); nivåstegen som fungerar i ett
verksamhetsmöte finns
[längst ned där](20-tekniker/byggstenar.md#nivåstegen-språket-som-håller-i-ett-möte).

Nedan är samma karta lagd över det som faktiskt går att starta här. Ett verktyg
beskriver sig alltid med sitt eget produktspråk; byggstenarna är det gemensamma
måttet som gör två verktyg jämförbara — och som visar vad du behöver bygga på med.

## Verktygen, och vad de består av

Varje kort säger vilka byggstenar verktyget innehåller, vilka som måste ställas in
och vilka det inte har. Knapparna gör det: starta, stoppa, ta bort, och koppla in i
Eneo där det går.

<!-- panel:verktyg -->

**Stoppa och Ta bort är två olika saker.** *Stoppa* släpper processerna och skalar
arbetslasterna i namnrymden till noll — inga poddar blir kvar och ingenting tar
CPU eller minne, men all data ligger kvar på volymerna. *Ta bort* raderar. Kör
*Stoppa* när du är klar för dagen; det är det som gör att en labbmiljö inte lämnar
igångvarande tjänster efter sig. Se [eneo.md](60-miljo/eneo.md#ta-bort-eneo-igen).

## Vad kör just nu

<!-- panel:status -->

## Att koppla in något i Eneo

Eneo har **inga verktyg från början**, och ingen inbyggd verktygslåda. Adminen
lägger upp MCP-servrar per organisation, och sedan väljer varje assistent vilka av
deras verktyg den får använda. Modellerna fungerar likadant: ingen modell finns
förrän en leverantör är upplagd.

Det är därför korten ovan har en *koppla in*-knapp: den skriver det som annars är
sexton klick i ett formulär, och den kan köras om när du bytt nyckel eller startat
om en server. Två saker begränsar vad som går att koppla in:

- **Eneo pratar bara Streamable HTTP.** Inte stdio, inte SSE. En stdio-server måste
  köras över HTTP för att gå att koppla in.
- **Eneo kör i namnrymden, inte i den här podden.** Den når bara servrar som ligger
  på en exponerad port, alltså ett publikt värdnamn — och då behövs en token.

Det gäller [Hello-MCP](../exempel/mcp/hello-mcp/README.md), som kör båda
transporterna av just det skälet. Se [eneo.md](60-miljo/eneo.md) och
[mcp.md](20-tekniker/mcp.md).

## Vad vi försöker ta reda på

1. **Vilka användningsfall** i vårt arbete tjänar på AI — och vilka gör det inte?
2. **Vilka AI-tekniker** finns, och vad är de faktiskt bra på?
3. **Hur matchar man rätt teknik mot rätt användningsfall?**
4. **Vad krävs för att gå från PoC till produktion** — styrning, drift, kostnad, risk?

Fråga 3 och 4 är de svåra. Fråga 1 och 2 är förarbetet.

Vi jobbar i [två spår](00-oversikt/vision-och-mal.md#två-spår): sådant vi själva
ansvarar för, som kan gå hela vägen, och utblickar mot verksamhet andra ansvarar för,
där resultatet är ett underlag att ta vidare tillsammans med dem. Vad styrningen
kräver i respektive: [förutsättningar](00-oversikt/forutsattningar.md).

Ny här? [Läsordningen](README.md) tar dig igenom repot. Har du en halvtimme och vill
göra något: starta **Eneo** ovan, tryck *Koppla in modellerna*, och läs
[eneo.md](60-miljo/eneo.md) medan installationen går. Den tar en plattform hela vägen
till något som liknar drift, och det är där de svåra frågorna sitter.

## Miljön

<!-- panel:miljo -->

### Tjänster i din namnrymd

Det här kör redan, oberoende av den här podden. Somligt ligger bakom inloggning.

<!-- panel:namnrymd -->

### Vad du har igång, och vad det kostar

Allt nedan lever kvar när den här podden stoppas — det är poängen med att köra
saker i namnrymden, och samtidigt det som gör att kvoten tar slut om ingen städar.
Tjänster som labbet självt deployat står med i kolumnen *Del av*. Är du klar för
dagen: *Stoppa* på kortet ovan tar ner poddarna men behåller datan.

<!-- panel:kvot -->

## När du hittat något

Ett experiment ska sluta med ett skrivet svar — även när svaret är "det här funkade
inte". Lärdomen som nästa person behöver *innan* de börjar hör hemma i
[minnesbanken](../minnesbank/MINNE.md), inte bara i experimentfilen.

Se [BIDRA.md](../BIDRA.md) för hur du lägger till något.

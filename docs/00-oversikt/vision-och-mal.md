# Vad vi vill uppnå

## Problemet

AI-verktygen är bra nog för att vara användbara i vårt arbete, och de förändras
snabbare än vi hinner utvärdera dem. Två saker går fel om vi inte gör något åt det:

**Var och en lär sig samma sak enskilt.** Den som suttit en kväll och listat ut hur
man får en agent att förstå vår domän har den kunskapen i huvudet och i sin egen
chatthistorik. Nästa person börjar om från noll. Det skalar inte, och det är inte
ens tydligt för oss själva hur mycket dubbelarbete som pågår.

**Piloter blir liggande.** En demo som imponerar på ett möte är inte samma sak som
något som går att förvalta. Vi vet inte tillräckligt om vad som skiljer, så vi
bygger antingen demos som aldrig går vidare, eller drar oss för att börja alls.

**Samtalet fastnar i begrepp.** Den som frågar "kan AI hjälpa oss med det här?" vill
inte ha en genomgång av RAG, verktygsanrop och agentloopar. Kan vi inte klustra
teknikerna till ett fåtal saker som går att välja mellan, blir varje samtal en
utbildning — och beslutet skjuts upp igen.

## Vad vi gör åt det

Det här repot är en gemensam yta för att arbeta systematiskt med problemen.

### 1. Kartlägg användningsfallen

Vad gör vi faktiskt, och var finns det arbete som en AI skulle kunna ta? Skrivet
avidentifierat så att det går att prata om öppet. → [10-anvandningsfall/](../10-anvandningsfall/)

### 2. Lär känna teknikerna

Inte "AI" som en klump, utan de faktiska byggstenarna: chattbot med verktygsåtkomst,
MCP, kodagenter, skills, minnesbanker, RAG, grafer. Varje teknik har ett eget dokument
med vad den är bra på och var den går sönder. → [20-tekniker/](../20-tekniker/)

### 3. Matcha teknik mot användningsfall

Det är här värdet ligger. Fel teknik på rätt problem ser ut som att AI inte fungerar.
→ [40-matchning/](../40-matchning/)

### 4. Ta reda på vad produktion kräver

Vad behövde vi som vi inte hade? Vad kostade det? Vad gick sönder när fler än en
person använde det? → [50-fran-poc-till-produktion/](../50-fran-poc-till-produktion/)

### 5. Dela minnet, inte bara koden

Genomgående i allt ovanstående: kunskapen vi bygger upp ska ligga på ett ställe som
både människor och AI-verktyg kan läsa. → [minnesbank/](../../minnesbank/)

Det är den delen vi tror är mest underskattad. Ett experiment vars lärdom bara finns
i experimentfilen kommer att göras om.

## Vad arbetet ska ge oss

Tre saker, i den här ordningen. De hänger ihop, men den som bara gör den första har
ändå fått ut något.

**1. Kompetens som sitter i händerna, inte i presentationer.** Vi ska ha kört
teknikerna själva. Det är skillnad på att veta vad en agent är och att ha sett en
agent göra fel på ett sätt man inte förutsåg. Learning by doing är inte en pedagogisk
preferens här — det är enda sättet att bygga den bedömningsförmåga vår roll kräver.

**2. En karta över vilken teknik som behövs för vilket slags fall.** Inte "AI kan
det här", utan: den här sortens användning kräver de här byggstenarna, och klarar sig
utan de där. Se [10-anvandningsfall/typfall.md](../10-anvandningsfall/typfall.md) och
[20-tekniker/byggstenar.md](../20-tekniker/byggstenar.md).

**3. Ett språk som håller i ett verksamhetsmöte.** Ett fåtal kluster och en
nivåstege som går att välja mellan, i stället för nio tekniker som ingen utanför
labbet kan skilja på. Om vi behöver introducera fem nya begrepp för att förklara ett
förslag har vi inte förstått det tillräckligt bra själva.

## Två spår

Vår roll spänner över mer än det vi själva ansvarar för. Det gäller även här, och
det är värt att vara uttalad om skillnaden — annars blir det otydligt både för oss
och för dem vi jobbar med.

| | **Eget spår** | **Utforskande spår** |
|---|---|---|
| Gäller | arbete vi själva ansvarar för | verksamhet någon annan ansvarar för |
| Frågan vi ställer | "kan vi göra det här bättre?" | "vad kommer att vara möjligt, och vad kräver det?" |
| Hur långt vi går | hela vägen — PoC, pilot, produktion | till en genomförd prövning och ett skrivet resultat |
| Vad det slutar med | en lösning någon använder | ett paketerat underlag att ta vidare *tillsammans med* den som äger frågan |
| Vad det inte är | — | ett förslag på vad någon annan borde göra |

**Det utforskande spåret är inte utanför uppdraget.** Att veta vad som blir möjligt i
nästa steg är en del av arkitekturrollen; det är svårt att ge vägledning om något man
aldrig kört. Det som ligger utanför är att gå vidare mot införande på egen hand i
någon annans verksamhet.

Skillnaden är alltså inte *vad* vi får prova, utan *vad resultatet blir*. I det
utforskande spåret är resultatet kunskap och ett underlag — inte en lösning som
väntar på att bli införd. Att komma dragande med en färdig lösning till någon som
äger frågan är ett säkert sätt att få den avvisad, oavsett hur bra den är.

Praktiskt: markera spåret överst i användningsfallet, tillsammans med
[mognadssteget](mognadstrappa.md). I det utforskande spåret stannar trappan vid PoC,
och nästa steg är en dialog — inte en pilot.

Se [forutsattningar.md](forutsattningar.md) för vilka tillämpningsområden det handlar
om och vad som gäller i respektive.

## Så här vet vi att det fungerar

Inte "vi har byggt X", utan:

- En ny kollega kan läsa sig till vad vi redan vet, i stället för att fråga eller
  gissa.
- Vi kan svara på "passar AI för det här?" med ett underbyggt svar i stället för en
  känsla — inklusive svaret nej, när det är rätt svar.
- Vi har minst ett användningsfall som gått hela vägen, och vi kan beskriva exakt
  vad som krävdes.
- Vi kan visa på något vi provade och lade ner, med skäl.
- Fler än en av oss har kört varje teknik själv, inte bara läst om den.
- Minst ett underlag från det utforskande spåret har landat hos den som äger frågan,
  och lett till ett samtal snarare än till ingenting.

## Så här vet vi att det inte fungerar

- Repot fylls med struktur men inga resultat.
- Experimenten dokumenteras bara när de lyckades.
- Minnesbanken blir en dumpningsplats som ingen läser.
- Vi bygger verktyg åt oss själva i stället för att lösa verksamhetens problem.
- Det utforskande spåret glider över i att vi föreslår saker i andras verksamhet.

Det är rimliga saker att ta upp när vi stämmer av med varandra.

## Avgränsningar

Det här är ett labb, inte ett projekt. Vi bygger inget som någon ska förlita sig på.
Vi hanterar ingen verklig data. Vi tar inga beslut åt verksamheten.

Det vi producerar är underlag: kunskap om vad som fungerar, för vem, till vilken
kostnad, och vad steget till skarpt läge skulle innebära.

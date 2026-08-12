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

## Vad vi gör åt det

Det här repot är en gemensam yta för att arbeta systematiskt med båda problemen.

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

## Så här vet vi att det fungerar

Inte "vi har byggt X", utan:

- En ny kollega kan läsa sig till vad vi redan vet, i stället för att fråga eller
  gissa.
- Vi kan svara på "passar AI för det här?" med ett underbyggt svar i stället för en
  känsla — inklusive svaret nej, när det är rätt svar.
- Vi har minst ett användningsfall som gått hela vägen, och vi kan beskriva exakt
  vad som krävdes.
- Vi kan visa på något vi provade och lade ner, med skäl.

## Så här vet vi att det inte fungerar

- Repot fylls med struktur men inga resultat.
- Experimenten dokumenteras bara när de lyckades.
- Minnesbanken blir en dumpningsplats som ingen läser.
- Vi bygger verktyg åt oss själva i stället för att lösa verksamhetens problem.

Det är rimliga saker att ta upp när vi stämmer av med varandra.

## Avgränsningar

Det här är ett labb, inte ett projekt. Vi bygger inget som någon ska förlita sig på.
Vi hanterar ingen verklig data. Vi tar inga beslut åt verksamheten.

Det vi producerar är underlag: kunskap om vad som fungerar, för vem, till vilken
kostnad, och vad steget till skarpt läge skulle innebära.

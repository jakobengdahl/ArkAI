# Checklista: vad krävs för att gå vidare?

Den här listan finns för att göra samtalet konkret. Den är inte en grind någon måste
passera — den är en uppsättning frågor som annars ställs för sent, ofta av någon
annan än den som byggde.

Använd den i två lägen: **innan** en pilot, och **innan** något får kallas produktion.

Se [mognadstrappan](../00-oversikt/mognadstrappa.md) för vad stegen betyder.

---

## Innan pilot

Piloten har riktiga användare. Det är där de flesta lösningar dör, och nästan aldrig
av tekniska skäl.

### Syfte och ägarskap

- [ ] En namngiven person äger piloten
- [ ] Det står skrivet vad "fungerar" betyder — **innan** starten
- [ ] Det finns ett slutdatum
- [ ] Det är bestämt vem som beslutar om fortsättning, och när

### Användarna

- [ ] Det är klart vilka de är och att de vet om att de är piloter
- [ ] De kan bedöma om svaret är rätt — se
      [beslutsguide fråga 2](../40-matchning/beslutsguide.md)
- [ ] Det finns ett sätt för dem att säga till när något blir fel
- [ ] De kan låta bli att använda det utan att det blir ett problem

Den sista är en kvalitetsmätare: ett verktyg folk slutar öppna har inte lyckats,
oavsett vad statistiken visar.

### Data

- [ ] Det är klarlagt vilket underlag som får användas och var det får behandlas
- [ ] Det är klart vad som händer med det användarna matar in — sparas det, var,
      hur länge, vem kommer åt det?
- [ ] Om leverantören ligger utanför: vad har lovats om vad de gör med underlaget?

### Att veta om det fungerar

- [ ] Det finns en uppsättning fall med kända svar
- [ ] Det finns en mätning gjord innan (hur lång tid tar det idag?)
- [ ] Det går att se vad systemet faktiskt gjorde i efterhand — Langfuse eller
      motsvarande finns i Onyxias katalog
- [ ] Kostnaden per användning är känd, åtminstone i storleksordning

### Det som brukar glömmas

- [ ] Vad händer när modellen svarar självsäkert fel? Märks det?
- [ ] Vad händer när tjänsten ligger nere?
- [ ] Vad kostar det om användningen blir tio gånger större än väntat?

---

## Innan produktion

Nu förlitar sig någon på det. Det är en förvaltningsfråga, inte ett projekt.

### Förvaltning

- [ ] Det finns en förvaltningsorganisation, inte bara en eldsjäl
- [ ] Någon har mandat och budget att fortsätta utveckla
- [ ] Det finns en väg in för användarna när något inte fungerar
- [ ] Det är bestämt vad som gäller när det ska avvecklas

Punkt ett är den som fäller flest. En lösning som bara en person förstår är inte i
produktion, oavsett var den kör.

### Teknik

- [ ] Modellberoendet är känt och hanterat — vad händer när modellen byts eller
      utgår? Se [sspcloud-llm.md](../60-miljo/sspcloud-llm.md)
- [ ] Det finns regressionstester mot de kända fallen, som körs vid modellbyte
- [ ] Åtkomsten följer användarens behörigheter, inte en teknisk användares
- [ ] Prompter, skills och konfiguration är versionshanterade
- [ ] Det går att spåra vad som hände i ett enskilt fall, i efterhand

Punkten om behörigheter är den som oftast kräver mest ombyggnad, och den upptäcks
oftast sist. Ta upp den redan i pilotplaneringen.

### Kvalitet över tid

- [ ] Någon tittar återkommande på om kvaliteten hållit i sig
- [ ] Det finns en plan för när underlaget ändras — reindexering, uppdaterade skills
- [ ] Det är känt hur användarna märker att svaret är osäkert

### Styrning

- [ ] Det är klarlagt vad regelverken kräver för just den här användningen
- [ ] Det är dokumenterat vad systemet gör, för någon som inte byggde det
- [ ] Ansvaret för besluten som fattas med stöd av systemet är utpekat

Se [styrning-och-risk.md](styrning-och-risk.md).

---

## Hur listan används

Gå igenom den och skriv ner vad ni **inte** kan bocka av. Den listan är resultatet —
inte antalet bockar.

Det som saknas är antingen arbete som återstår eller en medveten risk. Båda går bra;
det som inte går bra är att inte veta vilket det är.

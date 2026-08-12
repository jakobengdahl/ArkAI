---
namn: index-fore-innehall
beskrivning: Lägg ett kort index i kontexten och hämta detaljer vid behov — allt-på-en-gång blir sämre, inte bättre, när mängden växer.
typ: arbetssatt
uppdaterad: 2026-08-12
---

När vi ger en modell tillgång till kunskap — minnesbanken, dokumentation, en kodbas —
lägger vi in ett **index** i kontexten, inte innehållet. Indexet är en rad per sak,
med en beskrivning som räcker för att avgöra relevans. Modellen hämtar sedan de
enskilda filer den behöver.

**Varför:** intuitionen säger att mer kontext ger bättre svar. Det stämmer upp till
en punkt och blir sedan tvärtom: i en full kontext blir det svårare för modellen att
hitta det som faktiskt är relevant, och sannolikheten ökar att den plockar upp något
närliggande men fel. Ett index på 40 rader kostar nästan ingenting och gör att
modellen *vet vad som finns* — vilket är det den behöver för att kunna fråga rätt.

Samma princip gäller varför skills laddas selektivt i stället för att ligga i
systemprompten.

**Så använder du det:** `minnesbank/MINNE.md` är mönstret. Beskrivningsraden är den
viktigaste delen — skriv den som ett sökresultat, inte som en rubrik. En post som
beskrivs dåligt hämtas inte, oavsett hur bra den är.

Gäller lika mycket för människor: ingen läser 300 filer, men alla kan skumma ett
index.

Relaterat: [[dokumentera-negativa-resultat]]

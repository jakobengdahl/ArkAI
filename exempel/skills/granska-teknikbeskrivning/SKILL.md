---
name: granska-teknikbeskrivning
description: Använd när en teknikbeskrivning i docs/20-tekniker/ ska granskas eller skrivas — kontrollerar att den är ärlig, konkret och följer repots form. Använd inte för användningsfall eller experiment, de har egna former.
---

# Granska en teknikbeskrivning

Det här är ett **exempel på en skill** — ett arbetssätt paketerat så att ett
AI-verktyg kan ladda in det när det behövs. Se
[docs/20-tekniker/skills.md](../../../docs/20-tekniker/skills.md).

Beskrivningsraden i frontmatter ovan är det som avgör om skillen laddas alls. Notera
att den säger både *när den ska användas* och *när den inte ska det*. Det är
skillnaden mellan en skill som laddas i rätt läge och en som laddas slumpmässigt.

## Uppgiften

Granska en fil i `docs/20-tekniker/` mot punkterna nedan. Rapportera vad som saknas
eller är svagt — ändra inte filen utan att fråga.

## Kontrollera

### 1. Har den ett "när det inte passar"-avsnitt, och är det ärligt?

Det viktigaste. En teknikbeskrivning utan trovärdiga begränsningar är
marknadsföringsmaterial.

Svaga formuleringar att reagera på: "kräver viss uppsättning", "behöver anpassas
till våra behov", "fungerar bäst när man har rätt data". De säger ingenting.

Bra begränsningar är konkreta och beskriver ett läge man faktiskt hamnar i:
"vektorsökning missar exakta beteckningar och koder".

### 2. Står det vad som *inte* fungerar?

Sök efter påståenden som bara är positiva. Om avsnittet "Vad vi har provat" är
ifyllt men bara innehåller lyckade resultat — fråga vad som gick fel på vägen.

### 3. Skiljer den på erfarenhet och gissning?

"Vad vi har provat" ska bara innehålla rader som pekar på ett genomfört experiment.
Antaganden hör hemma under "Vad vi ännu inte vet".

Blandas de ihop blir dokumentet trovärdigare än det förtjänar.

### 4. Är kostnaden beskriven som mer än pengar?

Uppsättningstid, förvaltning, kontextförbrukning, vem som måste kunna det. Se
[docs/50-fran-poc-till-produktion/kostnad-och-drift.md](../../../docs/50-fran-poc-till-produktion/kostnad-och-drift.md).

### 5. Går det att förstå utan att kunna tekniken?

Målgruppen är en arkitektkollega som inte jobbat med just den här tekniken.
Facktermer ska finnas i [ordlistan](../../../docs/00-oversikt/ordlista.md) eller
förklaras.

### 6. Följer den mallen?

[MALL-teknik.md](../../../docs/20-tekniker/MALL-teknik.md). Rubriker får utelämnas
när de inte är relevanta, men inte "När det inte passar".

### 7. Innehåller den något som inte hör hemma i ett publikt repo?

[RIKTLINJER-INNEHALL.md](../../../RIKTLINJER-INNEHALL.md).

## Rapportera så här

Kort. Peka på rad eller rubrik. Sortera efter vad som betyder mest.

```
docs/20-tekniker/exempel.md

Saknas
- "När det inte passar" har tre punkter, alla formulerade som förutsättningar
  snarare än begränsningar. Vad går faktiskt sönder?
- Kostnadsavsnittet nämner bara tokens. Vem ska förvalta det?

Otydligt
- "Fungerar bra för de flesta fall" — vilka fall är det som inte fungerar?

Bra
- Skillnaden mot RAG är tydligt beskriven och kommer tidigt.
```

Ta med det som är bra. En granskning som bara listar brister får folk att sluta be om
granskningar.

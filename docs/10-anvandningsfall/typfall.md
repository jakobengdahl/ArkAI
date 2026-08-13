# Typfall

Sex slags AI-användning. Sätt typfallet överst i varje användningsfall — det säger
mer om vad som krävs än beskrivningen av uppgiften gör.

Poängen är att undvika två ytterligheter som båda leder fel. Att behandla AI som en
enda teknik gör att alla förslag bedöms likadant, vilket antingen blir för strängt
eller för slappt. Att behandla varje fall som unikt gör att ingenting kan
återanvändas och varje bedömning börjar om från noll.

Indelningen bygger på mönster som återkommer i statistikmyndigheter internationellt,
och den håller förvånansvärt väl även utanför den världen.

## De sex typfallen

| | Typfall | Vad som kännetecknar det |
|---|---|---|
| **A** | **Smal AI som ersätter en metod** | Modell tränad för en väldefinierad uppgift inne i en produktionskedja — klassificering, kodning, imputering. Ersätter regelbaserade eller traditionella statistiska metoder |
| **B** | **Språkmodeller som ersätter textmetoder** | Icke-generativa språkmodeller för klassificering och textbearbetning. Bredare än A, men fortfarande tätt knuten till en befintlig kedja |
| **C** | **Generativa system i produktionsprocessen** | Generativ AI som kompletterar eller delvis ersätter etablerade produktionsmoment — granskning, transformering, tolkning. Ofta i kombination med smala modeller |
| **D** | **Generativt stöd i interna processer** | Stöd utanför själva produktionskedjan: dokumentation, metadata, kunskapsstöd, programmering |
| **E** | **Generativ AI i externa gränssnitt** | Möter uppgiftslämnare, dataleverantörer eller användare av statistiken |
| **F** | **Generellt administrativt stöd** | Allmän kontorsproduktivitet: skriva, sammanfatta, söka. Delas med varje annan organisation |

## Vad typfallet avgör

Det är inte en etikett. Det säger något om vad som faktiskt krävs.

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| Finns det facit att mäta mot? | ja | ja | delvis | sällan | sällan | nej |
| Hur svårt är det att utvärdera? | lätt | lätt | svårt | medel | svårt | inte meningsfullt |
| Krav på spårbarhet | högt | högt | högt | medel | högt | lågt |
| Mänsklig översyn | stickprov | stickprov | granskning i varje steg, till en början | granskning av det som används | eskaleringsvägar och tillsyn | ingen särskild |
| Vem äger det hos oss | annan | annan | annan | vi, delvis | annan | alla |
| Vårt [spår](../00-oversikt/vision-och-mal.md) | utforskande | utforskande | utforskande | eget | inte i labbet | eget |

Två observationer som är värda mer än tabellen:

**A och B har facit, C till E har det inte.** Det är den skarpaste skiljelinjen i
hela indelningen. När det finns kända rätta svar är utvärdering en mätfråga. När det
inte gör det måste utvärderingen konstrueras — scenarier, robusthetstest,
strukturerad expertgranskning — och det arbetet underskattas i princip alltid.

**F är inte ointressant, men det är inte vårt.** Generellt kontorsstöd styrs på
organisationsnivå och skiljer sig inte från någon annan verksamhets. Vi kan använda
det och lära oss av det, men det finns lite att bidra med som är specifikt för vårt
uppdrag. Lägg inte utrymme där.

## Var vår tyngdpunkt ligger

**D är vårt eget område.** Dokumentation, metadata, kunskapsstöd, kodstöd — det är
arbete vi själva ansvarar för. Här kan ett användningsfall gå hela vägen till
pilot och vidare, och det är här mognadstrappan ska användas som den är tänkt.

**C och A–B är utforskande.** De sitter i produktionen, och den äger vi inte. Vi kan
och bör pröva dem i labbet — det är svårt att ge arkitekturvägledning om något man
aldrig kört — men resultatet är kunskap och ett underlag, inte en lösning som väntar
på införande. Se [de två spåren](../00-oversikt/vision-och-mal.md#två-spår).

**E rör vi inte i labbet.** Ett system som möter någon utanför organisationen har
risker vi inte kan hantera i en experimentmiljö: prompt injection, medvetet skadliga
interaktioner, behov av övervakning dygnet runt. Det behöver ordinarie ordning från
första dagen.

## Vad man vinner på att sätta typfall

Det gör tre annars långsamma samtal snabba:

1. **Vad ska utvärderas, och går det?** Typfallet avgör om facit finns.
2. **Hur mycket styrning krävs?** Kraven följer var användningen sitter, inte hur
   avancerad tekniken är. Se
   [00-oversikt/forutsattningar.md](../00-oversikt/forutsattningar.md).
3. **Vem ska vi prata med?** Typfallet pekar ut vem som äger frågan — och därmed om
   vi ska bygga eller lämna över.

## Hur det används

Skriv typfallet överst i användningsfallet, tillsammans med spår och mognadssteg:

```
**Typfall:** D · Generativt stöd i interna processer
**Spår:** Eget
**Steg:** PoC
```

Ett fall som spänner över flera typfall är oftast två fall. Dela det.

## Vidare läsning

- [../20-tekniker/byggstenar.md](../20-tekniker/byggstenar.md) — vad en lösning består av
- [../40-matchning/typfall-och-byggstenar.md](../40-matchning/typfall-och-byggstenar.md) — vilka byggstenar respektive typfall brukar kräva
- [../00-oversikt/forutsattningar.md](../00-oversikt/forutsattningar.md) — vad styrningen kräver var

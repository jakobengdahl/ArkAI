# Från demo till drift

En AI-lösning kan vara imponerande och samtidigt helt otillräcklig. Skillnaden syns
inte i demon — den syns i vad som händer när den ska användas av andra än den som
byggde den, varje dag, i ett år.

Den här trappan är till för att vi ska kunna prata om var något faktiskt befinner
sig, och vad som återstår.

## Stegen

### 0 · Skiss
Någon har en idé. Kanske en prompt som gav ett lovande svar en gång.

Räcker som skiss: att det är skrivet någonstans. Lägg det som ett användningsfall.

### 1 · PoC
Visar att det går. Byggd av en person, körd av samma person, går sönder om man
klickar fel.

**Frågan den svarar på:** är det här tekniskt möjligt?

Klar när: det finns ett dokumenterat experiment med ett svar. Även "nej" är ett svar,
och ett billigt sådant.

### 2 · Pilot
Riktiga användare, ett avgränsat problem, ett uttalat slutdatum.

**Frågan den svarar på:** blir det bättre för dem som gör jobbet?

Det är här de flesta lösningar dör, och nästan aldrig av tekniska skäl. De dör för
att ingen mätte om det blev bättre, för att svaren var opålitliga på ett sätt som
användarna inte kunde bedöma, eller för att det tog mer tid att kontrollera resultatet
än att göra jobbet själv.

Krävs för att kalla något pilot:
- en namngiven ägare
- en definition av vad "fungerar" betyder, bestämd **innan** starten
- ett slutdatum
- klarhet i vilka data som får användas

### 3 · Produktion
Någon förlitar sig på det. Det är en förvaltningsfråga, inte ett projekt längre.

**Frågan den svarar på:** kan vi ta ansvar för det här över tid?

Se [50-fran-poc-till-produktion/checklista.md](../50-fran-poc-till-produktion/checklista.md).

## Vad som ändras mellan stegen

Det är inte funktionaliteten. Det är allt annat.

| | PoC | Pilot | Produktion |
|---|---|---|---|
| Användare | du | en avgränsad grupp | den som behöver den |
| Data | påhittad | verklig, begränsad | verklig |
| Fel | irriterande | måste kunna upptäckas | måste kunna åtgärdas |
| Kostnad | struntsummor | mätbar | budgeterad |
| Modellbyte | prova på | planerad omtest | regressionstestat |
| Åtkomst | din inloggning | uttalad avgränsning | integrerad behörighetsmodell |
| Om det ligger nere | inget händer | någon blir irriterad | någon blir blockerad |
| Ägare | den som byggde | namngiven person | förvaltningsorganisation |
| Dokumentation | en experimentfil | tillräckligt för att någon annan ska kunna köra det | tillräckligt för att någon annan ska kunna ta över |

## Samma funktion, olika mängd byggstenar

Det syns tydligast om man ritar upp vad lösningen faktiskt består av i vart och ett av
stegen.

![Tre kolumner med staplade komponenter. PoC består av modell och prompt, egna
dokument i kontexten och ett verktyg. Piloten lägger till loggning, kända fall att
mäta mot samt ägare och slutdatum. Produktion med känsliga uppgifter lägger dessutom
till behörighet per användare, filtrering och gallring, regressionstest vid
modellbyte samt översyn och förvaltning. Understa komponenten är densamma i alla
tre.](../bilder/krav-vaxer.svg)

Understa lådan är densamma överallt: modellen och prompten. Det är den som demon
visar, och den som tar minst tid. Allt som skiljer kolumnerna åt är sådant som inte
syns förrän någon annan än den som byggde ska använda lösningen — eller förrän någon
frågar varför den svarade som den gjorde.

**Känsliga uppgifter är det som ökar antalet komponenter mest.** Behörighet knuten
till användaren i stället för till en teknisk användare, filtrering av vad som får
skickas iväg, gallring, och en väg att eskalera när något går fel. Det är fyra
konstruktionsfrågor och inte en instruktion i en prompt — och de går inte att lägga
till på slutet utan att bygga om.

Vilka byggstenar som finns att välja på, och vad var och en löser, står i
[20-tekniker/byggstenar.md](../20-tekniker/byggstenar.md#när-modellen-inte-räcker).

## Fyra fällor

**Att kalla en PoC för pilot.** Piloter har användare och ägare. Utan det är det en
PoC med publik.

**Att hoppa över piloten.** Från "det funkade när jag testade" direkt till bred
utrullning. Frågan om det faktiskt blir bättre för användarna blir aldrig ställd.

**Att bygga för produktion i steg 1.** Behörighetsmodell och loggning innan man vet
om idén håller. Dyrt sätt att lära sig att den inte gjorde det.

**Att fastna i steg 1.** Tio PoC:ar, noll piloter. Ofta ett tecken på att ingen äger
frågan om vad som ska hända sedan — inte på att teknikerna var dåliga.

## Vad vi använder trappan till

Skriv steget överst i varje experiment- och användningsfallsdokument. En rad, men den
gör diskussionen konkret: "det här är en PoC, nästa steg är pilot, och för det saknar
vi en ägare" är ett användbart läge att befinna sig i. "Vi har byggt något med AI" är
det inte.

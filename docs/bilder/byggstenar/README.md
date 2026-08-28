# Byggstenar, en fil per låda

Lådorna ur [anatomi.svg](../anatomi.svg) och tabellen i
[20-tekniker/byggstenar.md](../../20-tekniker/byggstenar.md), utbrutna till var sin
fil. Tänkta att dras in i ett skissverktyg och läggas om i ett eget upplägg — inte
att refereras från dokumentationen. Där används den sammansatta figuren.

## Filerna

| Fil | Byggsten | Ruta |
|---|---|---|
| [anvandaren.svg](anvandaren.svg) | Användaren | vanlig |
| [applikationslagret.svg](applikationslagret.svg) | Applikationslagret | vanlig |
| [api-lagret.svg](api-lagret.svg) | API-lagret | vanlig |
| [orkestrering.svg](orkestrering.svg) | Orkestrering | vanlig |
| [modellen.svg](modellen.svg) | Modellen | bas |
| [kontext-och-minne.svg](kontext-och-minne.svg) | Kontext och minne | vanlig |
| [verktygslagret.svg](verktygslagret.svg) | Verktygslagret | vanlig |
| [arbetssatt.svg](arbetssatt.svg) | Arbetssätt | vanlig |
| [kallsystem-register-dokument.svg](kallsystem-register-dokument.svg) | Källsystem, register, dokument | vanlig |
| [sakerhet-och-behorighet.svg](sakerhet-och-behorighet.svg) | Säkerhet och behörighet | vanlig |
| [driftmiljon.svg](driftmiljon.svg) | Driftmiljön | markerad |
| [utvardering.svg](utvardering.svg) | Utvärdering | markerad |
| [mansklig-oversyn.svg](mansklig-oversyn.svg) | Mänsklig översyn | markerad |
| [livscykelhantering.svg](livscykelhantering.svg) | Livscykelhantering | markerad |

`png/` innehåller samma lådor renderade i dubbel upplösning, för verktyg som inte
tar SVG.

## Färgerna betyder något

Samma palett som resten av figurerna, se [../README.md](../README.md).

| Ruta | Fyllning | Kant | Vad den markerar |
|---|---|---|---|
| **vanlig** | `#f4f4f7` | `#d8d8de` | En byggsten bland andra |
| **bas** | `#1b1b6e` | `#1b1b6e` | Modellen — det som ligger underst |
| **markerad** | `#e8f0fa` | `#0b5fa5` | De fyra som saknas i nästan varje demo, och som avgör om något kan förvaltas |

Att driftmiljö, utvärdering, mänsklig översyn och livscykelhantering är markerade är
alltså inte dekoration — det är poängen i
[byggstenar.md](../../20-tekniker/byggstenar.md), och den överlever att lådorna flyttas
till ett annat verktyg.

## Så är de gjorda

Alla lådor är 302 × 66 px och byggda av en `<rect>` och två `<text>`. Till skillnad
från de sammansatta figurerna finns **inget `<style>`-block och inget mörkerläge** —
de ska kunna importeras utan att ett skissverktyg tappar färgerna. Vill du ha dem
mörka, byt fyllning och textfärg i verktyget.

Genererade av `verktyg/gen-byggstenar.py`. Ändra listan där och kör om, hellre än att
redigera en enskild fil — annars glider stilen isär.

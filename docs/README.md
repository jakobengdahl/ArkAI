# Dokumentationen

Katalogerna är numrerade för att hamna i läsordning, inte för att man måste läsa dem
i tur och ordning.

| | Katalog | Vad det är | Börja här om du... |
|---|---|---|---|
| 00 | [oversikt/](00-oversikt/) | Vision, ordlista, mognadstrappa | ...är ny |
| 10 | [anvandningsfall/](10-anvandningsfall/) | Vad vi gör och var AI kan hjälpa | ...har ett problem att lösa |
| 20 | [tekniker/](20-tekniker/) | En sida per AI-teknik | ...vill veta vad något är |
| 30 | [experiment/](30-experiment/) | Labbloggar med svar | ...vill veta om något provats |
| 40 | [matchning/](40-matchning/) | Vilken teknik till vilket problem | ...ska välja |
| 50 | [fran-poc-till-produktion/](50-fran-poc-till-produktion/) | Vad steget kräver | ...har något som fungerar |
| 60 | [miljo/](60-miljo/) | Labbmiljön, verktygen, autentisering | ...ska sätta upp något |

Utanför `docs/`:

- [minnesbank/](../minnesbank/) — det delade minnet, både verktyg och experiment
- [exempel/](../exempel/) — körbar kod
- [verktyg/](../verktyg/) — skript för labbmiljön

## Var lägger jag det jag skrivit?

| Det du har | Där det hör hemma |
|---|---|
| Ett problem från verksamheten | `10-anvandningsfall/` |
| Något du testat och vet svaret på | `30-experiment/` |
| En beskrivning av en teknik | `20-tekniker/` |
| Något nästa person behöver veta *innan* de börjar | [`minnesbank/`](../minnesbank/) |
| Hur du fick något att funka i miljön | `60-miljo/` + en minnespost |

Den fjärde raden är den som glöms. Ett experiment är en berättelse om vad som hände;
en minnespost är en instruktion till framtiden. Bara den ena överlever.

## Läsordning för en ny kollega

1. [00-oversikt/vision-och-mal.md](00-oversikt/vision-och-mal.md) — vad vi försöker
2. [RIKTLINJER-INNEHALL.md](../RIKTLINJER-INNEHALL.md) — repot är publikt
3. [60-miljo/sspcloud-onyxia.md](60-miljo/sspcloud-onyxia.md) — miljön
4. [minnesbank/README.md](../minnesbank/README.md) — hur vi delar det vi lär oss
5. [30-experiment/](30-experiment/) — vad som redan gjorts

Sedan: ta något från "På tur" i experimentlistan.

# Bilder

Figurerna som används i dokumentationen. En fil per figur, SVG, incheckad som text.

| Fil | Vad den visar | Används i |
|---|---|---|
| [anatomi.svg](anatomi.svg) | Var byggstenarna sitter i en lösning | [20-tekniker/byggstenar.md](../20-tekniker/byggstenar.md) |
| [pabyggnad.svg](pabyggnad.svg) | Lagren ovanpå modellen, och vad varje lager svarar mot | [20-tekniker/byggstenar.md](../20-tekniker/byggstenar.md) |
| [nivastegen.svg](nivastegen.svg) | Nivåstegen, och vad som tillkommer på varje steg | [20-tekniker/byggstenar.md](../20-tekniker/byggstenar.md) |
| [krav-vaxer.svg](krav-vaxer.svg) | Samma funktion som PoC, pilot och produktion | [00-oversikt/mognadstrappa.md](../00-oversikt/mognadstrappa.md) |
| [verktygsanrop.svg](verktygsanrop.svg) | Ett verktygsanrop steg för steg | [20-tekniker/chattbot-plus-verktyg.md](../20-tekniker/chattbot-plus-verktyg.md) |
| [tre-minnena.svg](tre-minnena.svg) | Hämtning, minnesbank och graf — vilken fråga var och en svarar på | [20-tekniker/README.md](../20-tekniker/README.md) |

## Regler

**Bilden får inte bära information som inte står i texten.** Den ska göra ett
resonemang snabbare att ta till sig, inte ersätta det. Utgå från att någon läser
sidan med uppläsning, i en terminal eller i en diff.

**Alt-texten ska beskriva innehållet, inte figuren.** Skriv vad som står i den, inte
"översiktsbild". Det är den texten som är figuren för den som inte ser den.

**SVG, inte PNG.** Diff:bar, skalar, väger några kilobyte. Skärmdumpar hör inte
hemma här — se [RIKTLINJER-INNEHALL.md](../../RIKTLINJER-INNEHALL.md). Figurerna här
är konstruerade, inte hämtade ur ett riktigt system.

**Svenska i figuren**, samma termer som i texten runt omkring. Se
[ordlistan](../00-oversikt/ordlista.md).

## Så är de gjorda

Ljust läge ligger i presentationsattribut (`fill="#f4f4f7"`) på varje element.
`<style>`-blocket innehåller **bara** mörkerlägets avvikelser, bakom
`@media (prefers-color-scheme:dark)`.

Ordningen är medveten. En renderare som inte kör CSS — eller som blockerar den, vilket
[labbpanelen](../60-miljo/panelen.md) gör när den serverar bilder i sandlåda — visar då
den ljusa versionen korrekt i stället för svarta rutor. Motsatt upplägg, med
CSS-variabler för färgerna, ger en helt svart bild i samma läge. Det är prövat.

Inga skript, inga externa typsnitt, inga länkade resurser. Referera dem som vanlig
markdown:

```markdown
![Beskrivning av vad figuren visar](../bilder/namn.svg)
```

Panelen skriver om `src` till sin egen routing automatiskt, så samma rad fungerar
både på GitHub och i panelen.

## Palett

| Roll | Ljust | Mörkt |
|---|---|---|
| Kortets botten | `#ffffff` | `#202024` |
| Ruta | `#f4f4f7` | `#2a2a31` |
| Kant | `#d8d8de` | `#3d3d46` |
| Text | `#1a1a1a` | `#e9e9ee` |
| Svag text | `#5f5f6a` | `#a3a3ae` |
| Bas — modellen, det som ligger underst | `#1b1b6e` | `#6f6fd8` |
| Markerad ruta — det som brukar saknas | `#e8f0fa` / `#0b5fa5` | `#22303f` / `#6cb6ff` |

Håll dig till den. Färgerna betyder något: mörkblått är alltid modellen eller det som
är gemensamt mellan alternativen, blåmarkerat är alltid det som tillkommer.

# Bidra

## Innan du börjar

Läs [RIKTLINJER-INNEHALL.md](RIKTLINJER-INNEHALL.md). Repot är publikt.

## Arbetsflöde

Vi jobbar med korta grenar och pull requests — inte för formalitetens skull, utan för
att en PR är den naturliga platsen att diskutera *vad vi lärde oss*.

```bash
git switch -c exp/kort-beskrivning
# ... jobba ...
./verktyg/kontrollera-innehall.sh
git add -A && git commit -m "Experiment: kort beskrivning"
git push -u origin exp/kort-beskrivning
gh pr create --fill
```

Merge till `main` när någon annan läst igenom. För rena dokumenttillägg räcker det
att du själv läst igenom det en gång till med "publikt repo"-glasögonen på.

### Grennamn

| Prefix | Används för |
|---|---|
| `exp/` | Ett experiment (docs/30-experiment/) |
| `uc/` | Ett användningsfall (docs/10-anvandningsfall/) |
| `tek/` | En teknikbeskrivning (docs/20-tekniker/) |
| `minne/` | Ändring i den delade minnesbanken |
| `miljo/` | Skript, verktyg, labbmiljö |

## Vad ska en ny fil heta?

- Användningsfall: `docs/10-anvandningsfall/UF-007-kort-namn.md`
- Experiment: `docs/30-experiment/EXP-012-kort-namn.md`
- Teknik: `docs/20-tekniker/kort-namn.md` (ingen numrering — tekniker är inte en sekvens)
- Minnespost: `minnesbank/<kategori>/kort-namn.md`

Löpnumren är bara för att kunna hänvisa till något i en diskussion. Återanvänd inte
ett nummer även om filen tas bort.

## Mallar

Varje katalog har en `MALL-*.md`. Kopiera den. Mallarna är korta med flit — fyll i
det som är sant, stryk resten. Ett halvfärdigt dokument som finns är bättre än ett
komplett som inte skrivs.

## Skriv så här

- Svenska. Engelska facktermer är okej när de är etablerade (embedding, prompt,
  context window) — se [ordlistan](docs/00-oversikt/ordlista.md).
- Skriv ut vad du faktiskt körde och vad som faktiskt hände. Versionsnummer,
  modellnamn, ungefärlig tidsåtgång.
- Skriv slutsatsen först. Detaljerna under.
- Redovisa det som inte funkade. Det är ofta den mest värdefulla delen.

## När ett experiment är klart

Uppdatera två saker utöver själva experimentfilen:

1. [docs/40-matchning/matris.md](docs/40-matchning/matris.md) — om du lärde dig något
   om vilken teknik som passar vilket användningsfall.
2. [minnesbank/](minnesbank/) — om du lärde dig något som nästa person behöver veta
   *innan* de börjar.

Punkt 2 är hela poängen med repot. Ett experiment vars lärdom stannar i
experimentfilen kommer att göras om av någon annan om ett halvår.

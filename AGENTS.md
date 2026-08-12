# Instruktioner för AI-agenter i det här repot

Den här filen läses av AI-verktyg som arbetar i repot (Claude Code, opencode,
Continue m.fl.). Den är också läsvärd för människor — konventionerna är desamma.

Att filen finns är i sig ett experiment: hur mycket styr skrivna konventioner
faktiskt en agents beteende? Se
[docs/20-tekniker/kodagenter.md](docs/20-tekniker/kodagenter.md).

## Det viktigaste först

**Repot är publikt på GitHub.** Skriv aldrig in verksamhetsinterna detaljer, namn på
personer eller system, riktiga data, nycklar eller interna adresser. Läs
[RIKTLINJER-INNEHALL.md](RIKTLINJER-INNEHALL.md).

Om du behöver konkreta detaljer för att resonera: lägg dem i `lokalt/` (gitignorerad)
och lyft bara ut den generella lärdomen.

**Klistra inte in miljövariabler eller konfigurationsfiler.** `env`,
`~/.continue/config.yaml`, `~/.config/opencode/opencode.jsonc` och `.git/config`
innehåller alla fungerande tokens i den här miljön. Se
[minnesbanken](minnesbank/verktyg/api-nycklar-i-hemkatalogen.md).

## Läs minnesbanken först

[`minnesbank/MINNE.md`](minnesbank/MINNE.md) är ett index över vad vi redan lärt oss
om den här miljön. Läs **indexet** i början av en session och hämta enskilda poster
när de är relevanta.

Lägg inte hela minnesbanken i kontexten. Det är sämre, inte bättre — se
[index före innehåll](minnesbank/arbetssatt/index-fore-innehall.md).

## Språk

Svenska i all dokumentation. Etablerade engelska facktermer behålls (prompt, embedding,
context window, token) — se [ordlistan](docs/00-oversikt/ordlista.md).

Kod, filnamn och kommandon på svenska där det är naturligt; följ det som redan finns.

## Struktur

| Katalog | Innehåll | Mall |
|---|---|---|
| `docs/10-anvandningsfall/` | `UF-NNN-namn.md` | `MALL-anvandningsfall.md` |
| `docs/20-tekniker/` | `namn.md`, ingen numrering | `MALL-teknik.md` |
| `docs/30-experiment/` | `EXP-NNN-namn.md` | `MALL-experiment.md` |
| `minnesbank/` | en post per fil, i rätt kategori | `MALL-minnespost.md` |

Använd mallarna. Uppdatera indexet (`MINNE.md`, README-tabellerna) när du lägger till
en fil — en fil som inte står i indexet hittas inte.

## Skrivsätt

- **Slutsatsen först.** Läsaren ska kunna sluta efter första stycket.
- **Skriv vad som faktiskt hände**, med versionsnummer och felmeddelanden. Inte vad
  som borde hända.
- **Redovisa det som inte fungerade.** Egen rubrik i experimentmallen, med flit.
- Inga superlativ. Inga påståenden om vad tekniken "kommer att" göra.
- Skriv inte in i tabellen "Vad vi har provat" något vi inte provat.

## När du är klar med något

1. Uppdatera experiment- eller dokumentfilen
2. Uppdatera relevanta index och tabeller
3. Skriv en **minnespost** om lärdomen är något nästa person behöver veta *innan* de
   börjar

Punkt 3 glöms nästan alltid. Ett experiment är en berättelse om vad som hände; en
minnespost är en instruktion till framtiden. Bara den ena överlever.

## Innan commit

```bash
./verktyg/kontrollera-innehall.sh
```

Skapa en gren (`exp/`, `uc/`, `tek/`, `minne/`, `miljo/`) och en PR — commita inte
direkt på `main`. Se [BIDRA.md](BIDRA.md).

## Miljön

Onyxia/SSP Cloud, Kubernetes-baserad. Kort om det som brukar överraska:

- **Port 8080 är upptagen** av code-server. Använd 8081+.
- **Behörigheter sätts när tjänsten startar** och går inte att ändra i efterhand.
  Går något inte — kontrollera hur tjänsten startades innan du letar teknisk lösning.
- **`apt`-installationer försvinner** vid omstart. `~/.local` och `~/work` är kvar.
- **Kör inte `./verktyg/starta-openwebui.sh` utan att fråga** — den startar en
  långkörande process.

Detaljer: [docs/60-miljo/](docs/60-miljo/).

## Vad du inte ska göra utan att fråga

- Pusha till `main`
- Ta bort minnesposter (föreslå det i stället — en post kan vara någon annans slutsats)
- Starta eller stoppa tjänster som andra kan använda
- Installera saker globalt med `sudo`
- Ändra `.gitignore` så att fler filtyper släpps igenom

# Instruktioner för AI-agenter i det här repot

Den här filen läses av AI-verktyg som arbetar i repot (Claude Code, opencode,
Continue m.fl.). Den är också läsvärd för människor — konventionerna är desamma.

Att filen finns är i sig ett experiment: hur mycket styr skrivna konventioner
faktiskt en agents beteende? Se
[docs/20-tekniker/kodagenter.md](docs/20-tekniker/kodagenter.md).

## Det viktigaste först

**Repot är publikt på GitHub.** Skriv aldrig in namn på personer eller interna system,
riktiga data, nycklar eller interna adresser. Läs
[RIKTLINJER-INNEHALL.md](RIKTLINJER-INNEHALL.md).

Om du behöver konkreta detaljer för att resonera: lägg dem i `lokalt/` (gitignorerad)
och lyft bara ut den generella lärdomen.

## Verksamheten du skriver för

Läsarna arbetar i en offentlig myndighet med statistikproduktion. Arbetet består av
insamling, bearbetning och analys av data som blir faktabaserat beslutsunderlag för
samhället, för forskare och för andra myndigheter. Processerna följer i stora drag
**GSBPM** (Generic Statistical Business Process Model), och verksamheten är starkt
metadatadriven: klassifikationer, variabeldefinitioner, register och
kvalitetsdeklarationer är arbetsmaterial, inte administration.

Det påverkar hur du ska resonera:

- **Spårbarhet väger tyngre än effektivitet.** Ett svar som inte går att härleda är
  sällan användbart här, oavsett hur snabbt det kom.
- **Kvalitet är definierad, inte upplevd.** Det finns etablerade ramverk för vad
  kvalitet betyder. Skriv inte "bättre" utan att säga i vilken dimension.
- **Strukturerad metadata finns redan.** Föreslå inte att bygga upp kunskap från
  fritext när det finns en modell — se [metadatagrafen](docs/60-miljo/metadatagrafen.md).
- **Långa förvaltningshorisonter.** "Det fungerar" är inte samma sak som "det går att
  förvalta i tio år". Det är hela poängen med
  [50-fran-poc-till-produktion/](docs/50-fran-poc-till-produktion/).

Att beskriva den här sortens arbete öppet är tillåtet och önskvärt — det är det som
gör användningsfallen bedömbara. Det som inte hör hemma här är enskilda system,
personer, avtal, riktiga data och allt som rör kärnverksamhetens skarpa drift.
Ingenting vi gör i labbet rör den.

**Interna styrdokument refereras generellt, aldrig ordagrant.** Policyer, riktlinjer,
mallar och beslutsunderlag som inte är publicerade utanför organisationen ska
beskrivas som mönster — "en bedömning brukar fråga efter informationsklass" — inte
citeras, återges strukturmässigt eller läggas in som filer. Se
[docs/00-oversikt/forutsattningar.md](docs/00-oversikt/forutsattningar.md) för
tonläget. Dokumentfiler (`.pdf`, `.docx`, `.pptx`) är gitignorerade med flit.

## Två spår — kontrollera vilket du skriver i

Vi arbetar dels med sådant vi själva ansvarar för, dels med utblickar mot verksamhet
andra ansvarar för. Skillnaden styr vad ett dokument får landa i:

- **Eget spår** — får resonera hela vägen till pilot och produktion.
- **Utforskande spår** — resultatet är kunskap och ett underlag, aldrig ett förslag
  om vad någon annan bör göra. Föreslå inte införande, utrullning eller nästa steg i
  någon annans verksamhet. Formulera observationer.

Står det **Spår: Utforskande** överst i en fil, skriv därefter. Se
[docs/00-oversikt/vision-och-mal.md](docs/00-oversikt/vision-och-mal.md#två-spår).

Varje användningsfall inleds dessutom med ett
[typfall](docs/10-anvandningsfall/typfall.md) (A–F). Det avgör vad som krävs i
utvärdering, mänsklig översyn och styrning — sätt det innan du resonerar om teknik.

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
| `docs/bilder/` | `namn.svg`, en fil per figur | [`docs/bilder/README.md`](docs/bilder/README.md) |
| `minnesbank/` | en post per fil, i rätt kategori | `MALL-minnespost.md` |

Använd mallarna. Uppdatera indexet (`MINNE.md`, README-tabellerna) när du lägger till
en fil — en fil som inte står i indexet hittas inte.

Figurer: SVG, svenska, alt-text som beskriver innehållet, och **ingen information i
bilden som inte står i texten**. Färger och uppbyggnad står i
[`docs/bilder/README.md`](docs/bilder/README.md) — läs den innan du ritar en ny.

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
- **`apt`-installationer försvinner** vid omstart. `~/.local` och `~/work` är kvar,
  så installera i hemkatalogen och undvik `sudo`.
- **Starta inte långkörande tjänster utan att fråga.**

Detaljer: [docs/60-miljo/](docs/60-miljo/).

### Kör saker via manifestet, inte ad hoc

Allt som går att installera eller starta står i
[`verktyg/labb.toml`](verktyg/labb.toml). Använd det:

```bash
verktyg/kor.sh status                        # vad är installerat, vad kör
verktyg/kor.sh installera <tjänst>
verktyg/kor.sh starta <tjänst>
verktyg/kor.sh uppsattning <namn>
```

`kor.sh` tar ett lås per tjänst, loggar till `~/work/.labb/logg/` och skriver status
som [labbpanelen](docs/60-miljo/panelen.md) läser. Startar du samma sak för hand vid
sidan av vet panelen inget om det, och två installationer kan trampa på varandra.

Behöver något nytt kunna startas: lägg till det i `labb.toml` och skriv ett
`verktyg/installera/<namn>.sh`. Skriv inte in det i panelen — den har med flit ingen
kunskap om enskilda tjänster.

## Vad du inte ska göra utan att fråga

- Pusha till `main`
- Ta bort minnesposter (föreslå det i stället — en post kan vara någon annans slutsats)
- Starta eller stoppa tjänster som andra kan använda
- Installera saker globalt med `sudo`
- Ändra `.gitignore` så att fler filtyper släpps igenom

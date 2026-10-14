# Egen graf

En egen instans av grafappen, [CommunityOverview](https://github.com/jakobengdahl/CommunityOverview),
med ett schema du själv bestämmer över. Det är samma app som
[metadatagrafen](metadatagrafen.md) kör på. Skillnaden är att metadatagrafen är en
pilot som andra driver och som vi bara kopplar upp oss mot, medan den här är din: du
kan ändra nodtyper, lägga in egna objekt och ta bort alltihop utan att piloten märker
något.

## Kort svar

Appen kör **här i VS Code-podden, från källkod**, på samma commit som prod-imagen
byggdes från. Allt ligger under `~/work` och överlever en omstart av podden:

| Katalog | Innehåll |
|---|---|
| `~/work/graf-config/` | schemat. Redigeras i VS Code |
| `~/work/graf-data/` | grafen: `graph.json` med journal och historik, och `arkiv/` |
| `~/work/.labb/graf/` | källkod, Python-miljö, byggd frontend |

```bash
verktyg/kor.sh installera graf       # källkod, Python, frontend, schema (~5 min första gången)
verktyg/kor.sh starta graf           # startar appen på port 8085
verktyg/kor.sh koppla_eneo graf      # lägger upp grafen som MCP-server i Eneo
verktyg/kor.sh stoppa graf           # stoppar appen — grafen ligger kvar
verktyg/kor.sh avinstallera graf     # tar bort allt utom schemat
verktyg/seeda-graf.sh <fil>          # ersätter grafen med en lokal fil
```

Samma knappar finns på kortet *Egen graf* i panelen. Du kan också starta miljön med
[länken med Eneo och egen graf](starta-labbet.md#urlen), alltså profilen
`bas eneo graf`. Då installeras, startas och kopplas grafen in utan att du behöver
göra något mer.

## Schemat

```
~/work/graf-config/
  schema_config.json      nodtyper, relationer, färger, prompter — krävs
  federation_config.json  federering mot andra grafer — valfri
  graph.json              startdata — används bara när grafen saknas
  LAS-MIG.md
```

Första installationen fyller katalogen med en profil. Standardprofilen är `arkai`,
som ligger i repot under
[`verktyg/graf/profiler/arkai/`](../../verktyg/graf/profiler/arkai/). Vill du utgå
från en annan väljer du den vid första installationen:

```bash
GRAF_PROFIL=stat-metadata verktyg/kor.sh installera graf
```

Övriga profiler kommer ur källkoden. I den pinnade versionen är det `default`,
`stat-metadata`, `scb` och `test`. En profil i repot går före källkodens profil
med samma namn, och det som profilen saknar (här `federation_config.json`) tas ur
`default`. Filer som redan finns i katalogen skrivs aldrig över, så en graf som
redan är installerad får inte de nya typerna av sig själv — se nedan.

### Profilen `arkai`

`arkai` är källkodens `default` på den pinnade commiten, med fler nodtyper. Den har
ingen startdata, så grafen börjar tom.

| Nodtyp | På svenska | Ikon | Anmärkning |
|---|---|---|---|
| Actor | Aktör | `PersonFill` | Kunder och partner är aktörer med subtypen `Customer` eller `Partner` |
| Initiative, Capability, Resource, Legislation, Theme, Goal, Event, Risk | | | Oförändrade från `default` |
| Information | Information | `DatabaseFill` | Ersätter `Data`. Subtyper: `Dataset`, `Hållpunkt`, `Informationsobjekt` (det som rör sig mellan processer) |
| Process | Process | `GearWideConnected` | |
| Task | Uppgift | `KanbanFill` | Fälten `status` och `due_date` |
| Principle | Princip | `CompassFill` | |
| ValueProposition | Värdeerbjudande | `StarFill` | |
| Effect | Effekt | `GraphUpArrow` | |
| Decision | Beslut | `ClipboardCheckFill` | Fältet `decided_date` |
| Component | Komponent | `MotherboardFill` | Fältet `identifier` för t.ex. repo-URL |
| Feature | Funktion | `PuzzleFill` | |
| Cost | Kostnad | `PieChartFill` | Registret har ingen ikon för pengar |
| Metric | Mått | `BarChartFill` | Fälten `unit`, `target_value` och `current_value` |
| Requirement | Krav | `CardChecklist` | Fältet `status` |
| Concept | Begrepp | `LightbulbFill` | |
| Channel | Kanal | `MegaphoneFill` | |

Ikonerna går bara att välja bland dem som finns i appens `ICON_REGISTRY`. Listan
står i `docs/ICONS.md` i CommunityOverview, och ingen ikon används av två typer.
Subtyper är fri text i appen, inte en lista i schemat. De föreslagna subtyperna
står därför i typens beskrivning, som assistenten läser.

Relationerna är desamma som i `default`, med två ändringar: `PRODUCES` pekar på
`Information` i stället för `Data`, och en `Process` kan också vara källa. Övriga
kopplingar mellan de nya typerna görs med `RELATES_TO` och `PART_OF`, som inte är
begränsade.

**Vill du ha de nya typerna i en graf som redan är installerad:** kopiera filen och
starta om grafen. Den gamla schemafilen skrivs då över. Noder av typen `Data` får
du byta till `Information` själv.

```bash
cp verktyg/graf/profiler/arkai/schema_config.json ~/work/graf-config/
verktyg/starta-graf.sh --starta-om
``` Formatet beskrivs i
`docs/PROFILES.md` i CommunityOverview.

**Ändrat schemat?** Appen läser schemat när den startar, så det räcker att starta
om den. Det gör du med *Stoppa* och sedan *Starta* i panelen, med tasken **Grafen:
starta om (läs in schemat)** i VS Code, eller med `verktyg/starta-graf.sh --starta-om`.
Är JSON-filen trasig vägrar appen starta och säger vilken fil det gäller.

Katalogen ligger under `~/work` och inte i repot. Det är med flit: repot är publikt,
och ett eget schema kan innehålla sådant som inte hör hemma där. Vill du dela ett
schema öppet, lägg en avidentifierad kopia under `exempel/`.

## Startdata och seedning

Det finns två sätt att få in en `graph.json`. De skiljer sig i när de verkar.

**Startdata i `~/work/graf-config/graph.json`** kopieras till `~/work/graf-data/`
bara när grafen saknas där. Det sker vid första starten, eller efter *Ta bort*. En
omstart eller ominstallation skriver aldrig över det som byggts upp i grafen.

**Seeda från en lokal fil** ersätter grafen som den ser ut nu, med valfri fil:

- I VS Code: öppna filen, `Ctrl+Shift+P` → *Tasks: Run Task* → **Grafen: seeda från
  öppen fil**.
- I terminalen: `verktyg/seeda-graf.sh <fil>`

Skriptet kontrollerar att filen är en graf (ett objekt med listorna `nodes` och
`edges`), visar storleken på både den nya och den nuvarande grafen och frågar innan
något ändras. Kör appen stoppas den först och startas igen efteråt. Den gamla grafen
flyttas till `~/work/graf-data/arkiv/<tid>/` tillsammans med sina sidofiler:
journalen, historiken och embeddings (`graph.*`). Journalen måste flyttas med. Blir
den kvar spelas den upp ovanpå den nya grafen.

## Koppla in i Eneo

Eneo kör i en annan podd och når grafen genom Servicen `arkai-graf`, som pekar på
den här podden: `http://arkai-graf:8000/mcp/` → port 8085 här. Nätverkspolicyn för
VS Code-tjänsten släpper in trafik från alla poddar i namnrymden. Servicens selector
sätts om vid varje start, eftersom en ny VS Code-tjänst får ett nytt instansnamn.
Går den interna adressen inte provar kopplingen ingressen för port 8085 i stället.

Båda vägarna kräver en token. Den skapas vid första installationen, ligger i
`~/work/.labb/graf-token` och lämnas till Eneo när grafen kopplas in.

## Version

| | |
|---|---|
| Källkod | commit `021685b` i CommunityOverview, den som prod-imagen (taggen `latest`) byggdes från 2026-09-16 |
| Python | 3.11, som i imagen. Beroendena är inte låsta i CommunityOverview, så de löses som de såg ut när imagen byggdes (`uv pip install --exclude-newer 2026-09-16`) |
| ML | torch och sentence-transformers för CPU, som i imagen. `GRAF_ML=nej` hoppar över dem, och då fungerar semantisk sökning bara på förberäknade embeddings |

För att byta version sätter du `GRAF_COMMIT` (och gärna `GRAF_BYGGD`) och
installerar om. Commiten bakom en image står i imagens etikett
`org.opencontainers.image.revision`.

## Det som inte fungerade: egen arbetslast i namnrymden

Första versionen körde appen som Eneo gör, som en egen arbetslast i namnrymden med
prod-imagen och en egen volym. Den föll 2026-10-13 på att klustret inte skapade
volymen. PVC:n stod i `Pending` med *"Waiting for a volume to be created either by
the external provisioner 'rook-ceph.rbd.csi.ceph.com'…"*. En tom provvolym på 1 Gi
fastnade på samma sätt, trots samma lagringsklass och storlek som de bundna volymerna
i namnrymden, och trots att kvoten inte var nådd (130 Gi av 2 Ti). Klustrets
lagringsklasser och provisionerare går inte att se med rollen `edit`.

Att köra i podden kräver ingen ny volym, för `~/work` är redan en. Det har också
fördelar i sig: grafen och dess arkiv syns i VS Code, seedning är en filkopiering,
och ingenting blir kvar och tar kvot i namnrymden när tjänsten stoppas. Priset är att
grafen bara kör så länge VS Code-tjänsten gör det.

## Det som skiljer den från piloten

Namnrymden delas med flera CommunityOverview-instanser som andra driver. De heter
`communityoverview-*`, och metadatagrafens pilot är en av dem. Det enda vi lägger i
namnrymden är Servicen `arkai-graf`, med etiketten
`app.kubernetes.io/part-of=arkai-graf`. *Ta bort* väljer bara på den etiketten.

Se [minnesbanken](../../minnesbank/verktyg/namnrymden-delas-med-andras-grafer.md).

## Inloggning

Port 8085 är ett publikt värdnamn om den exponerades när tjänsten startade.
Webbgränssnittet kräver inloggning med `arkai@arkai.se` som både användarnamn och
lösenord, samma som Eneo. MCP kräver token.
Lösenordet står i repot med flit, precis som Eneos, eftersom labbet har en användare.
Grafens inbyggda assistent använder din LLM-nyckel, så den som kan lösenordet kan
använda nyckeln. Sätt `GRAF_ANVANDARE` och `GRAF_LOSEN` före starten om du vill ha
något annat.

# Eneo som alternativ till Open WebUI

[Eneo](https://www.eneo.ai) är en öppen AI-plattform byggd av Sundsvalls och Ånge
kommun för svensk offentlig sektor. Den gör i grunden samma sak som Open WebUI —
chattgränssnitt mot språkmodeller — men med sådant som Open WebUI saknar:
behörighetsmodell per organisation, revisionslogg, OIDC-federation, SCIM. Det gör den
intressant för oss, för det är precis den sortens frågor som skiljer en PoC från
något som får köras i drift. Se [50-fran-poc-till-produktion](../50-fran-poc-till-produktion/).

Det här dokumentet är **en plan, inte en installationsanvisning**. Installationen är
inte gjord. Miljön som beskrivs i [starta-labbet.md](starta-labbet.md) klarar den inte
— den måste startas med andra inställningar, och de går inte att ändra i efterhand.

Underlaget är mätt i labbmiljön 2026-08-28 mot Eneo v2.1.1.

## Kort svar

Det går, men inte på den väg Eneo själva dokumenterar. Deras enda beskrivna
installation är `docker compose`, och **det finns ingen containerruntime i
labbtjänsten**. Tre saker måste ändras, alla vid tjänstestart:
Kubernetes-rollen, diskstorleken och en extra exponerad port.

Räkna med en dags arbete, inte en eftermiddag.

## Vad Eneo kräver

Fem tjänster, enligt [deployment-guiden](https://docs.eneo.ai/guides/deployment):

| Tjänst | Teknik | Port | Roll |
|---|---|---|---|
| Frontend | SvelteKit | 3000 | Webbgränssnitt, SSR |
| Backend | FastAPI | 8000 | API, autentisering |
| Worker | ARQ | — | Dokumentindexering, bakgrundsjobb |
| Databas | PostgreSQL 16 + **pgvector** | 5432 | Data och vektorsökning |
| Cache/kö | Redis 7 | 6379 | Cache, jobbkö |

Rekommenderat: 4+ kärnor, 8 GB+ RAM, **50 GB disk** (minimum 20 GB).

En reverse proxy ska terminera TLS och dela trafiken på **samma origin**:
`/*` till frontend, och `/api/*`, `/docs`, `/openapi.json`, `/version` till backend.
WebSocket måste gå igenom — Eneo använder både WebSocket och SSE för
strömmande svar. `PUBLIC_ORIGIN` sätts till den externa URL:en, och `JWT_SECRET`
måste vara **identisk** i frontend och backend.

Projektet är i gott skick: AGPL-3.0, v2.1.1 släppt 2026-08-26, aktiv utveckling.
Imagerna på `ghcr.io/eneo-ai/` är publika — taggarna går att lista utan inloggning.
**Det finns inget Helm-chart och inga Kubernetes-manifest i repot.**

### Dokumentationen ligger efter koden

Getting-started säger `pnpm 8.9.0` och `Python ≥ 3.10`. Koden på `develop` säger
något annat: `frontend/package.json` har `"packageManager": "bun@1.3.14"`, och
`backend/pyproject.toml` har `requires-python = ">=3.11,<3.12"`. Ska något byggas
från källkod är det **bun och Python 3.11** som gäller. Läs `Taskfile.yml` i repot
före guiden.

## Vad labbmiljön ger

Uppmätt i en `vscode-python`-tjänst startad på standardsättet:

| | Läge |
|---|---|
| **Docker / podman / nerdctl** | **saknas helt** — `docker: command not found` |
| Kubernetes | `kubectl` och `helm` finns, men rollen är `view`: `kubectl auth can-i create deployments` → `no` |
| CPU / RAM | 15 kärnor, 50 GiB enligt cgroup — gott om marginal |
| **Disk** | `/home/onyxia/work` är **9,8 GB, varav 2,8 GB ledigt** |
| sudo | fungerar utan lösenord |
| Paket | pgdg-repot är förinlagt: `postgresql-16` och `postgresql-16-pgvector` 0.8.6 finns, liksom `redis-server` 7.0.15 |
| Toolchain | uv 0.12.5, Node 24, npm 11. **Ingen bun, ingen pnpm** |
| Utgående nät | pypi, npm, ghcr.io, github, ubuntu — allt öppet |
| Namnrymdskvot | 14/100 poddar, 93 Gi av 2 Ti lagring |

### Tre hinder

**Ingen containerruntime.** Hela den dokumenterade installationen är otillgänglig.
Antingen bygger man från källkod i podden, eller så deployar man imagerna i
Kubernetes.

**Disken.** 2,8 GB ledigt mot Eneos 20 GB minimum. Backendens venv, frontendens
`node_modules` och en pgdata får inte plats. 7,0 GB av de 9,8 går just nu till
`~/work/.cache` (uv) — `uv cache prune` friar en del, men storleken måste ändå upp.
Standardvärdet `persistence.size` är `10Gi`.

**En origin, två portar.** Onyxia ger varje exponerad port ett *eget* värdnamn.
Eneo vill ha frontend och backend på samma origin — sessionscookies och delad
`JWT_SECRET`. Två värdnamn ger cross-origin-cookies och trasig inloggning. Det
behövs alltså en liten Caddy eller nginx i podden som lyssnar på den exponerade
porten och delar trafiken på sökväg. Det är inte svårt, men det är en bit som inte
finns i Eneos anvisningar och som gäller **oavsett** vilken väg man väljer.

## Vägval

**A. Kubernetes-deploy med de färdiga imagerna.** Starta tjänsten med
`kubernetes.role=edit` — se [sspcloud-onyxia.md](sspcloud-onyxia.md#kubernetes-roll).
Deploya backend, frontend och worker från `ghcr.io/eneo-ai/` som egna manifest, och
ta databasen från katalogen: `postgresql-cnpg` har en `extension.pgvector`-flagga.
Mest produktionslikt, och det enda som ger riktig persistens. Priset: manifesten
måste skrivas för hand från compose-filen, och **Redis finns inte i
Onyxia-katalogen** — den får bli ett eget manifest med `redis:7-alpine`.

**B. Från källkod i podden**, som vi gör med Open WebUI. uv klarar Python 3.11 och
backend; bun installeras under `~/.local` och överlever omstart; postgres+pgvector
och redis från apt med datakatalogen i `~/work`. Passar labbets befintliga mönster
och kräver ingen ändrad Kubernetes-roll — men det blir **fem processer i en podd som
är förgänglig**, och `apt`-delen måste installeras om vid varje omstart.
Uppgraderingar blir manuella.

**C. Vänta på ett Helm-chart.** Eneo vänder sig till svensk offentlig sektor, som kör
mycket Kubernetes, så frågan lär inte vara främmande för dem. Men det är ingen väg
framåt den här månaden.

### Rekommendation: A

Motivet att välja A framför B är inte teknisk elegans. Eneo är inte ett verktyg man
provar en kvart — det är en plattform man jämför med Open WebUI över tid. Fem
processer som dör vid varje podomstart gör den jämförelsen ojämn på fel sätt: Open
WebUI är en enda process och kommer alltid att verka enklare än den är. Kör man Eneo
som riktiga tjänster i namnrymden jämför man plattformarna, inte installationsbesväret.

Även i väg A går trafiken in genom den exponerade porten på VS Code-podden, med
Caddy där som pekar på Eneos ClusterIP-tjänster. Det slipper gissningar om
ingress-värdnamn och certifikat, och återanvänder mekanismen labbet redan kan.

## Inställningar för den nya miljön

Ingen av dem går att ändra i efterhand.

| Parameter | Värde | Varför |
|---|---|---|
| `kubernetes.role` | `edit` | Annars går det inte att deploya. Standard är `view` |
| `persistence.size` | `50Gi` | Standard är `10Gi`. Eneo vill ha 20 GB minimum, 50 GB rekommenderat |
| `networking.user.enabled` | `true` | Krävs för att exponera portar alls |
| `networking.user.ports[0]` | `8081` | Open WebUI — behålls, det är den vi jämför mot |
| `networking.user.ports[1]` | `8084` | Eneo, via Caddy i podden |
| `resources.limits.memory` | `16Gi` | Räcker gott. Klustrets tak är 50 GiB |
| `resources.requests.memory` | `4Gi` | Så att podden faktiskt schemaläggs med marginal |
| `init.personalInit` | startskriptet i repot | Panelen och grundmiljön |
| `init.personalInitArgs` | `bas` | Open WebUI installeras från panelen när den behövs |
| `git.repository` | `https://github.com/jakobengdahl/ArkAI.git` | Klonas till `~/work/ArkAI` |
| `git.branch` | `main` | Utan detta klonas standardgrenen. Planen och skripten ligger i `main` |
| `vault.secret` | `arkai-hemligheter` | Modellnyckeln, se [starta-labbet.md](starta-labbet.md) |

### Start-URL

```
https://datalab.sspcloud.fr/launcher/ide/vscode-python?autoLaunch=true&name=arkai-eneo&init.personalInit=https%3A%2F%2Fraw.githubusercontent.com%2Fjakobengdahl%2FArkAI%2Fmain%2Fverktyg%2Fonyxia-init.sh&init.personalInitArgs=bas&git.repository=https%3A%2F%2Fgithub.com%2Fjakobengdahl%2FArkAI.git&git.branch=main&vault.secret=arkai-hemligheter&kubernetes.role=edit&persistence.size=50Gi&resources.limits.memory=16Gi&resources.requests.memory=4Gi&networking.user.enabled=true&networking.user.ports[0]=8081&networking.user.ports[1]=8084
```

### Databasen, som egen tjänst

```
https://datalab.sspcloud.fr/launcher/databases/postgresql-cnpg?name=eneo-db&imageCatalog.major=16&extension.pgvector=true&storage.size=20Gi
```

`autoLaunch` är med flit **inte** satt här: användarnamn och lösenord ska fyllas i
i formuläret. De hör hemma i Vault, inte i en URL i ett publikt repo.
Chartet kör PostgreSQL 18 som standard; `16` är valt för att matcha det Eneo
dokumenterar.

## Arbetsordning i den nya miljön

1. `kubectl auth can-i create deployments` → ska svara `yes`. Gör den inte det är
   tjänsten startad med fel roll, och inget nedanför fungerar.
2. Starta `eneo-db` från katalogen. Lägg uppgifterna i Vault.
3. Deploya Redis — eget manifest, `redis:7-alpine`.
4. Skriv manifest för backend, frontend och worker från Eneos `docker-compose`.
   `JWT_SECRET`, `URL_SIGNING_KEY` och `PUBLIC_ORIGIN` i en Secret.
5. `PUBLIC_ORIGIN` är värdnamnet för port 8084. Det syns med
   `python3 verktyg/labb.py ingress 8084` när tjänsten kör.
6. Caddy i podden på 8084: `/api/*`, `/docs`, `/openapi.json`, `/version` till
   backend-tjänsten, allt annat till frontend-tjänsten.
7. Modellen kopplas in i Eneos admingränssnitt, inte via miljövariabler:
   provider `openai` med base-URL mot [plattformens inferens](sspcloud-llm.md).

Blir det gjort hör det hemma som ett skript i `verktyg/installera/`, på samma sätt
som resten — se [verktygslada.md](verktygslada.md).

## Vad som inte är verifierat

Tre saker kan välta planen, och ingen av dem går att avgöra utan att prova:

**Fungerar frontenden bakom en sökvägsdelande proxy?** Dokumentationen är tyst, och
`Host()`-routing i Traefik är det enda exemplet. Det här är den största osäkerheten.
Faller den, är alternativet två exponerade portar och cross-origin-cookies — vilket
kan kräva ändringar i Eneos cookie-inställningar.

**Kräver Eneo `/v1/embeddings`?** Dokumentationen säger att en OpenAI-kompatibel
server ska exponera både `/v1/chat/completions` och `/v1/embeddings`. Om
plattformens inferens gör det är inte kontrollerat. Gör den inte det behövs en egen
embeddingmodell för att RAG-delen ska fungera.

**Hämtningsgräns på Docker Hub.** `redis:7-alpine` ligger där, och anonyma
hämtningar i ett delat kluster kan slå i taket. Märks det, får imagen speglas.

## Källor

- <https://docs.eneo.ai/docs/getting-started>
- <https://docs.eneo.ai/guides/deployment>
- <https://docs.eneo.ai/docs/architecture>
- <https://docs.eneo.ai/guides/ai-providers>
- <https://github.com/eneo-ai/eneo>

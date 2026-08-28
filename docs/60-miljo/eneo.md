# Eneo i labbet

[Eneo](https://www.eneo.ai) är en öppen AI-plattform byggd av Sundsvalls och Ånge
kommun för svensk offentlig sektor. Den gör i grunden samma sak som Open WebUI —
chattgränssnitt mot språkmodeller — men med sådant som Open WebUI saknar:
behörighetsmodell per organisation, revisionslogg, OIDC-federation, SCIM. Det gör den
intressant för oss, för det är precis den sortens frågor som skiljer en PoC från
något som får köras i drift. Se [50-fran-poc-till-produktion](../50-fran-poc-till-produktion/).

**Eneo v2.1.1 kör i labbet sedan 2026-08-28.** Det här dokumentet beskriver hur, och
var installationen avviker från det Eneo själva dokumenterar. Underlaget för vägvalen
finns i [EXP-002](../30-experiment/EXP-002-eneo-i-kubernetes.md).

## Kort svar

Eneo dokumenterar bara `docker compose`, och det finns ingen containerruntime i
labbtjänsten. I stället kör Eneo som **sex arbetslaster i namnrymden** — samma
tjänster som compose-filen, översatta till Kubernetes-manifest — plus en **Caddy i
VS Code-podden** som lägger frontend och backend på samma värdnamn.

Två saker måste vara satta redan när Onyxia-tjänsten startar: `kubernetes.role=edit`
och en exponerad port för Eneo. Ingetdera går att ändra i efterhand.

Installationen tar knappt tre minuter och är ett kommando.

## Köra det

I panelen räcker det med knappen *Kör igång* på uppsättningen **Eneo som plattform**:
den installerar, startar och kopplar in modellerna i ett svep. I terminalen är det
samma sak:

```bash
verktyg/kor.sh uppsattning eneo-plattform   # allt nedan, i ordning

verktyg/kor.sh installera eneo      # deployar i namnrymden, ~3 min
verktyg/kor.sh starta eneo          # skalar upp och startar proxyn här i podden
verktyg/kor.sh atgard koppla-eneo   # kopplar in plattformens modeller
verktyg/kor.sh stoppa eneo          # proxyn ner, tjänsterna till noll — data kvar
verktyg/kor.sh avinstallera eneo    # tar bort allt, inklusive databasen
```

Adressen är värdnamnet för port 8084, och panelen visar den. Den första
inloggningen skrivs till `~/work/.labb/eneo-inloggning.txt` (utanför repot, läge
0600) och ligger också i Kubernetes-hemligheten `eneo-hemligheter`. **Byt lösenord
vid första inloggningen** — porten är publik, se
[minnesbanken](../../minnesbank/verktyg/exponerad-port-kraver-inloggning.md).

Eneo överlever att den här podden startas om: det enda som kör lokalt är proxyn.
Databasen ligger på en egen volym i namnrymden.

## Hur det är byggt

| Arbetslast | Image | Roll |
|---|---|---|
| `eneo-db` | `pgvector/pgvector:pg16` | PostgreSQL 16 med pgvector, 20 Gi volym |
| `eneo-redis` | `redis:7-alpine` | Cache och jobbkö (ARQ), 2 Gi volym |
| `eneo-db-init` | `eneo-backend` (Job) | Migreringar och första tenant/användare |
| `eneo-backend` | `ghcr.io/eneo-ai/eneo-backend` | FastAPI på 8000 |
| `eneo-worker` | samma image, `RUN_AS_WORKER=true` | Bakgrundsjobb |
| `eneo-frontend` | `ghcr.io/eneo-ai/eneo-frontend` | SvelteKit med SSR på 3000 |

Manifesten ligger i [`verktyg/eneo/`](../../verktyg/eneo/) och är mallar — de
renderas av installationsskriptet, som fyller i värdnamn, imager och storlekar.
Numreringen är körordningen: databasen först, sedan migreringen, sedan applikationen.

Backend- och frontendimagerna är pinnade till **de digester Eneo attesterar för
v2.1.1** (`IMAGE-DIGESTS.txt` i releasen), inte till en tagg. `/version` svarar
`2.1.1-dev` — versionssträngen i den släppta imagen är byggd så, det är inte en
utvecklingsbygge.

### Proxyn, och varför den behövs

Eneo vill ha frontend och backend på **samma origin**: frontenden sätter
sessionskakan, och webbläsaren skickar den vidare till API:et. Onyxia ger varje
exponerad port ett eget värdnamn, så två portar hade blivit två origins och trasig
inloggning.

Caddy lyssnar därför på 8084 i den här podden och delar trafiken på sökväg —
`/api/*`, `/scim/*`, `/docs`, `/openapi.json` och `/version` till backend, allt annat
till frontend. Det är samma delning som Eneos eget Traefik-exempel gör med
`PathPrefix`, vilket är hela skälet till att den fungerar: vi hittar inte på en ny
topologi, vi flyttar deras.

Strömmande svar går igenom: en fråga till assistenten kommer tillbaka som
`event: text`-strömmar via proxyn. Kakan sätts och inloggningen går igenom hela
vägen utifrån.

### Var vi avviker från Eneos compose-fil

**Databasen är en egen StatefulSet, inte katalogens `postgresql-cnpg`.**
CNPG-operatorn *finns* i klustret och vi får skapa `Cluster`-resurser — den vägen är
alltså öppen och är den mer driftlika. Vi valde ändå Eneos egen image, för att hålla
hela installationen i ett skript och en variabel färre mot compose-filen. Vill man ha
riktig operatorhanterad databas med backup är det bytet nästa steg, inte en
ommöblering.

**`/app/data` och `/tmp` delas inte mellan backend och worker.** I compose är de
gemensamma volymer. Lagringsklassen här (`rook-ceph-block`) är ReadWriteOnce, och två
poddar kan inte montera samma volym — så båda har var sin `emptyDir`. Följden:
**exporterade revisionsloggar går inte att ladda ner**, eftersom worker skriver filen
i sin podd och backend läser i sin. Behövs den funktionen är lösningen antingen en
delad ReadWriteMany-volym eller att objektlagring kopplas in.

**Webbkryparen är avstängd** (`USING_CRAWL=false`). Den drar långa jobb och mycket
minne, och det är inte den vi jämför plattformar på.

**Ingen OIDC.** Inloggning sker med e-post och lösenord mot Eneos egen
användardatabas. Federationen är en av de intressanta sakerna med Eneo, men den
kräver en identitetsleverantör att federera mot.

**Ingen TLS i proxyn.** Onyxias ingress terminerar TLS; Caddy kör `auto_https off`
och får `X-Forwarded-Proto: https` satt åt sig.

## Inställningar för miljön

Ingen av dem går att ändra i efterhand. Det här är vad tjänsten faktiskt startades
med, och vad som visade sig behövas.

| Parameter | Värde | Kommentar |
|---|---|---|
| `kubernetes.role` | `edit` | **Krävs.** Standard är `view`, och då går ingenting av det här |
| `networking.user.enabled` | `true` | Krävs för att exponera portar alls |
| `networking.user.ports[0]` | `8081` | Open WebUI — den vi jämför mot |
| `networking.user.ports[1]` | `8084` | Eneo, via proxyn |
| `git.branch` | grenen du vill ha | Utan den klonas standardgrenen |
| `vault.secret` | miljöns hemlighet | Modellnyckeln, se [starta-labbet.md](starta-labbet.md) |

**`persistence.size` och minnet behöver inte höjas för Eneos skull.** Planen räknade
med 50 Gi disk och 16 Gi minne på podden, av Eneos systemkrav. Men i den här vägen kör
Eneo *inte* i podden: data ligger på egna volymer i namnrymden (20 Gi + 2 Gi, mot
kvotens 2 Ti) och minnet tas av Eneos egna poddar, som har sina gränser satta i
manifesten (backend 4 Gi, databasen 2 Gi). Podden själv behöver bara plats för
Caddy-binären.

Tjänsten det här skrevs i startades förvisso med 50 Gi disk och 50 Gi minnestak, men
det säger inget om behovet: 6,6 GB av disken är använd, och det mesta av det är
`uv`-cache sedan tidigare.

### Start-URL

URL:en som startar en miljö med de här inställningarna står i
[starta-labbet.md](starta-labbet.md#urlen) — en enda gång, så att den inte hinner
glida isär från den som faktiskt används. Profilen `bas eneo` gör att Eneo
installeras direkt när miljön startar.

## Modellerna

Eneo läser inte modellnycklar ur miljön på det sätt Open WebUI gör. Modeller läggs
upp per organisation: först en **leverantör** med bas-URL och nyckel, sedan de
modeller man vill kunna välja. Nyckeln krypteras med `ENCRYPTION_KEY` och hamnar i
Eneos databas.

Det går att göra i admingränssnittet. [`verktyg/konfigurera-eneo.py`](../../verktyg/konfigurera-eneo.py)
gör samma sak mot API:et, av samma skäl som motsvarigheten för Open WebUI finns: en
installation som kräver sexton klick i ett formulär är inte reproducerbar.

Leverantören läggs upp som typ `openai` med `config.endpoint` mot
[plattformens inferens](sspcloud-llm.md). Bakom Eneos modellhantering ligger LiteLLM,
som med en egen `api_base` pratar vanlig OpenAI-dialekt med `Authorization: Bearer` —
alltså precis vad plattformen vill ha. (Provider-typen `vllm` finns också, men den
skickar nyckeln i `X-API-Key` och passar därför inte här.)

Två modeller är inkopplade och verifierade med Eneos egen `validate-model`, som gör
ett riktigt anrop:

| | Modell | Anmärkning |
|---|---|---|
| Chatt | plattformens standardmodell (`OPENAI_MODEL`) | Samma modell som Open WebUI kör, så jämförelsen blir på plattformen och inte på modellen |
| Embedding | plattformens embeddingmodell | 4096 dimensioner |

**Att plattformens inferens har `/embeddings` var en öppen fråga i planen.** Den har
det, och Eneo når den. Det betyder att kunskapskällor och RAG i Eneo kan köras helt
på plattformens modeller.

`max_input_tokens` och `max_output_tokens` är satta av oss (32768/4096) och
medvetet försiktiga. Plattformens modellista säger ingenting om kontextfönster, och
Eneo trunkerar själv utifrån värdet.

## Ta bort Eneo igen

Eneo kör i namnrymden, inte i podden. **Stoppar du VS Code-tjänsten fortsätter Eneo
att köra** och att ta av kvoten — sex poddar och 22 Gi lagring — tills någon tar bort
det. Det är samma egenskap som gör att det överlever en poddomstart; den har bara två
sidor. Se [minnesbanken](../../minnesbank/verktyg/namnrymden-overlever-podden.md).

Två olika saker, och skillnaden är inte kosmetisk:

| | Vad som händer | Data |
|---|---|---|
| **Stoppa** | Proxyn ner, alla arbetslaster skalas till noll | Kvar på volymerna |
| **Ta bort** | Allt märkt `app.kubernetes.io/part-of=eneo` raderas | Borta |

I panelen sitter *Ta bort* på Eneos kort. Den kör ingenting direkt: den leder till en
sida som visar exakt vilka arbetslaster, tjänster och volymer som försvinner, och
först där finns knappen. I terminalen:

```bash
verktyg/kor.sh avinstallera eneo               # allt, databasen med
verktyg/ta-bort-eneo.sh --behall-data          # arbetslasterna bort, volymerna kvar
```

`--behall-data` är vägen om du vill frigöra poddar men komma tillbaka till samma
databas senare: en ny `installera` monterar volymerna igen.

Panelens startsida visar också vad som ligger i namnrymden och hur mycket av kvoten
det tar, så att det går att se att något står kvar utan att leta i `kubectl`.

## Vad som inte är gjort

- **Backup.** Databasen ligger på en volym utan säkerhetskopiering. Med CNPG hade det
  följt med.
- **Uppgradering.** Byte till en ny Eneo-version är att ändra digesterna i
  installationsskriptet och köra om det. Migreringarna kör i jobbet. Inte provat.
- **OIDC och SCIM** — se ovan.
- **WebSocket genom proxyn.** Strömmande svar via SSE är verifierat. Eneo använder
  enligt dokumentationen även WebSocket; det har inte prövats separat.
- **Objektlagring.** Eneo kan lägga filer i en S3-kompatibel tjänst i stället för i
  databasen. Plattformen har S3 — det är ett rimligt nästa steg, och det skulle
  samtidigt lösa den delade volymen.

## Källor

- <https://docs.eneo.ai/docs/getting-started>
- <https://docs.eneo.ai/guides/deployment>
- <https://docs.eneo.ai/docs/architecture>
- <https://github.com/eneo-ai/eneo> — `docs/deployment/` på taggen `v2.1.1` är det
  som faktiskt gäller. Dokumentationssajten ligger efter koden.

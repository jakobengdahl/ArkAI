# Eneo i labbet

[Eneo](https://www.eneo.ai) är en öppen AI-plattform byggd av Sundsvalls och Ånge
kommun för svensk offentlig sektor. Den gör i grunden samma sak som Open WebUI —
chattgränssnitt mot språkmodeller — men med sådant som Open WebUI saknar:
behörighetsmodell per organisation, revisionslogg, OIDC-federation, SCIM. Det gör den
intressant för oss, för det är precis den sortens frågor som skiljer en PoC från
något som får köras i drift. Se [50-fran-poc-till-produktion](../50-fran-poc-till-produktion/).

**Eneo v2.2.2 kör i labbet sedan 2026-10-12** (v2.1.1 från 2026-08-28). Det här dokumentet beskriver hur, och
var installationen avviker från det Eneo själva dokumenterar. Underlaget för vägvalen
finns i [EXP-002](../30-experiment/EXP-002-eneo-i-kubernetes.md).

## Kort svar

Eneo dokumenterar bara `docker compose`, och det finns ingen containerruntime i
labbtjänsten. I stället kör Eneo som **fem arbetslaster i namnrymden** — samma
tjänster som compose-filen, översatta till Kubernetes-manifest — plus en **Caddy i
VS Code-podden** som lägger frontend och backend på samma värdnamn.

Två saker måste vara satta redan när Onyxia-tjänsten startar: `kubernetes.role=edit`
och en exponerad port för Eneo. Ingetdera går att ändra i efterhand.

Installationen tar knappt tre minuter och är ett kommando.

## Köra det

Enklast är att starta miljön med [länken med Eneo](starta-labbet.md#urlen). Då
installeras Eneo, startas och får modellerna inkopplade utan att du gör något mer.

I panelen sitter knapparna på Eneos kort: *Installera*, *Starta*, *Koppla in
modellerna*, *Stoppa*, *Ta bort*. I terminalen är det samma sak:

```bash
verktyg/kor.sh installera eneo       # deployar i namnrymden, ~3 min
verktyg/kor.sh starta eneo           # skalar upp och startar proxyn här i podden
verktyg/kor.sh koppla_eneo eneo      # kopplar in plattformens modeller
verktyg/kor.sh stoppa eneo           # proxyn ner, alla poddar till noll — data kvar
verktyg/kor.sh avinstallera eneo     # tar bort allt, inklusive databasen

verktyg/kor.sh uppsattning eneo-plattform   # allt utom det sista, i ordning
```

Adressen är värdnamnet för port 8084, och panelen visar den. Inloggningen är
`arkai@arkai.se` / `arkai@arkai.se` — användarnamn och lösenord är samma, i varje ny installation, satt av
installationsskriptet och lagrad i `eneo-hemligheter` (`DEFAULT_USER_PASSWORD`)
och `eneo-backend-konfig` (`DEFAULT_USER_EMAIL`).

Att den står i klartext i repot är ett medvetet val för ett labb med en enda
användare: ett slumpat lösenord i en fil utanför repot var mest i vägen. **Priset är
att porten är publik.** 8084 ligger på ett värdnamn som vem som helst når, och Eneos
egen inloggning är hela skyddet — se
[minnesbanken](../../minnesbank/verktyg/exponerad-port-kraver-inloggning.md). Ska
något känsligt in i den här instansen: sätt `ENEO_ADMIN_EPOST` och `ENEO_ADMIN_LOSEN`
före installationen, eller byt lösenordet i gränssnittet och sätt `ENEO_ADMIN_LOSEN`
för skripten.

Eneo överlever att den här podden startas om: det enda som kör lokalt är proxyn.
Databasen ligger på en egen volym i namnrymden.

## Vilka byggstenar Eneo är

Eneo är ett **applikationslager med en behörighetsmodell**. Det är den ärliga
sammanfattningen, och den förklarar både vad man får gratis och vad man måste bygga
på. Kartan står i [byggstenar.md](../20-tekniker/byggstenar.md); tabellen nedan är
samma karta lagd över den här installationen. Panelen visar den på Eneos kort, och
källan till båda är `[tjanst.eneo.byggstenar]` i
[`verktyg/labb.toml`](../../verktyg/labb.toml).

| Byggsten | Läge | Vad det betyder här |
|---|---|---|
| **Applikationslagret** | ingår | Chatt, assistenter, spaces och admingränssnitt. Det är produkten — den går inte att koppla bort |
| **Säkerhet och behörighet** | ingår | Roller, organisationer, spaces och revisionslogg. OIDC och SCIM finns i produkten men är inte påslaget här |
| **API-lagret** | ingår | Eneos eget API, och LiteLLM bakom modellhanteringen. Därför duger vilken OpenAI-kompatibel leverantör som helst |
| **Driftmiljön** | ställs in | Sex arbetslaster i namnrymden. Imager, minne och volymstorlekar står i `verktyg/eneo/` |
| **Modellen** | ställs in | Ingen modell från början. Leverantör med bas-URL och nyckel, sedan chatt- och embeddingmodell |
| **Verktygslagret** | går att lägga till | Ingen MCP-server från början, och ingen inbyggd verktygslåda. Se nedan |
| **Kontext och minne** | går att lägga till | Kunskapskällor per space — filer och webbsidor, indexerade med embeddingmodellen |
| **Arbetssätt som paket** | går att lägga till | Assistenter med egna prompter, och assistentmallar som admin kan versionera |
| **Orkestrering** | delvis | En assistent väljer bland sina verktyg i en tur. Flerstegsupplägg som planerar och kör vidare finns inte |
| **Mänsklig översyn** | delvis | Enskilda verktyg kan kräva godkännande innan de körs. Granskning av svar är en arbetsordning, inte en funktion |
| **Livscykelhantering** | delvis | Assistentmallar versioneras och går att rulla tillbaka. Modellversion, prompter och index gör det inte |
| **Utvärdering** | saknas | Insights ger användningsstatistik, inte kända fall och regressionstest |

De tre nedersta raderna är inte kritik av Eneo — de är samma tre som saknas i nästan
varje plattform, och de är skälet till att en PoC och en drift är olika saker. Se
[styrning-och-risk.md](../50-fran-poc-till-produktion/styrning-och-risk.md).

### Verktyg: MCP i Eneo

Eneo har inga verktyg från början. Adminen lägger upp **MCP-servrar per
organisation**, Eneo hämtar deras verktygslista, och sedan väljer varje assistent
vilka av dem den får använda. Två begränsningar styr vad som går att koppla in:

- **Bara Streamable HTTP.** Inte stdio, inte SSE. En stdio-server måste alltså köras
  över HTTP för att gå att koppla in — det är därför
  [Hello-MCP](../../exempel/mcp/hello-mcp/README.md) kör båda transporterna.
- **Eneo kör i namnrymden, inte i podden.** `127.0.0.1` betyder Eneos egen podd. En
  server här i VS Code-podden måste ligga på en exponerad port, alltså ett publikt
  värdnamn — och behöver då en token.

Panelen har en *Koppla in i Eneo*-knapp på de kort där det går. I terminalen:

```bash
verktyg/kor.sh koppla_eneo hello-mcp
verktyg/kor.sh koppla_eneo metadatagraf
```

Skriptet är [`verktyg/koppla-mcp-till-eneo.py`](../../verktyg/koppla-mcp-till-eneo.py).
Det läser adress och token ur manifestet, lägger upp servern om den saknas,
uppdaterar den annars, och säger hur många verktyg Eneo hittade. Noll verktyg
betyder att Eneo inte nådde servern.

## Hur det är byggt

| Arbetslast | Image | Roll |
|---|---|---|
| `eneo-db` | `pgvector/pgvector:pg16` | PostgreSQL 16 med pgvector, 20 Gi volym |
| `eneo-redis` | `redis:7-alpine` | Cache och jobbkö (ARQ), 2 Gi volym |
| `eneo-db-init` | `eneo-backend` (Job) | Migreringar och första tenant/användare |
| `eneo-backend` | `ghcr.io/eneo-ai/eneo-backend` | Två containrar i samma podd: FastAPI på 8000, och workern (samma image, `RUN_AS_WORKER=true`) för bakgrundsjobb |
| `eneo-frontend` | `ghcr.io/eneo-ai/eneo-frontend` | SvelteKit med SSR på 3000 |

Manifesten ligger i [`verktyg/eneo/`](../../verktyg/eneo/) och är mallar — de
renderas av installationsskriptet, som fyller i värdnamn, imager och storlekar.
Numreringen är körordningen: databasen först, sedan migreringen, sedan applikationen.

Backend- och frontendimagerna är pinnade till **digesterna som taggen `2.2.2` pekade
på i GHCR** när vi bytte, inte till en tagg. Taggen i GHCR saknar `v`, till skillnad
från releasen på GitHub. `/version` svarar `2.2.2-dev` — versionssträngen i den
släppta imagen är byggd så, det är inte ett utvecklingsbygge.

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

**Backend och worker kör i samma podd.** I compose är de två tjänster som delar
volymerna `/app/data` och `/tmp`. Lagringsklassen här (`rook-ceph-block`) är
ReadWriteOnce, och två poddar kan inte montera samma volym — men två containrar i en
podd kan dela en `emptyDir`. Delningen är inte valfri: backend skriver en uppladdad
fil till `/tmp` och lägger bara *sökvägen* i jobbkön, och workern öppnar sedan samma
sökväg. Det gäller fortfarande i 2.2.2, även med objektlagring inkopplad.

Fram till 2026-10-12 körde de i var sin podd med var sin `emptyDir`. Då misslyckades
**varje uppladdning till en kunskapskälla** — backend loggade att allt gick bra,
workern loggade `FileNotFoundError: [Errno 2] No such file or directory:
'/tmp/<id>'`, och i gränssnittet syntes bara att filen aldrig dök upp. Exporterade
revisionsloggar gick inte heller att ladda ner, av samma skäl. Se
[minnesbanken](../../minnesbank/verktyg/eneo-backend-och-worker-delar-tmp.md).

Priset är att backend och worker startas om och skalas tillsammans. Med en användare
spelar det ingen roll.

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
| `networking.user.ports[0]` | `8081` | Hello-MCP över HTTP, så att Eneo kan nå den. Var Open WebUI:s port |
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
glida isär från den som faktiskt används. Profilen `bas eneo` installerar Eneo redan
vid start; standardprofilen `bas` gör det inte, så att en miljö som ingen använder
inte har sex poddar igång.

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

## Byte till 2.2.2

**Har du installerat Eneo från det här repot före 2026-10-12 kör du 2.1.1, och
kunskapsuppladdningen fungerar inte hos dig.** Vägen framåt är att ta bort och
installera om — då hoppar du över 2.2:s engångsmigrering helt. Kontona, spacen,
assistenterna och kunskapskällorna försvinner. **Kopiera assistenternas promptar
och inställningar till en textfil innan du börjar.** Modellerna kopplas in igen av
sig själva, och Metadatagrafen också när tjänsten startas via URL:en med dess
uppgifter i Vault.

Utan terminal, tre steg:

1. **I panelen:** *Ta bort* på Eneos kort, och bekräfta. Det tar bort Eneo ur
   namnrymden — det gör inte att stänga VS Code-tjänsten.
2. **I Onyxia:** ta bort VS Code-tjänsten under *My services*.
3. **Starta en ny** med [URL:en](starta-labbet.md#urlen), med profilen `bas eneo`.
   Vänta några minuter och öppna länken *Port 8084* på tjänstens sida i Onyxia.

Den nya tjänsten klonar repot på nytt och får därmed den nya versionen. Steg 2 och
3 kan inte ersättas av att bara trycka *Installera* i den gamla panelen: den kör
koden som klonades när tjänsten startades, alltså 2.1.1.

Med terminal går det också att behålla tjänsten:

```bash
cd ~/work/ArkAI && git pull                # hämta den nya versionen
verktyg/kor.sh avinstallera eneo           # raderar databasen
verktyg/kor.sh installera eneo             # installerar, startar och kopplar in modellerna
```

Det som ändrats och som du märker:

- **Lösenordet är `arkai@arkai.se`, samma som användarnamnet.** Det tidigare
  `arkai2026` är för kort: 2.2 kräver minst 12 tecken. Har du satt
  `ENEO_ADMIN_LOSEN` själv måste det också vara minst 12 tecken.
- **Ingen `eneo-worker` längre.** Workern är en container i `eneo-backend`-podden.
  Loggarna läses med `kubectl logs deploy/eneo-backend -c worker`.
- **Personliga spaces** får alla aktiverade modeller och MCP-servrar automatiskt
  och går inte att ändra via API:et (403). Det gjorde de i 2.1.1.
- **Organisationens space** skapas av Eneo och nås via
  `/api/v1/spaces/type/organization/`. Skapa inte ett eget med samma namn.
- MCP-servrar som pekade på en tidigare VS Code-podds värdnamn (Hello-MCP på port
  8081) slutade fungera när podden byttes ut. De behöver kopplas in på nytt mot den
  nya podden.

Vill du i stället uppgradera med datan kvar gäller Eneos egen
[uppgraderingsguide](https://docs.eneo.ai/guides/file-icon-storage-upgrade):
skrivskyddad kontroll med den nya imagen, backup, stoppa alla gamla backend- och
workerprocesser, kör `db-init`, starta den nya. Konfigurationen i repot är redan
anpassad. Vi har inte provat den vägen.

Konfiguration som ändrade betydelse i 2.2 och som stoppade installationen:

| Variabel | 2.1.1 | 2.2.2 |
|---|---|---|
| `JWT_EXPIRY_TIME` | `86400` i Eneos mall | Minuter, högst `43200`. `86400` stoppar migreringen med ett felmeddelande. Nu `1440` |
| `FEDERATION_PER_TENANT_ENABLED` | Används | Utfasad, varnar vid start. Ersatt av `FEDERATION_ENABLED` |
| `ENEO_SUPER_DUPER_API_KEY` | Används | Läses inte. Skapas inte längre |

## Ta bort Eneo igen

Eneo kör i namnrymden, inte i podden. **Stoppar du VS Code-tjänsten fortsätter Eneo
att köra** och att ta av kvoten — sex poddar och 22 Gi lagring — tills någon tar bort
det. Det är samma egenskap som gör att det överlever en poddomstart; den har bara två
sidor. Se [minnesbanken](../../minnesbank/verktyg/namnrymden-overlever-podden.md).

Två olika saker, och skillnaden är inte kosmetisk:

| | Vad som händer | Poddar kvar | Data |
|---|---|---|---|
| **Stoppa** | Proxyn ner, alla arbetslaster skalas till noll | Nej — inga | Kvar på volymerna |
| **Ta bort** | Allt märkt `app.kubernetes.io/part-of=eneo` raderas | Nej | Borta |

*Stoppa* är alltså den normala vägen när man är klar för dagen: **inga poddar kör,
ingenting tar CPU eller minne**, bara volymerna ligger kvar och tar av
lagringskvoten. Nästa `starta` skalar upp igen och allt är som det var.

### Assistenterna, och vad som överlever

Assistenter, spaces, kunskapskällor, modellkopplingar och konton ligger i
PostgreSQL, på volymen `eneo-db`. Den lever i **namnrymden**, inte i podden, och
överlever därför:

- att den här podden startas om,
- att hela VS Code-tjänsten stoppas och startas igen,
- `verktyg/kor.sh stoppa eneo`,
- `verktyg/ta-bort-eneo.sh --behall-data`.

Det enda som raderar dem är *Ta bort* i panelen, alltså `avinstallera` — och den går
via en bekräftelsesida som visar exakt vilka volymer som försvinner.

Det finns alltså **ingen export att komma ihåg**: en assistent du bygger i dag finns
kvar nästa gång du startar miljön, så länge du stoppar i stället för att ta bort. Vad
som *inte* finns är en säkerhetskopia: försvinner volymen finns ingen andra kopia, och
Eneo har ingen inbyggd export av assistenter. Behöver en assistentdefinition
överleva att databasen är borta får den skrivas ner i repot och läggas in igen för
hand — eller så byggs en export mot API:et (`/api/v1/assistants/`), vilket ingen har
gjort ännu.

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
  följt med. Det är den enda kopian av assistenter och kunskapskällor — se
  [Assistenterna, och vad som överlever](#assistenterna-och-vad-som-överlever).
- **Uppgradering på plats.** Byte från 2.1.x till 2.2.x är inte ett digestbyte —
  se [Byte till 2.2.2](#byte-till-222). Vi har bara provat att ta bort och
  installera om. Inom 2.2.x är det enligt Eneo ett digestbyte; inte provat.
- **OIDC och SCIM** — se ovan.
- **WebSocket genom proxyn.** Strömmande svar via SSE är verifierat. Eneo använder
  enligt dokumentationen även WebSocket; det har inte prövats separat.
- **Objektlagring.** Från 2.2.0 kan en administratör koppla in en S3-kompatibel
  tjänst för filinnehåll (Admin → Fillagring); i 2.1.1 fanns det inte. Det löser
  *inte* den delade `/tmp` — se ovan. Anslutningen tar bara access key och secret,
  ingen session token, så Onyxias `AWS_*`-uppgifter duger inte: de är STS-uppgifter
  som går ut efter sju dagar. Det skulle krävas en serviceaccount-nyckel i MinIO.
  Hälsokontrollen svarar `object_content: NOT_CONFIGURED`, och det är väntat.

## Källor

- <https://docs.eneo.ai/docs/getting-started>
- <https://docs.eneo.ai/guides/deployment>
- <https://docs.eneo.ai/docs/architecture>
- <https://github.com/eneo-ai/eneo> — `docs/deployment/` på taggen `v2.2.2` är det
  som faktiskt gäller. Dokumentationssajten ligger efter koden.

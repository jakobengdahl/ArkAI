# EXP-002 · Eneo utan Docker, i namnrymden

**Datum:** 2026-08-28
**Gjort av:** labbet
**Tidsåtgång:** en förmiddag

## Slutsats

Ja. Eneo v2.1.1 går att köra i labbmiljön trots att projektet bara dokumenterar
`docker compose` och trots att det inte finns någon containerruntime i tjänsten: sex
arbetslaster i namnrymden, plus en Caddy i podden som lägger frontend och backend på
samma origin. Installationen är ett kommando och tar knappt tre minuter.

Den största osäkerheten i [planen](../60-miljo/eneo.md) — om frontenden klarar en
proxy som delar på sökväg i stället för värdnamn — visade sig inte vara någon
osäkerhet alls. Eneos eget Traefik-exempel gör exakt samma sökvägsdelning. Inloggning,
sessionskaka och strömmande svar går igenom.

Den andra öppna frågan besvarades också: plattformens inferens **har** `/embeddings`,
och Eneo når den. RAG i Eneo kan alltså köras helt på plattformens modeller.

## Frågan

Går Eneo att installera i en Onyxia-tjänst utan containerruntime, och räcker de
inställningar som gick att sätta vid tjänstestart?

## Vad vi gjorde

Tjänsten startades om med `kubernetes.role=edit` och två exponerade portar (8081 för
Open WebUI, 8084 för Eneo). Det var det enda som inte gick att göra i efterhand.

Sedan: Eneos `docker-compose.yml` och `env_backend.template` från taggen `v2.1.1`
översattes till tre manifestmallar i [`verktyg/eneo/`](../../verktyg/eneo/) — data,
migrering, applikation — och ett skript som renderar och applicerar dem i ordning.

```bash
verktyg/kor.sh installera eneo      # ~3 min
verktyg/kor.sh starta eneo
verktyg/kor.sh atgard koppla-eneo
```

Versioner: Eneo 2.1.1 (backend- och frontendimager pinnade till digesterna i
releasens `IMAGE-DIGESTS.txt`), `pgvector/pgvector:pg16`, `redis:7-alpine`,
Caddy 2.11.4, Kubernetes-klient 1.36.3.

## Vad som hände

**Migreringen och första användaren gick igenom på 45 sekunder.** `init_db.py`
körde alembic hela vägen och la upp tenant, admin och `allowed_origins`.

**Backend, worker och frontend kom upp utan tillrättalägganden.** Ingen av dem
behövde ändrade inställningar utöver värdnamn och tjänstenamn.

Verifierat efteråt, i den ordningen:

| Kontroll | Resultat |
|---|---|
| `/version` genom proxyn | `{"version":"2.1.1-dev"}` |
| Inloggning mot backendens `/api/v1/users/login/token/` | 200, token |
| Inloggning via frontendens formulär, utifrån | 302 till `/spaces/personal/chat`, `auth`-kaka satt |
| Fråga till standardassistenten, `stream: true` | `event: text`-ström genom proxyn |
| Modellerna genom Eneos `validate-model` | chatt och embedding svarar |
| `kor.sh stoppa eneo` och `starta eneo` igen | uppe efter ~2 min, konto och modeller kvar |

## Vad vi lärde oss

- **Ta reverse proxy-reglerna rakt av ur projektets eget exempel.** Eneos
  Traefik-labels räknar upp sökvägarna som ska till backend. Samma lista i en
  Caddyfile fungerade direkt. Osäkerheten i planen kom av att vi läste
  `Host()`-routingen som ett krav i stället för som ett exempel.
- **Två exponerade portar hade varit fel väg.** De blir två origins.
  Se [minnesbanken](../../minnesbank/verktyg/tva-portar-ar-tva-origins.md).
- **Kubernetes har ingen motsvarighet till `depends_on: condition: service_healthy`.**
  Compose-filen gaterar backend på att migreringsjobbet är klart. Här blev det tre
  manifestfiler och ett skript som väntar mellan dem — både `init_db.py` och
  backendens start kör `alembic upgrade head`, och två samtidiga migreringar mot
  samma databas är inte värt att chansa på.
- **Plattformens inferens duger som modelleverantör i Eneo**, som typ `openai` med
  egen `api_base`. Bakom Eneos modellhantering ligger LiteLLM, som då pratar vanlig
  OpenAI-dialekt med `Authorization: Bearer`. Provider-typen `vllm` hade *inte*
  fungerat: den skickar nyckeln i `X-API-Key`.

## Vad som inte fungerade

**Vi drog fel slutsats om databasen.** `kubectl get crd | grep cnpg` gav tomt, och
slutsatsen blev att CloudNativePG saknades i klustret och att katalogens
`postgresql-cnpg` därmed var stängd. Men att lista CRD:er är förbjudet i namnrymden —
`Forbidden` är inte samma sak som `finns inte`. `kubectl api-resources` visar hela
`postgresql.cnpg.io`-familjen, och vi får skapa `Cluster`-resurser.
Se [minnesbanken](../../minnesbank/verktyg/forbjudet-ar-inte-saknat.md). Databasen
kör nu som en egen StatefulSet med Eneos egen image, vilket är ett rimligt val — men
det var ett val, inte det enda som gick.

**Panelen pekade på fel värdnamn för den andra porten.** `verktyg/labb.py` läste
`rules[0].host` ur ingressen. Med bara en exponerad port märks det inte; med två får
den andra porten den förstas värdnamn — och det värdet går rakt in i Eneos
`PUBLIC_ORIGIN`, där fel värde ger tyst trasig inloggning. Rättat, och skrivet som
[minnespost](../../minnesbank/verktyg/en-ingress-regel-per-port.md).

**Första installationskörningen dog i mallrenderingen.** Manifestmallarna renderas
med `string.Template`, och en kommentar i filen innehöll `${...}` som exempel. Python
försöker ersätta även det som står i en YAML-kommentar:
`ValueError: Invalid placeholder in string: line 3, col 49`.

**En felsökning som var vårt eget fel.** Eneos `validate-model` svarade
`NotFoundError ... Received Model Group=<embeddingmodellen>` för embeddingmodellen,
vilket såg ut som att plattformen saknade `/embeddings`. Den gjorde inte det: fältet
i anropet heter `model_type`, inte `mode`, och med okänt fältnamn föll typen tillbaka
på `completion` — alltså en chattfråga till en embeddingmodell. Med rätt fältnamn
svarar båda. Det som såg ut som en begränsning hos plattformen var en stavning hos
oss.

## Vad vi inte hann eller inte kunde svara på

- **Om Eneo faktiskt är bättre än Open WebUI för våra frågor.** Den jämförelsen är
  hela poängen och är inte gjord. Den här filen svarar bara på om det går att köra.
- **OIDC och SCIM** — det som mest skiljer plattformarna åt. Kräver en
  identitetsleverantör att federera mot.
- **Uppgradering till nästa version.** Byte av digest plus omkörning, i teorin.
- **WebSocket genom proxyn.** SSE är verifierat, WebSocket inte.
- **Backup.** Databasen ligger på en volym utan säkerhetskopiering.

## Nästa steg

1. Kör samma uppgift i Eneo och i Open WebUI och skriv ner vad som skiljer — det
   är det experimentet som faktiskt besvarar varför Eneo är intressant.
2. Lägg in ett kunskapsunderlag i Eneo och se vad hämtningen ger med plattformens
   embeddingmodell.
3. Byt databasen till katalogens `postgresql-cnpg` om installationen ska leva längre
   än ett experiment — det är den som ger backup och failover.

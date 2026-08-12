# Labbmiljön: SSP Cloud / Onyxia

[Onyxia](https://onyxia.sh) är en öppen källkodsplattform som gör ett
Kubernetes-kluster till en datalabbmiljö. SSP Cloud är en instans av den. Onyxia är
värt att förstå i sig — det är i praktiken en referensarkitektur för "självbetjänings-
plattform ovanpå Kubernetes", och flera av frågorna vi brottas med kring PoC → produktion
har de redan besvarat på ett sätt vi kan lära av.

Onyxias egen dokumentation: <https://docs.onyxia.sh/> (finns även som markdown — lägg
till `.md` på vilken sid-URL som helst, och det finns en `llms.txt` med hela indexet.
Bra att veta när man vill mata den till ett AI-verktyg.)

## De tre delarna

| Del | Vad det är | Vad du kommer åt det med |
|---|---|---|
| **Tjänster** | Det du startar från katalogen. Körs i din Kubernetes-namnrymd. | Onyxias webbgränssnitt, `kubectl` |
| **Filer** | S3-lagring (MinIO). Personlig bucket + eventuella projekt-buckets. | Filutforskaren, `mc`, `AWS_*`-variabler |
| **Hemligheter** | Vault (key–value v2). | Hemlighetsutforskaren, `VAULT_*`-variabler |

Åtkomsten bygger genomgående på din inloggning (OIDC/Keycloak). Onyxia proxar inte
S3 utan hämtar tillfälliga STS-uppgifter åt dig — därför roteras `AWS_*`-variablerna,
och därför ska du aldrig skriva ner dem någonstans.

## Behörigheter sätts när tjänsten startar

Det här är den enskilt viktigaste sak att förstå om miljön, och det som är lättast
att missa.

### Kubernetes-roll

I startformuläret finns **Kubernetes permissions** med tre roller — alla begränsade
till din egen namnrymd:

| Roll | Vad du kan göra | När |
|---|---|---|
| `view` | läsa resurser | **standard** — räcker för vanligt arbete |
| `edit` | skapa och ändra resurser | när du vill deploya något själv |
| `admin` | dessutom hantera roller och behörigheter | när du experimenterar med RBAC |

Startar du en tjänst med standardvalet och sedan försöker `helm install` något får du:

```console
$ kubectl auth can-i create deployments
no
```

Det är alltså inte en begränsning i plattformen, utan valet `view`. Vill du kunna
deploya egna saker inifrån VS Code — starta tjänsten med `edit` eller `admin`.

**Rollen går bara att sätta vid start.** Samma sak gäller de flesta andra
inställningar nedan. Hemkatalogen är persistent, så att starta om en tjänst med
andra inställningar kostar bara några minuter — gör det hellre än att kämpa emot.

### Nätverk → portar

Under **Network access**: *"Enable access to your service through specific ports"*.
Ange den port du tänker köra något på, t.ex. `8081`. Porten får en egen ingress-URL
vid sidan av VS Code-URL:en. Se [openwebui.md](openwebui.md).

### AI-assistent

Under **AI Assistant** kopplas plattformens LLM-inferens in i tjänsten. Det innebär
konkret att en API-nyckel och en modell skrivs in i `~/.continue/config.yaml` och
`~/.config/opencode/opencode.jsonc` när tjänsten startar.
Se [ai-verktyg-i-imagen.md](ai-verktyg-i-imagen.md) och [sspcloud-llm.md](sspcloud-llm.md).

### Git

Repo-URL, användarnamn, e-post och access-token. Repot klonas automatiskt.
Se [git-och-auth.md](git-och-auth.md) — det finns en fallgrop där.

### Vault och S3

Kan monteras in i tjänsten som miljövariabler. Det är så du får hemligheter in i en
körande tjänst utan att skriva dem i repot.

## Podden är förgänglig, hemkatalogen är det inte

`/home/onyxia/work` ligger på en persistent volym. Allt annat — `apt`-paket, saker
under `/usr`, körande processer — försvinner vid omstart.

Det gör att sådant du installerar med `uv tool install` eller `npm install -g`
(under `~/.local`) överlever, medan `sudo apt install` inte gör det. Därför finns
`verktyg/`-skripten i det här repot.

```bash
./verktyg/kontrollera-miljo.sh    # vad finns, vad saknas
```

## Port 8080 är upptagen

Det är code-server (VS Code självt). Använd 8081 och uppåt.

## Att dela med kollegor

Se [delade-resurser.md](delade-resurser.md). Kort version: Onyxia har **projekt** —
grupper av användare som delar namnrymd, S3-bucket, hemligheter och inställningar.
Det är den mekanism vi vill använda för en gemensam minnesbank som är större än vad
som är lämpligt att lägga i ett publikt git-repo.

## Tjänster värda att starta från katalogen

Katalogen ändras; det här fanns när dokumentet skrevs och är relevant för våra experiment.

| Tjänst | Katalog | Användning hos oss |
|---|---|---|
| Neo4j | Databaser | Grafbaserat minne — [20-tekniker/grafminne.md](../20-tekniker/grafminne.md) |
| Qdrant / Milvus | Databaser | Vektorindex för semantisk sökning i minnesbanken |
| PostgreSQL | Databaser | Strukturerat minne, metadata, `pgvector` |
| Elastic | Databaser | Lexikal sökning — jämförelsepunkt mot vektorsökning |
| Langfuse | Automation | Spårning och utvärdering av LLM-anrop. Direkt relevant för PoC → produktion |

**Open WebUI och Ollama finns inte i katalogen.** Open WebUI installerar vi i
VS Code-tjänsten, se [openwebui.md](openwebui.md). För modeller finns plattformens
egen inferens, se [sspcloud-llm.md](sspcloud-llm.md).

## Vidare läsning

- [sspcloud-llm.md](sspcloud-llm.md) — plattformens LLM-inferens och API-nyckel
- [ai-verktyg-i-imagen.md](ai-verktyg-i-imagen.md) — opencode och Continue är förinstallerade
- [delade-resurser.md](delade-resurser.md) — projekt, S3, delning
- [git-och-auth.md](git-och-auth.md) — git, GitHub CLI, tokens
- [verktygslada.md](verktygslada.md) — installera om verktyg efter omstart
- [openwebui.md](openwebui.md) — Open WebUI

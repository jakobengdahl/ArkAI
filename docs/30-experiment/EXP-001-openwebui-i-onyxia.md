# EXP-001 · Kan Open WebUI köras i en Onyxia-tjänst?

**Datum:** 2026-08-12
**Gjort av:** uppsättningen av labbmiljön
**Tidsåtgång:** ~1 timme, varav ~20 minuter installation

## Slutsats

Ja. Open WebUI 0.11.0 kör i en `vscode-python`-tjänst, installerat med
`uv tool install --python 3.11 open-webui`, på port **8081** (inte 8080 — där sitter
code-server). Det behövs varken Docker eller Kubernetes-rättigheter.

För att nå gränssnittet i webbläsaren ska tjänsten startas med portexponering under
**Network access**. Det gick inte att verifiera i efterhand eftersom inställningen
bara kan sättas när tjänsten startar — se "Vad vi inte kunde svara på".

## Frågan

Går Open WebUI att köra i den befintliga VS Code-tjänsten, utan Docker och utan
rättigheter att deploya i Kubernetes?

Bakgrunden är att Open WebUI normalt distribueras som container, och att den inte
finns i Onyxias katalog.

## Vad vi gjorde

```bash
# Python 3.11 — imagen har 3.13, som Open WebUI inte stödjer
uv python install 3.11
uv tool install --python 3.11 open-webui
export PATH="$HOME/.local/bin:$PATH"

# Starta
mkdir -p /home/onyxia/work/open-webui-data
DATA_DIR=/home/onyxia/work/open-webui-data WEBUI_AUTH=False \
  ENABLE_OPENAI_API=False ENABLE_OLLAMA_API=False \
  open-webui serve --host 127.0.0.1 --port 8081
```

Verifiering:

```console
$ curl -s http://127.0.0.1:8081/health
{"status":true}
$ curl -s http://127.0.0.1:8081/api/config | jq '{name, version}'
{"name": "Open WebUI", "version": "0.11.0"}
```

## Vad som hände

Installationen tog ett par minuter och drog in ett stort antal beroenden. Första
starten tog ytterligare ~40 sekunder eftersom en embeddingmodell
(`sentence-transformers/all-MiniLM-L6-v2`) hämtas ner vid uppstart.

Efter det svarade tjänsten normalt.

## Vad vi lärde oss

- **Port 8080 är upptagen av code-server.** Detta var det första försöket och det
  misslyckades. Se [minnesposten](../../minnesbank/verktyg/onyxia-port-8080-upptagen.md).
- **`uv` löser versionskonflikten elegant.** Installationen hamnar under `~/.local`,
  alltså på den persistenta volymen, och överlever poddomstarter — till skillnad från
  allt man installerar med `apt`.
  [Minnespost](../../minnesbank/verktyg/openwebui-kraver-python-311.md).
- **`ss` och `lsof` finns inte i imagen.** Det gjorde felsökningen av portkonflikten
  onödigt förvirrande. `timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/8081"` fungerar
  utan dem.
- **Onyxias behörighetsmodell missförstods först.** Se nedan.

## Vad som inte fungerade

**Första starten på port 8080.** Felet doldes i uppstartsloggen, och ett `curl` mot
`localhost:8080/health` svarade `401 Unauthorized` — från code-server. Det ser ut som
ett autentiseringsproblem i den egna tjänsten. Det verkliga felet låg 40 rader upp:

```
[Errno 98] error while attempting to bind on address ('127.0.0.1', 8080): address already in use
```

**Fel slutsats om Kubernetes-rättigheter.** `kubectl auth can-i create deployments`
svarade `no`, och vi drog slutsatsen att plattformen inte tillåter användare att
deploya. Fel: rättigheterna styrs av **Kubernetes-rollen som väljs när tjänsten
startar** (`view` / `edit` / `admin`), och standardvalet är `view`. Tjänsten hade
alltså startats med minsta möjliga behörighet.

Värt att notera som mönster: felet var inte tekniskt utan en missad
konfigurationsinställning, och det ledde till en dokumenterad "begränsning" som inte
finns. Kontrollera hur tjänsten startades innan du drar slutsatser om plattformen.
[Minnespost](../../minnesbank/verktyg/onyxia-behorigheter-satts-vid-start.md).

**Verifiering via code-servers proxy.** `/proxy/8081/` och `/absproxy/8081/` finns
båda som rutter men kräver en inloggad session. Ett försök att logga in med `curl`
mot `/login` fick ingen giltig cookie, så det gick inte att bekräfta att Open WebUI:s
statiska filer fungerar under ett sökvägsprefix. Det är en känd svårighet för
SPA-applikationer som förväntar sig att ligga i roten.

## Vad vi inte kunde svara på

- Fungerar Open WebUI under code-servers `/proxy/8081/`? Obekräftat. Behöver testas
  från en webbläsare med inloggad session.
- Fungerar den egna ingressen som Onyxias **Network access → Ports** ger?
  Inställningen fanns i chartens schema (`networking.user.enabled` + `port`), men går
  bara att sätta vid start. Behöver testas nästa gång en tjänst startas.
- Hur mycket resurser drar den under verklig användning? Bara uppstart mättes.

## Nästa steg

1. Starta om VS Code-tjänsten med **Network access → port 8081** och
   **Kubernetes permissions → edit**. Bekräfta att ingressen fungerar.
2. Peka instansen mot [plattformens LLM-inferens](../60-miljo/sspcloud-llm.md) och
   kör ett riktigt användningsfall.
3. Sätt `WEBUI_AUTH=True` och `WEBUI_SECRET_KEY` innan någon kollega ska nå den.

Dokumentation som blev av det här: [../60-miljo/openwebui.md](../60-miljo/openwebui.md),
[`verktyg/starta-openwebui.sh`](../../verktyg/starta-openwebui.sh).

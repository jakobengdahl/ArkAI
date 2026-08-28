# Verktygslådan

Onyxia-poddar är förgängliga. Allt du installerar med `apt` försvinner vid omstart;
allt under `/home/onyxia` finns kvar.

Slutsatsen vi dragit av det: **installera aldrig med `apt` det som går att lägga i
hemkatalogen.** Alla verktyg nedan hamnar under `~/.local`, ingenting kräver `sudo`,
och andra gången du startar en tjänst är allt redan på plats.

Normalt behöver du inte köra något av det här för hand:

```bash
./verktyg/labb-start.sh            # grunden, i ett steg
./verktyg/kontrollera-miljo.sh     # vad finns, vad saknas
```

## Finns redan i imagen

`git`, `python3` (3.13), `uv`, `jq`, `curl`, `kubectl`, `helm`, `mc`.
Kör inte om det som redan finns.

## Grunden: Node och GitHub CLI

```bash
./verktyg/installera/bas.sh
```

Skriptet hämtar båda som tarball till `~/.local`, sätter `PATH` i `~/.bashrc` och
kör `satt-upp-git-auth.sh`. Idempotent — kör om det när du vill.

**Node 24 eller senare**, dels för MCP-servrar som distribueras via npm (fortfarande
majoriteten, och `npx` är standardsättet att köra dem), dels för att OpenClaw kräver
22.22.3+/24.15+.

**GitHub CLI** behövs för pull requests och för att slippa token i klartext.

## Python 3.11 för Open WebUI

Imagen har 3.13. Open WebUI kräver 3.11. `uv` löser det utan att röra systemets Python:

```bash
./verktyg/kor.sh installera openwebui
```

vilket i praktiken är:

```bash
uv python install 3.11
uv tool install --python 3.11 open-webui
```

## Caddy för Eneo

Eneo behöver en proxy i podden som lägger frontend och backend på samma värdnamn.
Binären hämtas från Caddys releaser till `~/.local/bin` av
`./verktyg/kor.sh installera eneo` och överlever en omstart som allt annat där. Själva
Eneo kör i namnrymden och behöver inte installeras om — se [eneo.md](eneo.md).

## Python-beroenden för experiment

Använd `uv` med en projektlokal virtuell miljö — inte `pip install` mot systemets
Python.

```bash
cd exempel/mcp/hello-mcp
uv sync            # skapar .venv utifrån pyproject.toml
uv run server.py
```

## Efter en poddomstart

Ingenting. Verktygen ligger kvar under `~/.local`; det som försvann var de körande
processerna. Starta om dem från panelen, eller:

```bash
cd ~/work/ArkAI
./verktyg/labb-start.sh
```

Startade du tjänsten via [labbets URL](starta-labbet.md) sker även det automatiskt —
Onyxias startformulär har ett fält för ett init-skript, och det är där
[`verktyg/onyxia-init.sh`](../../verktyg/onyxia-init.sh) kopplas in.

## Nätverksverktyg

`ss` och `lsof` saknas i imagen och kräver `apt`, alltså ominstallation efter varje
omstart. Vi har därför slutat förlita oss på dem — panelen och skripten sonderar
portar med bash i stället:

```bash
timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/8081" && echo upptagen || echo ledig
```

Vill du ändå ha dem: `sudo apt-get install -y iproute2 lsof net-tools`.

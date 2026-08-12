# Verktygslådan

Onyxia-poddar är förgängliga. Allt du installerar med `apt` försvinner vid omstart;
allt under `/home/onyxia` finns kvar. Det här dokumentet är receptet för att komma
tillbaka till en fungerande arbetsmiljö.

Kontrollera först vad som saknas:

```bash
./verktyg/kontrollera-miljo.sh
```

## Finns redan i imagen

`git`, `python3` (3.13), `uv`, `jq`, `curl`, `kubectl`, `helm`, `mc`.
Kör inte om det som redan finns.

## GitHub CLI

Behövs för pull requests och för att slippa token i klartext.

```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null
sudo apt-get update -qq && sudo apt-get install -y gh
```

Sedan: `./verktyg/satt-upp-git-auth.sh`

## Node.js

Behövs för de MCP-servrar som distribueras via npm — det är fortfarande majoriteten
av dem, och `npx` är standardsättet att köra dem.

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

## Python 3.11 för Open WebUI

Imagen har 3.13. Open WebUI kräver 3.11. `uv` löser det utan att röra systemets Python:

```bash
uv python install 3.11
uv tool install --python 3.11 open-webui
export PATH="$HOME/.local/bin:$PATH"    # lägg till i ~/.bashrc
```

## Nätverksverktyg

`ss` och `lsof` saknas i imagen, vilket är förvirrande första gången du ska ta reda på
vad som lyssnar på en port.

```bash
sudo apt-get install -y iproute2 lsof net-tools
```

Utan dem duger bash:

```bash
timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/8081" && echo upptagen || echo ledig
```

## Python-beroenden för experiment

Använd `uv` med en projektlokal virtuell miljö — inte `pip install` mot systemets
Python.

```bash
cd exempel/mcp/hello-mcp
uv sync            # skapar .venv utifrån pyproject.toml
uv run server.py
```

## Vad som är värt att automatisera

Efter en poddomstart:

```bash
cd ~/work/ArkAI
./verktyg/kontrollera-miljo.sh      # se vad som saknas
./verktyg/satt-upp-git-auth.sh      # git + gh
export PATH="$HOME/.local/bin:$PATH"
```

Bara `gh`, `node` och nätverksverktygen behöver installeras om — resten ligger
persistent. Det tar ett par minuter.

Onyxias startformulär har också ett fält för ett init-skript (en URL till ett
shellskript som körs när tjänsten startar). Vill du slippa stegen ovan helt är det
rätt ställe att lägga dem. Lägg i så fall skriptet i det här repot och peka på
`raw.githubusercontent.com`-URL:en — då kan alla i teamet återanvända det.

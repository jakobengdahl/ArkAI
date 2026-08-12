# AI-verktygen som redan finns i imagen

Onyxias datascience-image kommer med AI-utvecklingsverktyg förinstallerade, och
plattformen kan koppla in sin egen LLM-inferens i dem åt dig när tjänsten startar.
Det är lätt att missa — och det är ett bra utgångsläge för experimenten i
[20-tekniker/](../20-tekniker/).

## Vad som finns

| Verktyg | Vad det är | Var det konfigureras |
|---|---|---|
| **opencode** | Agent för utveckling i terminalen | `~/.config/opencode/opencode.jsonc` |
| **Continue** | VS Code-tillägg: chatt och autocomplete i editorn | `~/.continue/config.yaml` |

Kontrollera vad du har:

```bash
opencode --version
cat ~/.config/opencode/opencode.jsonc
cat ~/.continue/config.yaml
```

## Onyxia fyller i konfigurationen åt dig

Slår du på **AI Assistant** i startformuläret skriver Onyxia in modell, bas-URL och
API-nyckel i båda konfigurationsfilerna. Du behöver alltså inte konfigurera något
själv för att komma igång.

Två saker är värda att veta om det:

**Nyckeln ligger i klartext i hemkatalogen.** Både `~/.continue/config.yaml` och
`~/.config/opencode/opencode.jsonc` innehåller en fungerande API-nyckel. Hemkatalogen
är persistent, filerna är läsbara för allt som kör i podden, och de kommer med om du
kopierar hemkatalogen någonstans. Samma sak som med git-token, se
[git-och-auth.md](git-och-auth.md). Klistra aldrig in de här filerna någonstans utan
att först rensa nyckeln.

**Du styr inte vilken modell som konfigureras.** Vill du peka mot något annat — en
annan modell, plattformens egen inferens, en lokal modell — redigerar du filerna
själv. Formatet är dokumenterat hos [opencode](https://opencode.ai) respektive
[Continue](https://docs.continue.dev).

## Continue kommer med en MCP-server

Det här är det mest intressanta i sammanhanget. `~/.continue/config.yaml` innehåller
ett `mcpServers`-block som redan kopplar in en MCP-server för DuckDB:

```yaml
mcpServers:
  - name: DuckDB
    command: uvx
    args: [mcp-server-motherduck, --allow-switch-databases, --read-write,
           --db-path, ":memory:", --home-dir, /home/onyxia]
```

Det är ett färdigt, körande exempel på precis det mönster vi vill förstå: en
chattbot i editorn som via MCP kan fråga en riktig databas i stället för att gissa.
Titta på det innan du bygger din första egna MCP-server — se
[20-tekniker/mcp.md](../20-tekniker/mcp.md) och
[exempel/mcp/hello-mcp/](../../exempel/mcp/hello-mcp/).

## Varför det spelar roll för vårt arbete

De flesta diskussioner om "AI för utvecklare" handlar om vilken modell som är bäst.
Det här är ett konkret motexempel: allt som gör verktygen användbara här —
konfigurationen, nyckelhanteringen, MCP-kopplingen, integrationen i editorn — är
**plattformsarbete**, inte modellarbete. Ingen enskild utvecklare hade behövt göra
något av det.

Det är samma sorts arbete som skiljer en PoC från något i produktion. Att det redan
är gjort åt oss här är värt att titta närmare på när vi ska beskriva vad steget
kräver — se [50-fran-poc-till-produktion/](../50-fran-poc-till-produktion/).

## Andra verktyg värda att jämföra med

Se [20-tekniker/agentupplagg.md](../20-tekniker/agentupplagg.md) och
[20-tekniker/kodagenter.md](../20-tekniker/kodagenter.md). De förinstallerade
verktygen är en utgångspunkt, inte ett facit — och att jämföra dem mot alternativ
är ett av de billigaste experiment vi kan göra.

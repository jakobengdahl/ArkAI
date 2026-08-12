---
namn: mcp-sdk-2-bytte-api
beskrivning: MCP:s Python-SDK bytte API i 2.0 — FastMCP heter MCPServer och nästan alla exempel på nätet är skrivna mot 1.x.
typ: verktyg
uppdaterad: 2026-08-12
---

I `mcp` 2.0 finns inte `mcp.server.fastmcp` längre:

```python
from mcp.server.fastmcp import FastMCP      # 1.x — ModuleNotFoundError
from mcp.server.mcpserver import MCPServer  # 2.x
```

Dekoratorn `@mcp.tool()` fungerar likadant. Klientsidan har dessutom gått från
camelCase till snake_case: `init.server_info`, `tool.input_schema`.

**Varför:** första försöket att bygga en MCP-server följde ett exempel från nätet och
föll direkt på importen. Felet ser ut som ett installationsproblem
(`ModuleNotFoundError: No module named 'mcp.server.fastmcp'`) men är en API-ändring.
Eftersom `FastMCP` var det etablerade namnet i ett par år är i princip allt
exempelmaterial som går att googla skrivet mot 1.x.

**Så använder du det:** kontrollera versionen innan du felsöker vidare, och läs API:t
i den installerade paketet i stället för i ett blogginlägg:

```bash
python -c "import importlib.metadata as m; print(m.version('mcp'))"
python -c "import mcp.server.mcpserver as m; print([x for x in dir(m) if not x.startswith('_')])"
```

Fungerande exempel att utgå från: [exempel/mcp/hello-mcp/](../../exempel/mcp/hello-mcp/).

Relaterat: [[index-fore-innehall]]

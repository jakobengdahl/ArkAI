#!/usr/bin/env python3
"""Förkonfigurerar Open WebUI: modellkopplingen och verktygsservrarna.

    verktyg/konfigurera-openwebui.py --visa     # vad som skulle sättas
    verktyg/konfigurera-openwebui.py --env      # export-rader att köra före första start
    verktyg/konfigurera-openwebui.py --skriv    # skriv in i webui.db

Två vägar in, för Open WebUI läser sin konfiguration på två sätt:

  * **Före första start** finns ingen databas. Då är miljövariabler enda vägen,
    och det är vad --env är till för.
  * **Efteråt vinner databasen.** Värden som en gång hamnat där läses inte om
    från miljön, hur många gånger man än startar om. Därför skriver --skriv
    direkt i databasen — det är det som gör att en ändrad hemlighet eller en
    nyinstallerad MCP-server slår igenom utan att man rensar sin data.

Uppgifterna kommer ur miljön (Vault-hemligheten) och ur ~/work/.labb/mcp.json.
Ingenting av det här hör hemma i repot.
"""

from __future__ import annotations

import json
import os
import shlex
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import labb  # noqa: E402

# Nycklarna Open WebUI använder i tabellen "config". Verifierade mot
# open_webui/config.py — de har bytt namn förr och kan göra det igen.
NYCKLAR = {
    "openai_pa": "openai.enable",
    "baser": "openai.api_base_urls",
    "nycklar": "openai.api_keys",
    "standardmodell": "ui.default_models",
    "verktyg": "tool_server.connections",
}


def datakatalog() -> Path:
    return Path(os.environ.get("DATA_DIR") or Path.home() / "work" / "open-webui-data")


def databas() -> Path:
    return datakatalog() / "webui.db"


def modellkoppling() -> dict | None:
    """Modellen ur miljön, eller None om hemligheten inte är monterad."""
    nyckel = os.environ.get("OPENAI_API_KEY", "").strip()
    bas = (os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE_URL") or "").strip()
    if not nyckel or not bas:
        return None
    return {"bas": bas.rstrip("/"), "nyckel": nyckel, "modell": os.environ.get("OPENAI_MODEL", "").strip()}


def verktygsservrar() -> list[dict]:
    """En verktygsserver per MCP-server som bryggan exponerar.

    mcpo monterar varje server ur mcp.json under sitt eget namn. Vi läser
    samma fil, så listan speglar det som faktiskt är installerat.
    """
    port = int(os.environ.get("MCPO_PORT", "8083"))
    fil = labb.LABB / "mcp.json"
    if not fil.exists():
        return []
    try:
        servrar = json.loads(fil.read_text()).get("mcpServers", {})
    except (json.JSONDecodeError, OSError):
        return []
    return [
        {
            "url": f"http://127.0.0.1:{port}/{namn}",
            "path": "openapi.json",
            "type": "openapi",
            # Bryggan kör utan nyckel på loopback. "none" betyder att Open WebUI
            # inte skickar någon Authorization-header alls.
            "auth_type": "none",
            "key": "",
            "config": {"enable": True},
            "info": {"name": namn, "description": f"MCP-servern {namn} via bryggan"},
        }
        for namn in sorted(servrar)
    ]


def _vara_urler(servrar: list[dict]) -> set[str]:
    return {s["url"] for s in servrar}


def onskat_lage() -> dict:
    """Det vi vill att Open WebUI ska ha, oavsett hur det skrivs dit."""
    lage: dict = {}
    m = modellkoppling()
    if m:
        lage[NYCKLAR["openai_pa"]] = True
        lage[NYCKLAR["baser"]] = [m["bas"]]
        lage[NYCKLAR["nycklar"]] = [m["nyckel"]]
        if m["modell"]:
            lage[NYCKLAR["standardmodell"]] = m["modell"]
    v = verktygsservrar()
    if v:
        lage[NYCKLAR["verktyg"]] = v
    return lage


# ── Utskrift ──────────────────────────────────────────────────────────────


def _doldt(varde) -> str:
    s = json.dumps(varde, ensure_ascii=False) if not isinstance(varde, str) else varde
    return s if len(s) <= 8 else s[:4] + "…" + s[-2:]


def visa() -> int:
    m = modellkoppling()
    v = verktygsservrar()
    print(f"Databas: {databas()}{'' if databas().exists() else '  (finns inte än)'}")
    print()
    if m:
        print("Modellkoppling")
        print(f"  bas-URL   {m['bas']}")
        print(f"  nyckel    {_doldt(m['nyckel'])}")
        print(f"  modell    {m['modell'] or '(ingen förvald)'}")
    else:
        print("Modellkoppling: hoppas över — OPENAI_API_KEY och OPENAI_BASE_URL saknas i miljön.")
        print("  De kommer ur Vault-hemligheten. Se docs/60-miljo/starta-labbet.md.")
    print()
    if v:
        print(f"Verktygsservrar ({len(v)})")
        for s in v:
            print(f"  {s['info']['name']:<16} {s['url']}/{s['path']}")
    else:
        print("Verktygsservrar: inga — ingen MCP-server är installerad än.")
    return 0


def env_rader() -> int:
    """Rader att eval:a i skalet före första start."""
    m = modellkoppling()
    if m:
        print(f"export ENABLE_OPENAI_API=True")
        print(f"export OPENAI_API_BASE_URL={shlex.quote(m['bas'])}")
        print(f"export OPENAI_API_KEY={shlex.quote(m['nyckel'])}")
        if m["modell"]:
            print(f"export DEFAULT_MODELS={shlex.quote(m['modell'])}")
    v = verktygsservrar()
    if v:
        print(f"export TOOL_SERVER_CONNECTIONS={shlex.quote(json.dumps(v, ensure_ascii=False))}")
    return 0


# ── Skrivning ─────────────────────────────────────────────────────────────


def skriv() -> int:
    db = databas()
    if not db.exists():
        print(f"Ingen databas i {db}.", file=sys.stderr)
        print("Open WebUI har inte startat än. Starta den först — startskriptet", file=sys.stderr)
        print("sätter samma sak via miljövariabler den första gången.", file=sys.stderr)
        return 1

    lage = onskat_lage()
    if not lage:
        print("Ingenting att skriva: varken hemlighet eller MCP-server finns.")
        return 0

    ny = dict(lage)
    with sqlite3.connect(db) as anslutning:
        anslutning.execute(
            "CREATE TABLE IF NOT EXISTS config "
            "(key TEXT PRIMARY KEY, value JSON NOT NULL, updated_at BIGINT)"
        )
        # Verktygsservrar slås ihop i stället för att skrivas över: någon kan ha
        # lagt till en egen i gränssnittet, och den ska inte försvinna för att
        # vi trycker på en knapp.
        if NYCKLAR["verktyg"] in ny:
            rad = anslutning.execute(
                "SELECT value FROM config WHERE key = ?", (NYCKLAR["verktyg"],)
            ).fetchone()
            befintliga = []
            if rad:
                try:
                    befintliga = json.loads(rad[0]) or []
                except (json.JSONDecodeError, TypeError):
                    befintliga = []
            vara = _vara_urler(ny[NYCKLAR["verktyg"]])
            andras = [s for s in befintliga if isinstance(s, dict) and s.get("url") not in vara]
            ny[NYCKLAR["verktyg"]] = andras + ny[NYCKLAR["verktyg"]]

        nu = int(time.time())
        for nyckel, varde in ny.items():
            anslutning.execute(
                "INSERT INTO config (key, value, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
                (nyckel, json.dumps(varde, ensure_ascii=False), nu),
            )

    for nyckel in ny:
        if nyckel == NYCKLAR["nycklar"]:
            print(f"  {nyckel} = {_doldt(ny[nyckel][0])}")
        elif nyckel == NYCKLAR["verktyg"]:
            print(f"  {nyckel} = {len(ny[nyckel])} server(rar)")
        else:
            print(f"  {nyckel} = {json.dumps(ny[nyckel], ensure_ascii=False)}")
    print()
    print("Skrivet. Kör Open WebUI redan syns modellen direkt; verktygen dyker upp")
    print("under Inställningar → Verktyg. Ladda om fliken om något dröjer.")
    return 0


def main(argv: list[str]) -> int:
    val = argv[0] if argv else "--visa"
    match val:
        case "--visa":
            return visa()
        case "--env":
            return env_rader()
        case "--skriv":
            return skriv()
        case _:
            print(__doc__)
            return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

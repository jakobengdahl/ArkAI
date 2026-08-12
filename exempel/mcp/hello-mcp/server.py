"""En minimal MCP-server som exponerar minnesbanken i det här repot.

Servern gör tre saker, som motsvarar det mönster nästan alla nyttiga MCP-servrar
följer:

    lista_minnen()  – ge modellen en billig överblick (indexet)
    las_minne(namn) – hämta en enskild post när den behövs
    sok_minnen(ord) – hitta rätt post att hämta

Det är samma "index före innehåll"-princip som minnesbanken själv bygger på:
modellen ska veta *vad som finns* utan att behöva ha allt i kontexten.

Kör:
    uv run server.py            # stdio, det klienter förväntar sig
    uv run server.py --lista    # snabbtest utan MCP-klient
"""

from __future__ import annotations

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

# Repots rot, räknat från den här filens plats.
REPO = Path(__file__).resolve().parents[3]
MINNESBANK = REPO / "minnesbank"

# OBS: MCP:s Python-SDK bytte API i 2.0 — den äldre `FastMCP` heter nu `MCPServer`
# och importeras från mcp.server.mcpserver. Exempel du hittar på nätet är ofta
# skrivna mot 1.x. Se README.md.
mcp = MCPServer("arkai-minnesbank")


def _poster() -> list[Path]:
    """Alla minnesposter, exklusive index och mall."""
    return sorted(
        p
        for p in MINNESBANK.rglob("*.md")
        if p.name not in {"MINNE.md", "README.md"} and not p.name.startswith("MALL-")
    )


def _beskrivning(post: Path) -> str:
    """Plocka ut beskrivningsraden ur frontmatter."""
    for rad in post.read_text(encoding="utf-8").splitlines()[:10]:
        if rad.startswith("beskrivning:"):
            return rad.split(":", 1)[1].strip()
    return ""


# Docstringen är det modellen läser för att avgöra om verktyget ska användas.
# Den är alltså en del av prompten — skriv den för en läsare som ska välja verktyg,
# inte för en utvecklare som ska underhålla koden.


@mcp.tool()
def lista_minnen() -> str:
    """Lista alla poster i den delade minnesbanken med namn och beskrivning.

    Använd det här först för att se vad som finns. Det är billigt. Hämta sedan
    enskilda poster med las_minne när du vet vilken du behöver.
    """
    if not MINNESBANK.is_dir():
        return f"Hittar ingen minnesbank i {MINNESBANK}"

    rader = []
    for post in _poster():
        kategori = post.parent.name
        rader.append(f"- {post.stem} [{kategori}] — {_beskrivning(post)}")

    if not rader:
        return "Minnesbanken är tom."
    return "\n".join(rader)


@mcp.tool()
def las_minne(namn: str) -> str:
    """Läs en enskild minnespost i sin helhet.

    Argument:
        namn: postens namn utan .md, t.ex. "onyxia-port-8080-upptagen".
              Använd lista_minnen eller sok_minnen för att hitta namn.
    """
    träffar = [p for p in _poster() if p.stem == namn]
    if not träffar:
        return f"Ingen post heter '{namn}'. Kör lista_minnen för att se vad som finns."
    return träffar[0].read_text(encoding="utf-8")


@mcp.tool()
def sok_minnen(sokord: str) -> str:
    """Sök i minnesbanken på fritext och få tillbaka de poster som matchar.

    Enkel delsträngssökning i namn och innehåll — ingen semantisk sökning.
    Argument:
        sokord: ett eller flera ord, t.ex. "port" eller "token".
    """
    ord = sokord.lower().strip()
    if not ord:
        return "Ange ett sökord."

    träffar = []
    for post in _poster():
        innehall = post.read_text(encoding="utf-8").lower()
        if ord in post.stem.lower() or ord in innehall:
            träffar.append(f"- {post.stem} — {_beskrivning(post)}")

    if not träffar:
        return f"Inga träffar på '{sokord}'. Kör lista_minnen för att se allt."
    return "\n".join(träffar)


if __name__ == "__main__":
    if "--lista" in sys.argv:
        # Snabbtest utan MCP-klient — anropar funktionerna direkt.
        print(f"Minnesbank: {MINNESBANK}\n")
        print(lista_minnen())
    else:
        mcp.run()

#!/usr/bin/env python3
"""Lägger upp en av labbets MCP-servrar som verktygsserver i Eneo.

    verktyg/koppla-mcp-till-eneo.py hello-mcp        # visar vad som skulle sättas
    verktyg/koppla-mcp-till-eneo.py hello-mcp --skriv

Eneo har inga verktyg från början. Adminen lägger upp MCP-servrar per
organisation, och därefter kan varje assistent välja vilka av deras verktyg den
får använda. Det är den enda vägen — Eneo har ingen inbyggd verktygslåda.

**Eneo stödjer bara Streamable HTTP.** Inte stdio, inte SSE. En stdio-server
måste alltså köras över HTTP för att gå att koppla in, och den hamnar då på ett
publikt värdnamn och behöver en token. Se docs/60-miljo/eneo.md.

Vad som ska kopplas in står i verktyg/labb.toml, inte här:

    mcp_http_intern_url  adress inne i namnrymden (Service-DNS), för en server
                       som kör som egen arbetslast. Provas först — då slipper
                       trafiken gå ut via ingressen. Svarar den inte för Eneo
                       provas ingressen för mcp_http_port, om den finns
    mcp_http_port      porten servern kör på i den här podden — URL:en hämtas
                       ur ingressen, för det är den adressen Eneo kan nå
    mcp_http_url_env   för en server som kör någon annanstans: miljövariabeln
                       med dess adress. Bara värdnamnet används
    mcp_http_sokvag    sökvägen till Streamable HTTP-slutpunkten
    mcp_http_token_fil fil under ~/work/.labb med token
    token_env          eller miljövariabeln med token
"""

from __future__ import annotations

import os
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eneo_api as api  # noqa: E402
import labb  # noqa: E402


def adresser(tjid: str, t: dict) -> list[str]:
    """URL:erna att pröva, i ordning. Den interna först, om den finns."""
    if not t.get("mcp_http_intern_url"):
        return [adress(tjid, t)]
    lista = [t["mcp_http_intern_url"]]
    if t.get("mcp_http_port"):
        url = labb.egen_ingress_for(int(t["mcp_http_port"]))
        if url:
            lista.append(url.rstrip("/") + t.get("mcp_http_sokvag", "/mcp"))
    return lista


def adress(tjid: str, t: dict) -> str:
    """URL:en Eneo ska anropa. Eneo kör i en annan podd — 127.0.0.1 duger inte."""
    sokvag = t.get("mcp_http_sokvag", "/mcp")
    if t.get("mcp_http_url_env"):
        bas = os.environ.get(t["mcp_http_url_env"], "").strip()
        if not bas:
            api.fel(f"{t['mcp_http_url_env']} saknas i miljön.",
                    "Lägg den i miljöns Vault-hemlighet — se docs/60-miljo/starta-labbet.md.")
        # Bara värdnamnet: variabeln pekar på webbgränssnittet, MCP-slutpunkten
        # ligger på egen sökväg i roten.
        delar = urllib.parse.urlsplit(bas)
        return f"{delar.scheme}://{delar.netloc}{sokvag}"
    if t.get("mcp_http_port"):
        url = labb.egen_ingress_for(int(t["mcp_http_port"]))
        if not url:
            api.fel(
                f"Port {t['mcp_http_port']} är inte exponerad i den här tjänsten.",
                "Eneo kör i en annan podd och når bara servern via ingressen.",
                "Portar exponeras när tjänsten startar — se docs/60-miljo/starta-labbet.md.",
            )
        return url.rstrip("/") + sokvag
    api.fel(f"{tjid} saknar mcp_http_port eller mcp_http_url_env i verktyg/labb.toml.")
    return ""


def token(t: dict) -> str:
    if t.get("mcp_http_token_fil"):
        fil = labb.LABB / t["mcp_http_token_fil"]
        if not fil.is_file():
            api.fel(f"Hittar ingen token i {fil}.",
                    "Starta servern en gång — den skapar filen.")
        return fil.read_text().strip()
    if t.get("token_env"):
        return os.environ.get(t["token_env"], "").strip()
    return ""


def skriv(namn: str, url: str, hemlig: str, beskrivning: str) -> int:
    tok = api.logga_in()
    kropp = {
        "name": namn,
        "http_url": url,
        "description": beskrivning,
        "http_auth_type": "bearer" if hemlig else "none",
        "tags": ["labbet"],
    }
    if hemlig:
        kropp["http_auth_config_schema"] = {"token": hemlig}

    for post in api.poster(api.anrop("/api/v1/mcp-servers/", tok)):
        if post.get("name") == namn:
            svar = api.anrop(f"/api/v1/mcp-servers/{post['id']}/", tok, data=kropp)
            if "_fel" in svar:
                print(f"  {namn}: kunde inte uppdateras — {svar['_fel']} {svar['_text']}")
                return 1
            print(f"  {namn}: fanns, adress och token uppdaterade")
            # En uppdatering svarar inte med anslutningsstatus. Fråga efter
            # verktygen i stället — det är ändå det som avgör om den duger.
            verktyg = api.poster(api.anrop(f"/api/v1/mcp-servers/{post['id']}/tools/", tok))
            print(f"  {namn}: {len(verktyg)} verktyg")
            return 0 if verktyg else 1

    svar = api.anrop("/api/v1/mcp-servers/", tok, data=kropp)
    if "_fel" in svar:
        print(f"  {namn}: kunde inte läggas upp — {svar['_fel']} {svar['_text']}")
        return 1
    anslutning = svar.get("connection", {})
    if not anslutning.get("success"):
        print(f"  {namn}: upplagd, men Eneo nådde den inte — "
              f"{anslutning.get('error_message') or 'okänt fel'}")
        return 1
    print(f"  {namn}: upplagd, {anslutning.get('tools_discovered', 0)} verktyg hittade")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    tjid = sys.argv[1]
    if tjid not in labb.tjanster():
        api.fel(f"Okänd tjänst: {tjid}")
    t = labb.tjanst(tjid)
    namn = t.get("namn", tjid)
    urler = adresser(tjid, t)
    hemlig = token(t)

    print(f"MCP-server : {namn}")
    print(f"Adress     : {urler[0]}")
    for reserv in urler[1:]:
        print(f"  reserv   : {reserv}")
    print(f"Token      : {'ja' if hemlig else 'nej — servern är öppen'}")
    print(f"Eneo       : {api.BAS}")
    if "--skriv" not in sys.argv:
        print("\nInget skrivet. Kör med --skriv för att lägga in det i Eneo.")
        return 0
    print()
    kod = 1
    for i, url in enumerate(urler):
        if i:
            print(f"  provar i stället {url}")
        kod = skriv(namn, url, hemlig, t.get("beskrivning", ""))
        if kod == 0:
            break
    return kod


if __name__ == "__main__":
    sys.exit(main())

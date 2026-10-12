#!/usr/bin/env python3
"""Kopplar in plattformens modeller i Eneo.

    verktyg/konfigurera-eneo.py --visa      # vad som skulle sättas
    verktyg/konfigurera-eneo.py --skriv     # skriv in i Eneo

Eneo läser inte modellnycklar ur miljön på det sätt Open WebUI gör. Modeller
läggs upp per organisation: först en *leverantör* med bas-URL och nyckel, sedan
de modeller man vill kunna välja. Nyckeln krypteras med ENCRYPTION_KEY och
hamnar i Eneos egen databas.

Det går att göra i admingränssnittet. Det här skriptet gör samma sak mot API:et,
av samma skäl som konfigurera-openwebui.py finns: en installation som kräver
sexton klick i ett formulär är inte reproducerbar, och nyckeln ska inte behöva
klistras in för hand.

Uppgifterna kommer ur miljön (Vault-hemligheten):

    OPENAI_BASE_URL   https://llm.lab.sspcloud.fr/api
    OPENAI_API_KEY    din personliga nyckel
    OPENAI_MODEL      standardmodellen, om du vill ha en annan än den första
                      i listan

Vilka modeller som läggs upp står i verktyg/labb.toml under [tjanst.eneo]:
`modeller` (chatt, den första blir standard) och `embedding_modell`. Det är
samma lista för alla som installerar labbet — modeller som plattformen inte
har just nu hoppas över med en rad i loggen.

Inloggningen som admin hämtas ur Kubernetes: e-posten ur eneo-backend-konfig,
lösenordet ur eneo-hemligheter. Har du bytt lösenord i gränssnittet — sätt
ENEO_ADMIN_LOSEN.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eneo_api as api  # noqa: E402
from eneo_api import anrop, fel, logga_in, poster  # noqa: E402

LEVERANTOR = "SSP Cloud"

# Eneo behöver veta hur långt sammanhang modellen klarar — den trunkerar
# själv innan den frågar. Plattformens modellista (/models) säger ingenting om
# det, men vLLM bakom den gör det: en fråga om fler utdatatokens än modellen
# klarar avvisas med "max_tokens=… cannot be greater than max_model_len=N".
# Gränsen gäller in- och utdata tillsammans, så indata blir N minus utdata.
# Svarar plattformen inte på frågan används reservvärdet, som är försiktigt.
MAX_UT = int(os.environ.get("ENEO_MAX_OUTPUT", "8192"))
RESERV_KONTEXT = 32768


# ── Plattformens sida ─────────────────────────────────────────────────────


def modellkoppling() -> dict:
    nyckel = os.environ.get("OPENAI_API_KEY", "").strip()
    bas = (os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE_URL") or "").strip()
    if not nyckel or not bas:
        fel(
            "OPENAI_API_KEY och OPENAI_BASE_URL saknas i miljön.",
            "Lägg dem i miljöns Vault-hemlighet — se docs/60-miljo/starta-labbet.md.",
        )
    return {"bas": bas.rstrip("/"), "nyckel": nyckel}


def plattformens_modeller(koppling: dict) -> list[str]:
    beg = urllib.request.Request(
        koppling["bas"] + "/models",
        headers={"Authorization": "Bearer " + koppling["nyckel"]},
    )
    with urllib.request.urlopen(beg, timeout=15) as svar:
        return [m["id"] for m in json.load(svar).get("data", [])]


def kontextlangd(koppling: dict, modell: str, embedding: bool = False) -> int | None:
    """Modellens max_model_len enligt plattformen, eller None om den inte gick att läsa.

    Frågan är byggd för att avvisas innan modellen gör något: för chatt en
    orimligt hög max_tokens, för embedding en text längre än någon modell tar.
    Felmeddelandet innehåller gränsen.
    """
    if embedding:
        vag, data = "/embeddings", {"model": modell, "input": "ord " * 300_000}
    else:
        vag, data = "/chat/completions", {
            "model": modell, "max_tokens": 1_000_000_000, "stream": False,
            "messages": [{"role": "user", "content": "hej"}],
        }
    beg = urllib.request.Request(
        koppling["bas"] + vag, data=json.dumps(data).encode(),
        headers={"Authorization": "Bearer " + koppling["nyckel"],
                 "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(beg, timeout=60) as svar:
            text = svar.read().decode(errors="replace")
    except urllib.error.HTTPError as svar:
        text = svar.read().decode(errors="replace")
    except (TimeoutError, OSError):
        return None
    m = (re.search(r"max_model_len=(?:max_total_tokens=)?(\d+)", text)
         or re.search(r"maximum context length is (\d+)", text))
    return int(m.group(1)) if m else None


def tokengranser(koppling: dict, modell: str, embedding: bool = False) -> tuple[int, int]:
    """(max indata, max utdata) att registrera i Eneo. Utdata är 0 för embedding."""
    langd = kontextlangd(koppling, modell, embedding)
    if langd is None:
        print(f"  {modell}: plattformen sa inget om kontextlängden — "
              f"använder reservvärdet {RESERV_KONTEXT}")
        langd = RESERV_KONTEXT
    if embedding:
        return langd, 0
    ut = min(MAX_UT, langd // 4)
    return int(os.environ.get("ENEO_MAX_INPUT", "0")) or langd - ut, ut


def valj_modeller(ider: list[str]) -> tuple[list[str], str | None]:
    """(chattmodeller, embeddingmodell). Den första chattmodellen blir standard."""
    import labb  # noqa: PLC0415
    t = labb.tjanst("eneo")
    onskade = list(t.get("modeller") or [])
    if not onskade:
        chatt, emb = _gissa_modeller(ider)
        return ([chatt] if chatt else []), emb
    saknas = [m for m in onskade if m not in ider]
    for m in saknas:
        print(f"  {m}: finns inte hos plattformen just nu — hoppas över")
    chatt = [m for m in onskade if m in ider]
    standard = os.environ.get("OPENAI_MODEL", "").strip()
    if standard in chatt:
        chatt.remove(standard)
        chatt.insert(0, standard)
    emb = t.get("embedding_modell")
    if emb and emb not in ider:
        print(f"  {emb}: finns inte hos plattformen just nu — hoppas över")
        emb = None
    return chatt, emb or _gissa_modeller(ider)[1]


def _gissa_modeller(ider: list[str]) -> tuple[str | None, str | None]:
    """(chattmodell, embeddingmodell) ur plattformens lista.

    Chattmodellen tas ur OPENAI_MODEL när den är satt — det är samma val som
    Open WebUI får, så jämförelsen mellan plattformarna görs på samma modell.
    Embeddingmodellen känns igen på namnet; något bättre finns inte att gå på
    i ett OpenAI-kompatibelt /models-svar.
    """
    embedding = next((i for i in ider if "embed" in i.lower()), None)
    chatt = os.environ.get("OPENAI_MODEL", "").strip() or None
    if chatt and chatt not in ider:
        fel(f"OPENAI_MODEL={chatt} finns inte hos {os.environ.get('OPENAI_BASE_URL')}.",
            "Modeller just nu: " + ", ".join(ider))
    if not chatt:
        chatt = next((i for i in ider if i != embedding), None)
    return chatt, embedding


# ── Eneos sida ────────────────────────────────────────────────────────────


def leverantor(token: str, koppling: dict) -> str:
    """Leverantörens id. Skapas om den saknas, annars uppdateras nyckeln."""
    for p in poster(anrop("/api/v1/admin/model-providers/", token)):
        if p.get("name") == LEVERANTOR:
            anrop(f"/api/v1/admin/model-providers/{p['id']}/", token, metod="PUT", data={
                "credentials": {"api_key": koppling["nyckel"]},
                "config": {"endpoint": koppling["bas"]},
                "is_active": True,
            })
            print(f"  leverantör {LEVERANTOR}: fanns, nyckel och bas-URL uppdaterade")
            return p["id"]
    ny = anrop("/api/v1/admin/model-providers/", token, data={
        "name": LEVERANTOR,
        "provider_type": "openai",
        "credentials": {"api_key": koppling["nyckel"]},
        "config": {"endpoint": koppling["bas"]},
        "is_active": True,
    })
    if "_fel" in ny:
        fel(f"Kunde inte lägga upp leverantören: {ny['_fel']} {ny['_text']}")
    print(f"  leverantör {LEVERANTOR}: upplagd mot {koppling['bas']}")
    return ny["id"]


def redan_upplagd(token: str, vag: str, namn: str) -> dict | None:
    return next((m for m in poster(anrop(vag, token)) if m.get("name") == namn), None)


def validera(token: str, lev: str, namn: str, typ: str) -> None:
    # Kontrollen är en provfråga till modellen. En kall modell hos plattformen
    # kan ta över en minut — det är inte ett fel i kopplingen, som redan är
    # gjord, så det ska inte få hela steget att misslyckas.
    try:
        svar = anrop(f"/api/v1/admin/model-providers/{lev}/validate-model/", token,
                     data={"model_name": namn, "model_type": typ})
    except (TimeoutError, OSError) as fel_:
        print(f"  {namn}: svarade inte inom tidsgränsen ({fel_}) — upplagd ändå, prova i Eneo")
        return
    if svar.get("success"):
        print(f"  {namn}: svarar ({typ})")
    else:
        print(f"  {namn}: FEL — {svar.get('error') or svar.get('_text')}")


def skriv(koppling: dict, chattmodeller: list[str], embedding: str | None) -> None:
    token = logga_in()
    lev = leverantor(token, koppling)

    for nr, chatt in enumerate(chattmodeller):
        max_in, max_ut = tokengranser(koppling, chatt)
        granser = f"{max_in} in / {max_ut} ut"
        fanns = redan_upplagd(token, "/api/v1/completion-models/", chatt)
        if fanns:
            # Modeller som lades upp av en äldre version av skriptet fick fasta
            # gränser. Rätta dem, men rör inget annat som någon kan ha ändrat.
            if (fanns.get("max_input_tokens"), fanns.get("max_output_tokens")) == (max_in, max_ut):
                print(f"  chattmodell {chatt}: fanns redan ({granser})")
                continue
            svar = anrop(f"/api/v1/admin/tenant-models/completion/{fanns['id']}/", token,
                         metod="PUT", data={"max_input_tokens": max_in,
                                            "max_output_tokens": max_ut})
            print(f"  chattmodell {chatt}: " + (
                f"fanns, gränserna ändrade från {fanns.get('max_input_tokens')} in / "
                f"{fanns.get('max_output_tokens')} ut till {granser}" if "_fel" not in svar
                else f"FEL {svar['_fel']} {svar['_text']}"))
            continue
        svar = anrop("/api/v1/admin/tenant-models/completion/", token, data={
            "provider_id": lev, "name": chatt, "display_name": chatt,
            "max_input_tokens": max_in, "max_output_tokens": max_ut,
            "supports_tool_calling": True, "hosting": "eu", "family": "openai",
            "is_active": True, "is_default": nr == 0,
        })
        print(f"  chattmodell {chatt}: " + (f"upplagd ({granser})" if "_fel" not in svar
                                            else f"FEL {svar['_fel']} {svar['_text']}"))

    if embedding:
        max_in, _ = tokengranser(koppling, embedding, embedding=True)
        fanns = redan_upplagd(token, "/api/v1/embedding-models/", embedding)
        if fanns and fanns.get("max_input") == max_in:
            print(f"  embeddingmodell {embedding}: fanns redan ({max_in} in)")
        elif fanns:
            svar = anrop(f"/api/v1/admin/tenant-models/embedding/{fanns['id']}/", token,
                         metod="PUT", data={"max_input": max_in})
            print(f"  embeddingmodell {embedding}: " + (
                f"fanns, max indata ändrad från {fanns.get('max_input')} till {max_in}"
                if "_fel" not in svar else f"FEL {svar['_fel']} {svar['_text']}"))
        else:
            svar = anrop("/api/v1/admin/tenant-models/embedding/", token, data={
                "provider_id": lev, "name": embedding, "display_name": embedding,
                "max_input": max_in,
                "hosting": "eu", "family": "openai", "is_active": True, "is_default": True,
            })
            print(f"  embeddingmodell {embedding}: " + (f"upplagd ({max_in} in)" if "_fel" not in svar
                                                        else f"FEL {svar['_fel']} {svar['_text']}"))

    print("Kontrollerar att modellerna verkligen svarar:")
    for chatt in chattmodeller:
        validera(token, lev, chatt, "completion")
    if embedding:
        validera(token, lev, embedding, "embedding")


def main() -> None:
    lage = sys.argv[1] if len(sys.argv) > 1 else "--visa"
    koppling = modellkoppling()
    ider = plattformens_modeller(koppling)
    chatt, embedding = valj_modeller(ider)

    print(f"Leverantör : {LEVERANTOR} → {koppling['bas']}")
    print(f"Chatt      : {', '.join(chatt) or '(ingen hittad)'}")
    print(f"Embedding  : {embedding or '(ingen hittad)'}")
    print(f"Eneo       : {api.BAS}")
    if lage != "--skriv":
        print("\nTokengränser enligt plattformen:")
        for c in chatt:
            max_in, max_ut = tokengranser(koppling, c)
            print(f"  {c}: {max_in} in / {max_ut} ut")
        if embedding:
            print(f"  {embedding}: {tokengranser(koppling, embedding, embedding=True)[0]} in")
        print("\nInget skrivet. Kör med --skriv för att lägga in det i Eneo.")
        return
    print()
    skriv(koppling, chatt, embedding)


if __name__ == "__main__":
    main()

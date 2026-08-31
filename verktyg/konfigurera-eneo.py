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
    OPENAI_MODEL      chattmodellen, om du vill ha en annan än standardvalet

Inloggningen som admin hämtas ur Kubernetes: e-posten ur eneo-backend-konfig,
lösenordet ur eneo-hemligheter. Har du bytt lösenord i gränssnittet — sätt
ENEO_ADMIN_LOSEN.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eneo_api as api  # noqa: E402
from eneo_api import anrop, fel, logga_in, poster  # noqa: E402

LEVERANTOR = "SSP Cloud"

# Eneo behöver veta hur långt sammanhang modellen klarar — den trunkerar
# själv innan den frågar. Plattformens modellista säger ingenting om det, så
# värdena är satta av oss och medvetet försiktiga.
MAX_IN = int(os.environ.get("ENEO_MAX_INPUT", "32768"))
MAX_UT = int(os.environ.get("ENEO_MAX_OUTPUT", "4096"))


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


def valj_modeller(ider: list[str]) -> tuple[str | None, str | None]:
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


def redan_upplagd(token: str, vag: str, namn: str) -> bool:
    return any(m.get("name") == namn for m in poster(anrop(vag, token)))


def validera(token: str, lev: str, namn: str, typ: str) -> None:
    svar = anrop(f"/api/v1/admin/model-providers/{lev}/validate-model/", token,
                 data={"model_name": namn, "model_type": typ})
    if svar.get("success"):
        print(f"  {namn}: svarar ({typ})")
    else:
        print(f"  {namn}: FEL — {svar.get('error') or svar.get('_text')}")


def skriv(koppling: dict, chatt: str, embedding: str | None) -> None:
    token = logga_in()
    lev = leverantor(token, koppling)

    if chatt and not redan_upplagd(token, "/api/v1/completion-models/", chatt):
        svar = anrop("/api/v1/admin/tenant-models/completion/", token, data={
            "provider_id": lev, "name": chatt, "display_name": chatt,
            "max_input_tokens": MAX_IN, "max_output_tokens": MAX_UT,
            "supports_tool_calling": True, "hosting": "eu", "family": "openai",
            "is_active": True, "is_default": True,
        })
        print(f"  chattmodell {chatt}: " + ("upplagd" if "_fel" not in svar
                                            else f"FEL {svar['_fel']} {svar['_text']}"))
    elif chatt:
        print(f"  chattmodell {chatt}: fanns redan")

    if embedding and not redan_upplagd(token, "/api/v1/embedding-models/", embedding):
        svar = anrop("/api/v1/admin/tenant-models/embedding/", token, data={
            "provider_id": lev, "name": embedding, "display_name": embedding,
            "hosting": "eu", "family": "openai", "is_active": True, "is_default": True,
        })
        print(f"  embeddingmodell {embedding}: " + ("upplagd" if "_fel" not in svar
                                                    else f"FEL {svar['_fel']} {svar['_text']}"))
    elif embedding:
        print(f"  embeddingmodell {embedding}: fanns redan")

    print("Kontrollerar att modellerna verkligen svarar:")
    if chatt:
        validera(token, lev, chatt, "completion")
    if embedding:
        validera(token, lev, embedding, "embedding")


def main() -> None:
    lage = sys.argv[1] if len(sys.argv) > 1 else "--visa"
    koppling = modellkoppling()
    ider = plattformens_modeller(koppling)
    chatt, embedding = valj_modeller(ider)

    print(f"Leverantör : {LEVERANTOR} → {koppling['bas']}")
    print(f"Chatt      : {chatt}")
    print(f"Embedding  : {embedding or '(ingen hittad)'}")
    print(f"Eneo       : {api.BAS}")
    if lage != "--skriv":
        print("\nInget skrivet. Kör med --skriv för att lägga in det i Eneo.")
        return
    print()
    skriv(koppling, chatt, embedding)


if __name__ == "__main__":
    main()

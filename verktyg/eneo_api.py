"""Det minsta som behövs för att prata med Eneos API från labbet.

Finns för att två skript gör det — verktyg/konfigurera-eneo.py lägger upp
modellerna, verktyg/koppla-mcp-till-eneo.py lägger upp verktygsservrarna — och
inloggningen är samma sak båda gångerna.

Bara standardbiblioteket, av samma skäl som labb.py: modulen ska gå att
importera innan något är installerat.

Inloggningen hämtas ur Kubernetes: e-posten ur configmap:en
`eneo-backend-konfig`, lösenordet ur secret:en `eneo-hemligheter`. Har du bytt
lösenord i gränssnittet — sätt `ENEO_ADMIN_LOSEN`.
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

BAS = os.environ.get("ENEO_BAS_URL", "http://127.0.0.1:8084").rstrip("/")


def fel(*rader: str) -> None:
    for rad in rader:
        print(rad, file=sys.stderr)
    sys.exit(1)


def _kubectl(*arg: str) -> str:
    try:
        ute = subprocess.run(["kubectl", *arg], capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return ""
    return ute.stdout.strip() if ute.returncode == 0 else ""


def hemlighet(nyckel: str) -> str:
    rå = _kubectl("get", "secret", "eneo-hemligheter", "-o", f"jsonpath={{.data.{nyckel}}}")
    if not rå:
        return ""
    try:
        return base64.b64decode(rå).decode()
    except ValueError:
        return ""


def standardepost() -> str:
    return _kubectl("get", "configmap", "eneo-backend-konfig",
                    "-o", "jsonpath={.data.DEFAULT_USER_EMAIL}")


def anrop(vag: str, token: str | None = None, data: dict | None = None,
          metod: str | None = None, timeout: float = 90) -> dict:
    """Ett API-anrop. Fel returneras som {"_fel": kod, "_text": …}, inte som avbrott.

    Skälen står i anropsställena: den som lägger upp en modell vill kunna säga
    *vad* som gick fel i sin egen logg, inte få ett spårutdrag.
    """
    kropp = json.dumps(data).encode() if data is not None else None
    beg = urllib.request.Request(BAS + vag, data=kropp,
                                 method=metod or ("POST" if data else "GET"))
    beg.add_header("Content-Type", "application/json")
    if token:
        beg.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(beg, timeout=timeout) as svar:
            text = svar.read().decode()
            return json.loads(text) if text else {"_ok": svar.status}
    except urllib.error.HTTPError as e:
        return {"_fel": e.code, "_text": e.read().decode()[:400]}
    except urllib.error.URLError as e:
        return {"_fel": 0, "_text": str(e)}


def poster(svar) -> list:
    """Eneo svarar ibland med en lista, ibland med {"items": [...]}."""
    if isinstance(svar, dict):
        svar = svar.get("items", [])
    return svar if isinstance(svar, list) else []


def logga_in() -> str:
    epost = os.environ.get("ENEO_ADMIN_EPOST") or standardepost()
    losen = os.environ.get("ENEO_ADMIN_LOSEN") or hemlighet("DEFAULT_USER_PASSWORD")
    if not losen:
        fel("Hittade inget adminlösenord i eneo-hemligheter. Sätt ENEO_ADMIN_LOSEN.")
    kropp = urllib.parse.urlencode({"username": epost, "password": losen}).encode()
    beg = urllib.request.Request(BAS + "/api/v1/users/login/token/", data=kropp)
    beg.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(beg, timeout=30) as svar:
            return json.load(svar)["access_token"]
    except urllib.error.HTTPError as e:
        fel(f"Kunde inte logga in som {epost} ({e.code}).",
            "Har du bytt lösenord i gränssnittet? Sätt ENEO_ADMIN_LOSEN.")
    except urllib.error.URLError as e:
        fel(f"Nådde inte Eneo på {BAS}: {e}", "Kör: verktyg/kor.sh starta eneo")
    return ""   # nås inte — fel() avslutar

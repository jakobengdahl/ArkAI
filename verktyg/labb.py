#!/usr/bin/env python3
"""Gemensam kunskap om labbet: manifestet, statusen, miljön.

Både panelen och verktyg/kor.sh läser den här modulen. Poängen är att det finns
ett enda ställe som vet hur man tar reda på om en tjänst är installerad eller
igång — annars säger terminalen och panelen olika saker om samma tjänst.

Bara standardbiblioteket. Modulen måste gå att importera innan något är
installerat.

Kan också köras direkt:

    python3 verktyg/labb.py ids
    python3 verktyg/labb.py kommando eneo starta
    python3 verktyg/labb.py status eneo
    python3 verktyg/labb.py mcp-json
"""

from __future__ import annotations

import fcntl
import json
import os
import re
import shlex
import socket
import subprocess
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

# ── Sökvägar ──────────────────────────────────────────────────────────────

ROT = Path(__file__).resolve().parent.parent
MANIFEST = ROT / "verktyg" / "labb.toml"


def labbkatalog() -> Path:
    """Arbetskatalog för loggar, lås och status.

    Ligger utanför repot med flit: den överlever `git clean`, och ingenting
    som skrivs där kan råka commitas.
    """
    if os.environ.get("LABB_DIR"):
        return Path(os.environ["LABB_DIR"])
    arbete = Path(os.environ.get("WORKSPACE_DIR") or Path.home() / "work")
    if not arbete.is_dir():
        arbete = Path.home()
    return arbete / ".labb"


LABB = labbkatalog()
LOGG = LABB / "logg"
LAS = LABB / "las"
STATUS = LABB / "status"


def se_till_att_kataloger_finns() -> None:
    for k in (LOGG, LAS, STATUS):
        k.mkdir(parents=True, exist_ok=True)


# ── Manifestet ────────────────────────────────────────────────────────────

_katalog_cache: tuple[float, dict] | None = None


def katalog() -> dict:
    """Manifestet, omläst när filen ändrats."""
    global _katalog_cache
    mtid = MANIFEST.stat().st_mtime
    if _katalog_cache is None or _katalog_cache[0] != mtid:
        with MANIFEST.open("rb") as f:
            _katalog_cache = (mtid, tomllib.load(f))
    return _katalog_cache[1]


def tjanster() -> dict[str, dict]:
    return katalog().get("tjanst", {})


def tjanst(tjid: str) -> dict:
    t = tjanster().get(tjid)
    if t is None:
        raise KeyError(f"okänd tjänst: {tjid}")
    return t


def uppsattningar() -> dict[str, dict]:
    return katalog().get("uppsattning", {})


def synliga_tjanster() -> dict[str, dict]:
    """Tjänsterna panelen visar. Det som avvecklas ligger kvar men syns inte.

    Skillnaden finns för att en tjänst ska kunna tas ur bruk stegvis:
    installationsskript och dokumentation kvar, men ingen knapp som lockar
    någon att starta den igen. Se docs/60-miljo/openwebui.md.
    """
    return {i: t for i, t in tjanster().items() if not t.get("avvecklas")}


def byggstenar() -> list[dict]:
    """Byggstenarna ur docs/20-tekniker/byggstenar.md, i bildens ordning."""
    return katalog().get("byggsten", [])


def byggstenar_for(tjid: str) -> list[dict]:
    """[{id, namn, lage, not}] för en tjänst, i byggstenslistans ordning.

    Ordningen kommer från listan, inte från tjänsten: två verktyg ska gå att
    jämföra genom att läsa raderna på samma plats.
    """
    egna = tjanst(tjid).get("byggstenar", {})
    ut = []
    for b in byggstenar():
        post = egna.get(b["id"])
        if post:
            ut.append({"id": b["id"], "namn": b["namn"],
                       "lage": post.get("lage", "okand"), "not": post.get("not", "")})
    return ut


def navigering() -> list[dict]:
    return katalog().get("navigering", [])


def panelport() -> int:
    return int(os.environ.get("PANEL_PORT") or katalog().get("panel", {}).get("port", 8082))


def panel_publik_port() -> int | None:
    """Porten där panelen nås utifrån, bakom inloggning. None stänger av den."""
    varde = os.environ.get("PANEL_PUBLIK_PORT", katalog().get("panel", {}).get("publik_port"))
    return int(varde) if varde not in (None, "", "0") else None


def panel_inloggning() -> tuple[str, str]:
    """Användare ur manifestet, lösenord ur Vault (PANEL_LOSEN). Aldrig ur repot."""
    anv = os.environ.get("PANEL_ANVANDARE") or katalog().get("panel", {}).get("publik_anvandare", "")
    return anv, os.environ.get("PANEL_LOSEN", "")


def kommando(tjid: str, handling: str) -> str | None:
    """Kommandot för en handling, eller None om tjänsten inte stöder den."""
    return tjanst(tjid).get(handling)


def eneo_uppe() -> bool:
    """Svarar Eneo? Avgör om det är någon mening med att visa Koppla till Eneo.

    Kopplingen skriver mot Eneos API. Är Eneo nere blir knappen ett fel i en
    logg i stället för ett resultat, och då är det bättre att den inte finns.
    """
    return "eneo" in tjanster() and levande("eneo")


# ── Miljön ────────────────────────────────────────────────────────────────


def miljo() -> dict:
    """Det startskriptet skrev ner om hur tjänsten startades."""
    fil = LABB / "miljo.toml"
    if not fil.is_file():
        return {}
    try:
        with fil.open("rb") as f:
            return tomllib.load(f)
    except (tomllib.TOMLDecodeError, OSError):
        return {}


def proxy_url(port: int) -> str | None:
    """URL till en lokal port via code-servers proxy.

    Fungerar för sådant som klarar att ligga under en sökväg. Open WebUI gör
    inte det — se minnesbanken.
    """
    mall = os.environ.get("VSCODE_PROXY_URI")
    if not mall:
        return None
    return mall.replace("{{port}}", str(port))


_ingress_cache: tuple[float, list[dict]] | None = None


def ingresser() -> list[dict]:
    """Ingressernas regler i namnrymden: [{namn, host, portar}].

    En post per *regel*, inte per ingress. Exponerar du två portar lägger
    Onyxia båda i samma ingress, med ett värdnamn per port — slår man ihop
    reglerna hamnar den andra porten på den första portens värdnamn.

    Kräver bara läsrättigheter, alltså standardrollen `view`. Det är så vi kan
    visa riktiga URL:er till tjänster som kör utanför den här podden.
    """
    global _ingress_cache
    nu = time.monotonic()
    if _ingress_cache and nu - _ingress_cache[0] < 60:
        return _ingress_cache[1]
    resultat: list[dict] = []
    try:
        rå = subprocess.run(
            ["kubectl", "get", "ingress", "-o", "json"],
            capture_output=True, text=True, timeout=8,
        )
        if rå.returncode == 0:
            for post in json.loads(rå.stdout).get("items", []):
                namn = post.get("metadata", {}).get("name", "")
                for regel in post.get("spec", {}).get("rules", []):
                    if not regel.get("host"):
                        continue
                    portar = set()
                    for stig in regel.get("http", {}).get("paths", []):
                        p = stig.get("backend", {}).get("service", {}).get("port", {}).get("number")
                        if p:
                            portar.add(int(p))
                    resultat.append({
                        "namn": namn,
                        "host": regel["host"],
                        "portar": sorted(portar),
                    })
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError):
        pass
    _ingress_cache = (nu, resultat)
    return resultat


def _tjanstprefix() -> str:
    """Onyxias namn på den här tjänsten, t.ex. vscode-python-539185.

    Poddnamnet är tjänstnamnet plus ett löpnummer. Ingresserna heter samma sak
    plus ett suffix, vilket är hur vi skiljer våra egna ingresser från andras.
    """
    return re.sub(r"-\d+$", "", os.environ.get("HOSTNAME", ""))


def egen_ingress_for(port: int) -> str | None:
    """URL till den här poddens exponerade port, om den exponerades vid start.

    Är porten inte exponerad finns ingen ingress, och då finns det ingen väg
    dit utifrån. Behörigheter sätts när tjänsten startar — se minnesbanken.
    """
    prefix = _tjanstprefix()
    for ing in ingresser():
        if port not in ing["portar"]:
            continue
        if prefix and not ing["namn"].startswith(prefix):
            continue
        return f"https://{ing['host']}/"
    return None


_namnrymd_cache: tuple[float, dict] | None = None


def namnrymden() -> dict:
    """Arbetslaster, volymer och kvot i namnrymden.

    Det här är den enda vy som visar sådant som *överlever den här podden*.
    Deployar man något i namnrymden — Eneo, en databas — kör det kvar när
    VS Code-tjänsten stoppas, och fortsätter ta av kvoten. Panelen visar det
    för att man ska kunna städa, inte bara starta.

    Kräver bara läsrättigheter. Går något inte att läsa utelämnas den delen.
    """
    global _namnrymd_cache
    nu = time.monotonic()
    if _namnrymd_cache and nu - _namnrymd_cache[0] < 30:
        return _namnrymd_cache[1]

    def kubectl(*arg: str) -> dict:
        try:
            rå = subprocess.run(["kubectl", *arg, "-o", "json"],
                                capture_output=True, text=True, timeout=10)
            return json.loads(rå.stdout) if rå.returncode == 0 else {}
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError):
            return {}

    arbetslaster = []
    for post in kubectl("get", "deployments,statefulsets,jobs").get("items", []):
        sort = post.get("kind", "")
        status = post.get("status", {})
        if sort == "Job":
            lage = "klar" if status.get("succeeded") else ("kör" if status.get("active") else "—")
        else:
            lage = f"{status.get('readyReplicas', 0)}/{post.get('spec', {}).get('replicas', 0)}"
        arbetslaster.append({
            "sort": sort,
            "namn": post.get("metadata", {}).get("name", ""),
            "lage": lage,
            "etiketter": post.get("metadata", {}).get("labels", {}) or {},
        })

    volymer = [
        {
            "namn": p.get("metadata", {}).get("name", ""),
            "storlek": p.get("spec", {}).get("resources", {}).get("requests", {}).get("storage", ""),
            "etiketter": p.get("metadata", {}).get("labels", {}) or {},
        }
        for p in kubectl("get", "pvc").get("items", [])
    ]

    kvot = {}
    for k in kubectl("get", "resourcequota").get("items", []):
        status = k.get("status", {})
        for namn, hard in (status.get("hard") or {}).items():
            kvot[namn] = {"anvant": (status.get("used") or {}).get(namn, "?"), "tak": hard}

    svar = {"arbetslaster": arbetslaster, "volymer": volymer, "kvot": kvot}
    _namnrymd_cache = (nu, svar)
    return svar


def ingress_match(monster: str) -> str | None:
    for ing in ingresser():
        if monster in ing["namn"]:
            return f"https://{ing['host']}/"
    return None


# ── Status ────────────────────────────────────────────────────────────────
#
# Tillstånd sonderas, det läses inte ur en fil. En podd kan ha startats om
# sedan statusfilen skrevs, och någon kan ha kört samma sak från terminalen.
# Filen under status/ är bara en anteckning om senaste körningen.


def lasfil(tjid: str) -> Path:
    return LAS / f"{tjid}.lock"


def kors_nu(tjid: str) -> bool:
    """True om kor.sh håller låset för tjänsten just nu.

    Delat lås (LOCK_SH), inte exklusivt: två sonderingar samtidigt stör inte
    varandra, och kor.sh:s exklusiva lås utesluter dem båda — vilket är precis
    det vi vill upptäcka.

    Kvar finns ett litet fönster åt andra hållet: håller vi det delade låset i
    de mikrosekunder anropet tar, kan kor.sh:s `flock` misslyckas. Därför
    väntar kor.sh i två sekunder i stället för att ge upp direkt.
    """
    fil = lasfil(tjid)
    if not fil.exists():
        return False
    try:
        with fil.open("a+") as f:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError:
                return True
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except OSError:
        return False
    return False


def senaste_korning(tjid: str) -> dict:
    fil = STATUS / f"{tjid}.json"
    if not fil.is_file():
        return {}
    try:
        return json.loads(fil.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def skriv_korning(tjid: str, **falt) -> None:
    se_till_att_kataloger_finns()
    data = senaste_korning(tjid)
    data.update(falt)
    (STATUS / f"{tjid}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2))


def loggfil(tjid: str, handling: str) -> Path:
    return LOGG / f"{tjid}-{handling}.log"


def _skalkommando_lyckas(kmd: str, timeout: float = 5) -> bool:
    try:
        return subprocess.run(
            ["bash", "-lc", kmd], cwd=ROT, capture_output=True, timeout=timeout
        ).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _svarar(url: str, timeout: float = 2) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as svar:
            return svar.status < 500
    except urllib.error.HTTPError as fel:
        # 401 betyder att något svarar — det räcker som livstecken.
        return fel.code < 500
    except Exception:
        return False


def _port_oppen(port: int, timeout: float = 1) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=timeout):
            return True
    except OSError:
        return False


def levande(tjid: str) -> bool:
    """Svarar tjänsten? Tittar bara på hälsokontroll eller port.

    Skild från status() med flit: den som väntar in en start håller själv
    låset, och skulle då få svaret "arbetar" i evighet av status().
    """
    t = tjanst(tjid)
    if t.get("typ") == "fjarr":
        bas = os.environ.get(t.get("url_env", "")) or ""
        if not bas:
            bas = ingress_match(t.get("ingress_matchning", "\0")) or ""
        return bool(bas) and _svarar(bas.rstrip("/") + t.get("halsa_sokvag", "/"))
    if t.get("halsa"):
        return _svarar(t["halsa"])
    if t.get("port"):
        return _port_oppen(int(t["port"]))
    return False


_probe_cache: dict[str, tuple[float, dict]] = {}


def status(tjid: str, cache_sekunder: float = 3) -> dict:
    """Sonderat tillstånd för en tjänst.

    tillstand: arbetar | kor | installerad | saknas | okand
    """
    nu = time.monotonic()
    if tjid in _probe_cache and nu - _probe_cache[tjid][0] < cache_sekunder:
        return _probe_cache[tjid][1]

    t = tjanst(tjid)
    svar: dict = {"id": tjid, "namn": t.get("namn", tjid), "typ": t.get("typ", "lokal")}
    senast = senaste_korning(tjid)
    svar["senast"] = senast

    if kors_nu(tjid):
        svar["tillstand"] = "arbetar"
        svar["handling"] = senast.get("handling", "")
    elif t.get("typ") == "fjarr":
        # URL:en kommer helst ur miljön (Vault-hemligheten). Hittas den inte
        # där letar vi efter en matchande ingress i namnrymden.
        bas = os.environ.get(t.get("url_env", "")) or ""
        if not bas:
            bas = ingress_match(t.get("ingress_matchning", "\0")) or ""
        svar["url"] = bas or None
        if bas and _svarar(bas.rstrip("/") + t.get("halsa_sokvag", "/")):
            svar["tillstand"] = "kor"
        elif bas:
            svar["tillstand"] = "saknas"
        else:
            svar["tillstand"] = "okand"
    else:
        port = t.get("port")
        if levande(tjid):
            svar["tillstand"] = "kor"
        elif t.get("finns") and _skalkommando_lyckas(t["finns"]):
            svar["tillstand"] = "installerad"
        elif t.get("finns"):
            svar["tillstand"] = "saknas"
        else:
            svar["tillstand"] = "installerad"
        if port:
            if t.get("egen_ingress"):
                svar["url"] = egen_ingress_for(int(port))
                svar["kraver_ingress"] = svar["url"] is None
            else:
                svar["url"] = proxy_url(int(port))

    _probe_cache[tjid] = (nu, svar)
    return svar


def alla_statusar() -> dict[str, dict]:
    return {tjid: status(tjid) for tjid in tjanster()}


# ── Delad MCP-konfiguration ───────────────────────────────────────────────


def skriv_mcp_json() -> Path:
    """Skriver ~/work/.labb/mcp.json som alla klienter kan peka på.

    Det är den här filen som gör att tjänsterna hänger ihop: samma
    verktygsuppsättning för Claude Code, OpenClaw och Open WebUI:s brygga,
    i stället för tre konfigurationer som glider isär.

    Filen kan innehålla tokens och skrivs därför med 0600. Den ligger i
    ~/work/.labb/, alltså utanför repot.
    """
    se_till_att_kataloger_finns()
    servrar: dict[str, dict] = {}
    for tjid, t in tjanster().items():
        s = status(tjid)
        if t.get("mcp_kommando"):
            # stdio-server: startas av klienten. Räcker att den är installerad.
            if s["tillstand"] in ("installerad", "kor"):
                delar = [d.replace("{rot}", str(ROT))
                         for d in shlex.split(t["mcp_kommando"])]
                servrar[tjid] = {"type": "stdio", "command": delar[0], "args": delar[1:]}
        elif t.get("mcp_sokvag") and s["tillstand"] == "kor" and (
                s.get("url") or (t.get("typ") == "lokal" and t.get("port"))):
            # En lokal tjänst utan exponerad port nås ändå av klienter i podden.
            bas = s.get("url") or f"http://127.0.0.1:{t['port']}/"
            post = {"type": "sse", "url": bas.rstrip("/") + t["mcp_sokvag"]}
            token = os.environ.get(t.get("token_env", "")) if t.get("token_env") else None
            tokenfil = LABB / t["mcp_http_token_fil"] if t.get("mcp_http_token_fil") else None
            if not token and tokenfil and tokenfil.is_file():
                token = tokenfil.read_text().strip()
            if token:
                post["headers"] = {"Authorization": f"Bearer {token}"}
            servrar[tjid] = post
    # Rättigheterna sätts före skrivningen. Filen kan innehålla en token, och
    # det finns inget ögonblick där den ska ha legat läsbar för andra.
    fil = LABB / "mcp.json"
    fil.touch(mode=0o600, exist_ok=True)
    fil.chmod(0o600)
    fil.write_text(json.dumps({"mcpServers": servrar}, ensure_ascii=False, indent=2))
    return fil


# ── Kommandorad ───────────────────────────────────────────────────────────


def _main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    match argv[0]:
        case "ids":
            print("\n".join(tjanster()))
        case "kommando":
            kmd = kommando(argv[1], argv[2])
            if not kmd:
                return 1
            print(kmd)
        case "status":
            print(json.dumps(status(argv[1]), ensure_ascii=False, indent=2))
        case "tillstand":
            print(status(argv[1])["tillstand"])
        case "levande":
            return 0 if levande(argv[1]) else 1
        case "alla":
            print(json.dumps(alla_statusar(), ensure_ascii=False, indent=2))
        case "mcp-json":
            print(skriv_mcp_json())
        case "byggstenar":
            print(json.dumps(byggstenar_for(argv[1]), ensure_ascii=False, indent=2))
        case "uppsattning-finns":
            if argv[1] in uppsattningar():
                print(argv[1])
        case "ingress":
            url = egen_ingress_for(int(argv[1]))
            if not url:
                return 1
            print(url)
        case "namnrymd":
            print(json.dumps(namnrymden(), ensure_ascii=False, indent=2))
        case "katalog":
            print(LABB)
        case _:
            print(f"okänt kommando: {argv[0]}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))

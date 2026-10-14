#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown>=3.6"]
# ///
"""Labbpanelen — repots markdown renderad, och knappar för det som går att köra.

Två regler styr hela designen:

1. **Markdown är master.** Panelen renderar filerna som ligger i repot. Den har
   inget eget innehåll och ingen egen databas. Det som ska stå någonstans ska
   stå i en .md-fil som också går att läsa på GitHub.

2. **Inga absoluta sökvägar.** All routing sker via query-strängen och all CSS
   ligger inline. Därför fungerar panelen oförändrad både på
   http://127.0.0.1:8082/ och bakom code-servers /proxy/8082/ — till skillnad
   från appar som antar att de ligger i roten av ett värdnamn. Se
   minnesbank/verktyg/spa-fungerar-inte-bakom-sokvagsproxy.md.

Kör:
    verktyg/starta-panelen.sh
"""

from __future__ import annotations

import base64
import errno
import html
import http.server
import os
import re
import secrets
import subprocess
import sys
import threading
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import markdown
from markdown.extensions.toc import slugify_unicode

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import labb  # noqa: E402

ROT = labb.ROT
NONCE = secrets.token_urlsafe(16)
LASBARA_ANDELSER = {".md"}
BILDANDELSER = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}

STIL = """
:root {
  --bg:#ffffff; --text:#1a1a1a; --svag:#666; --kant:#e3e3e3; --dammig:#f6f6f6;
  --lank:#0b5fa5; --gron:#1a7f37; --gul:#9a6700; --rod:#b42318; --bla:#0b5fa5;
}
@media (prefers-color-scheme: dark) {
  :root { --bg:#1b1b1d; --text:#e6e6e6; --svag:#9a9a9a; --kant:#333; --dammig:#242427;
          --lank:#6cb6ff; --gron:#4ac26b; --gul:#d4a72c; --rod:#ff7b72; --bla:#6cb6ff; }
}
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--text);
  font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif; }
a { color:var(--lank); }
.ram { display:flex; min-height:100vh; align-items:stretch; }
nav { width:210px; flex:0 0 210px; border-right:1px solid var(--kant);
  background:var(--dammig); padding:18px 0; }
nav h1 { font-size:13px; letter-spacing:.08em; text-transform:uppercase;
  color:var(--svag); margin:0 0 12px 18px; }
nav a { display:block; padding:5px 18px; text-decoration:none; color:var(--text); font-size:14px; }
nav a:hover { background:var(--bg); }
nav a.pa { border-left:3px solid var(--lank); padding-left:15px; font-weight:600; }
nav .grupp { margin-top:22px; }
main { flex:1; min-width:0; padding:26px 34px 80px; max-width:1000px; }
main img { max-width:100%; }
h1,h2,h3 { line-height:1.25; }
h1 { font-size:26px; margin-top:0; }
h2 { font-size:20px; margin-top:32px; border-bottom:1px solid var(--kant); padding-bottom:5px; }
h3 { font-size:16px; }
code { background:var(--dammig); padding:1px 5px; border-radius:4px; font-size:13px; }
pre { background:var(--dammig); padding:12px 14px; border-radius:6px; overflow-x:auto; }
pre code { background:none; padding:0; }
table { border-collapse:collapse; width:100%; margin:14px 0; display:block; overflow-x:auto; }
th,td { border:1px solid var(--kant); padding:6px 10px; text-align:left; font-size:14px; }
th { background:var(--dammig); }
blockquote { border-left:3px solid var(--kant); margin:14px 0; padding:2px 14px;
  color:var(--svag); }
.kort { border:1px solid var(--kant); border-radius:8px; padding:14px 16px; margin:10px 0;
  background:var(--dammig); }
.kort h3 { margin:0 0 4px; font-size:15px; }
.kort p { margin:4px 0 10px; color:var(--svag); font-size:14px; }
.rutnat { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:12px; }
.märke { display:inline-block; font-size:12px; padding:1px 8px; border-radius:20px;
  border:1px solid currentColor; margin-left:8px; vertical-align:middle; }
.kor { color:var(--gron); } .arbetar { color:var(--gul); }
.installerad { color:var(--bla); } .saknas,.okand { color:var(--svag); } .fel { color:var(--rod); }
button, .knapp { font:inherit; font-size:13px; padding:5px 12px; border-radius:6px;
  border:1px solid var(--kant); background:var(--bg); color:var(--text); cursor:pointer;
  text-decoration:none; display:inline-block; margin-right:6px; }
button:hover, .knapp:hover { border-color:var(--lank); color:var(--lank); }
button.primar { background:var(--lank); color:#fff; border-color:var(--lank); }
button.primar:hover { opacity:.9; color:#fff; }
form { display:inline; }
.varning { border-left:3px solid var(--gul); background:var(--dammig); padding:10px 14px;
  border-radius:0 6px 6px 0; margin:10px 0; font-size:14px; }
.sidfot { margin-top:50px; padding-top:14px; border-top:1px solid var(--kant);
  color:var(--svag); font-size:13px; }
.logg { background:#0d0d0f; color:#d8d8d8; padding:14px; border-radius:6px;
  overflow-x:auto; font-size:12.5px; line-height:1.5; max-height:70vh; }
.tabellsvag td { color:var(--svag); }
.kort { min-width:0; overflow-wrap:anywhere; }
/* Flex med wrap, inte inline-spann: chipsen skrivs ut utan mellanslag mellan
   sig, och då finns det ingen radbrytningspunkt — de rann ut över grannkorten. */
.stenar, .teckenforklaring { display:flex; flex-wrap:wrap; gap:5px; align-items:center; }
.stenar { margin:8px 0 10px; }
.sten { font-size:12px; line-height:1.5; padding:1px 8px; border-radius:20px;
  border:1px solid currentColor; white-space:nowrap; }
.kort form, .kort .knapp { margin-bottom:6px; }
.inloggning { display:table; width:auto; margin:6px 0 10px; font-size:13px; }
.inloggning td { border:none; padding:1px 10px 1px 0; font-size:13px; }
.inloggning td:first-child { color:var(--svag); white-space:nowrap; overflow-wrap:normal; }
.sten.inbyggd { color:var(--gron); } .sten.konfig { color:var(--bla); }
.sten.tillval { color:var(--svag); } .sten.begransad { color:var(--gul); }
.sten.saknas { color:var(--rod); opacity:.75; }
details { margin:4px 0 12px; }
details summary { cursor:pointer; font-size:13.5px; color:var(--svag); }
details table { margin:8px 0 0; }
details td:first-child { white-space:nowrap; }
.byggposter { margin-top:8px; }
.byggpost { padding:7px 0; border-top:1px solid var(--kant); font-size:13.5px; }
.byggpost:first-child { border-top:none; }
.byggpost span { font-size:13px; }
.byggnot { color:var(--svag); font-size:13px; margin-top:2px; line-height:1.45; }
.teckenforklaring { font-size:13px; color:var(--svag); margin:6px 0 16px; }

"""


# ── Hjälp ─────────────────────────────────────────────────────────────────


def inom_repot(rel: str) -> Path | None:
    """Sökväg inuti repot, eller None.

    Två spärrar, båda nödvändiga:

    * `relative_to` stoppar `../../etc/passwd`.
    * `git check-ignore` stoppar det som är gitignorerat — `.env`, `lokalt/`,
      nycklar. Att en fil ligger i arbetskatalogen betyder inte att den är
      tänkt att läsas av någon annan, och panelen ska inte bli vägen dit.
    """
    try:
        p = (ROT / rel).resolve()
        p.relative_to(ROT)
    except (ValueError, OSError):
        return None
    if not p.is_file():
        return None
    if ".git" in p.relative_to(ROT).parts[:1]:
        return None
    if _ignoreras(p):
        return None
    return p


def _ignoreras(p: Path) -> bool:
    try:
        return subprocess.run(
            ["git", "check-ignore", "-q", str(p)], cwd=ROT, timeout=5
        ).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return True   # kan vi inte avgöra det, visar vi den inte


def e(text: str) -> str:
    return html.escape(str(text), quote=True)


# ── Markdown → HTML ───────────────────────────────────────────────────────

_ANKARE = re.compile(r'(href|src)="([^"]+)"')


def gor_lankar_relativa(html_text: str, kalla: Path) -> str:
    """Skriv om länkar mellan .md-filer till panelens query-routing.

    Externa länkar och ankare lämnas som de är. Ingenting får bli en absolut
    sökväg — det är det som skulle sluta fungera bakom proxyn.
    """
    katalog = kalla.parent

    def byt(m: re.Match) -> str:
        attr, mal = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#|\?|data:)", mal):
            return m.group(0)
        ren = mal.split("#")[0]
        ankare = mal[len(ren):]
        if not ren:
            return m.group(0)
        try:
            absolut = (katalog / ren).resolve()
            rel = absolut.relative_to(ROT).as_posix()
        except (ValueError, OSError):
            return m.group(0)
        if ren.endswith("/") or (ROT / rel).is_dir():
            rel = f"{rel}/README.md"
        suffix = Path(rel).suffix.lower()
        if attr == "src" and suffix in BILDANDELSER:
            return f'src="?bild={urllib.parse.quote(rel)}"'
        if suffix in LASBARA_ANDELSER:
            return f'href="?sida={urllib.parse.quote(rel)}{ankare}"'
        if (ROT / rel).exists():
            return f'href="?fil={urllib.parse.quote(rel)}"'
        return m.group(0)

    return _ANKARE.sub(byt, html_text)


def rendera_markdown(fil: Path) -> str:
    text = fil.read_text(encoding="utf-8")
    text = expandera_block(text)
    ut = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "toc", "md_in_html"],
        # Utan detta blir "## Två spår" id:t "tva-spar", medan GitHub behåller
        # "två-spår". Länkarna i filerna är skrivna för GitHub — följ dem.
        extension_configs={"toc": {"slugify": slugify_unicode}},
    )
    return gor_lankar_relativa(ut, fil)


# ── Dynamiska block ───────────────────────────────────────────────────────
#
# Markdownfilerna innehåller <!-- panel:namn -->. På GitHub syns de inte alls;
# i panelen byts de mot levande innehåll. Master förblir markdown.

_BLOCK = re.compile(r"<!--\s*panel:([a-z-]+)\s*-->")


def expandera_block(text: str) -> str:
    return _BLOCK.sub(lambda m: _BLOCKBYGGARE.get(m.group(1), _okant)(m.group(1)), text)


def _okant(namn: str) -> str:
    return f"<p><em>Okänt panelblock: {e(namn)}</em></p>"


def _statusar() -> dict[str, dict]:
    ids = list(labb.synliga_tjanster())
    with ThreadPoolExecutor(max_workers=8) as pool:
        return dict(zip(ids, pool.map(labb.status, ids)))


TILLSTANDSTEXT = {
    "kor": "kör",
    "arbetar": "arbetar",
    "installerad": "installerad",
    "saknas": "ej installerad",
    "okand": "okänd",
}


def _knappar(tjid: str, s: dict, eneo_uppe: bool = False) -> str:
    t = labb.tjanst(tjid)
    delar = []

    def form(handling: str, etikett: str, primar: bool = False) -> str:
        klass = "primar" if primar else ""
        return (
            f'<form method="post" action=""><input type="hidden" name="nonce" value="{NONCE}">'
            f'<input type="hidden" name="id" value="{e(tjid)}">'
            f'<input type="hidden" name="handling" value="{handling}">'
            f'<button type="submit" class="{klass}">{e(etikett)}</button></form>'
        )

    if s["tillstand"] == "arbetar":
        delar.append(f'<a class="knapp" href="?logg={e(tjid)}">Visa vad som händer</a>')
    else:
        if s["tillstand"] == "saknas" and t.get("installera"):
            delar.append(form("installera", "Installera", primar=True))
        if s["tillstand"] == "installerad" and t.get("starta"):
            delar.append(form("starta", "Starta", primar=True))
        if s["tillstand"] == "kor":
            # webbsida = false: tjänsten svarar på sin port men har inget att
            # titta på i en webbläsare. En MCP-server ger 404 i roten, och en
            # knapp som leder dit är sämre än ingen knapp.
            if s.get("url") and t.get("webbsida", True):
                delar.append(f'<a class="knapp" href="{e(s["url"])}" target="_blank">Öppna</a>')
            if t.get("stoppa"):
                delar.append(form("stoppa", "Stoppa"))
        # Kopplingen skriver mot Eneos API. Den visas när det finns något att
        # skriva till — annars blir knappen ett fel i en logg.
        if t.get("koppla_eneo") and s["tillstand"] == "kor" and eneo_uppe:
            delar.append(form("koppla_eneo", t.get("koppla_eneo_knapp", "Koppla in i Eneo")))
        # Avinstallation är destruktiv och går via en bekräftelsesida, aldrig
        # direkt från ett kort. Sidan visar vad som faktiskt försvinner.
        if t.get("avinstallera") and s["tillstand"] in ("installerad", "kor"):
            delar.append(f'<a class="knapp" href="?bekrafta={e(tjid)}">Ta bort</a>')
        if t.get("dok"):
            dok = urllib.parse.quote(t["dok"])
            delar.append(f'<a class="knapp" href="?sida={dok}">Läs mer</a>')
        if any(labb.loggfil(tjid, h).exists()
               for h in ("installera", "starta", "koppla_eneo")):
            delar.append(f'<a class="knapp" href="?logg={e(tjid)}">Logg</a>')
    return "".join(delar)


LAGETEXT = {
    "inbyggd": "ingår, går inte att koppla bort",
    "konfig": "ingår, men måste ställas in",
    "tillval": "ingår inte — går att lägga till",
    "begransad": "finns delvis, läs noten",
    "saknas": "finns inte",
}


def _byggstenar(tjid: str) -> str:
    """Vilka byggstenar verktyget består av, och vad som går att ställa in.

    Kopplingen står i verktyg/labb.toml, bredvid tjänsten. Poängen med att visa
    den här är att ett verktyg annars beskrivs med sitt eget produktspråk, och
    då går det inte att jämföra med nästa verktyg. Se
    docs/20-tekniker/byggstenar.md.
    """
    stenar = labb.byggstenar_for(tjid)
    if not stenar:
        return ""
    chips = "".join(
        f'<span class="sten {e(b["lage"])}">{e(b["namn"])}</span>' for b in stenar
    )
    # En post per byggsten, staplad: namn och läge på en rad, noten under.
    # En tabell med tre kolumner fick inte plats i ett kort på ~300 px —
    # noten blev en smal remsa med ett par ord per rad.
    poster = "".join(
        f'<div class="byggpost"><div><strong>{e(b["namn"])}</strong> '
        f'<span class="{e(b["lage"])}">· {e(LAGETEXT.get(b["lage"], b["lage"]))}</span></div>'
        + (f'<div class="byggnot">{e(b["not"])}</div>' if b.get("not") else "")
        + "</div>"
        for b in stenar
    )
    return (
        f'<p class="stenar">{chips}</p>'
        "<details><summary>Vad som ingår, och vad som går att ställa in</summary>"
        f'<div class="byggposter">{poster}</div>'
        "</details>"
    )


def _tjanstekort(tjid: str, s: dict, eneo_uppe: bool = False) -> str:
    t = labb.tjanst(tjid)
    text = TILLSTANDSTEXT.get(s["tillstand"], s["tillstand"])
    varning = ""
    if s.get("kraver_ingress"):
        varning = (
            '<div class="varning"><strong>Porten är inte exponerad.</strong> '
            f'{e(t["namn"])} kräver ett eget värdnamn, och det sätts bara vid start. '
            'Se <a href="?sida=docs/60-miljo/starta-labbet.md">Starta labbet</a> för URL:en '
            "som startar om med rätt inställning.</div>"
        )
    adress = ""
    if s.get("url") and not t.get("webbsida", True) and s["tillstand"] == "kor":
        # Ingen knapp, men adressen är det man behöver veta: det är den Eneo
        # och andra klienter utifrån ska peka på.
        adress = (f'<p style="font-size:13px"><code>'
                  f'{e(s["url"].rstrip("/") + t.get("mcp_http_sokvag", ""))}</code></p>')
    elif s.get("url") and t.get("egen_ingress") and s["tillstand"] == "kor":
        # Eget värdnamn går att dela och bokmärka — skriv ut det, inte bara
        # en knapp. Inloggningen står i manifestet (fältet inloggning).
        inl = t.get("inloggning") or {}
        rader = [("Adress", f'<a href="{e(s["url"])}" target="_blank">{e(s["url"])}</a>')]
        if inl.get("anvandare"):
            rader.append(("Användare", f"<code>{e(inl['anvandare'])}</code>"))
        if inl.get("losenord"):
            rader.append(("Lösenord", f"<code>{e(inl['losenord'])}</code>"))
        adress = ('<table class="inloggning">' + "".join(
            f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rader) + "</table>")
    return (
        f'<div class="kort"><h3>{e(t.get("namn", tjid))}'
        f'<span class="märke {s["tillstand"]}">{text}</span></h3>'
        f'<p>{e(t.get("beskrivning", ""))}</p>{varning}{adress}'
        f'{_byggstenar(tjid)}{_knappar(tjid, s, eneo_uppe)}</div>'
    )


def block_verktyg(_: str) -> str:
    """Ett kort per verktyg, med byggstenarna det består av."""
    statusar = _statusar()
    eneo_uppe = labb.eneo_uppe()
    ordning = {"arbetar": 0, "kor": 1, "installerad": 2, "saknas": 3, "okand": 4}
    ids = sorted(statusar, key=lambda i: (ordning.get(statusar[i]["tillstand"], 9), i))
    forklaring = " ".join(
        f'<span class="sten {lage}">{namn}</span>'
        for lage, namn in (
            ("inbyggd", "ingår"), ("konfig", "ställs in"), ("tillval", "går att lägga till"),
            ("begransad", "delvis"), ("saknas", "saknas"),
        )
    )
    return (
        f'<p class="teckenforklaring">{forklaring}</p>'
        '<div class="rutnat">'
        + "".join(_tjanstekort(i, statusar[i], eneo_uppe) for i in ids)
        + "</div>"
    )


def block_status(_: str) -> str:
    statusar = _statusar()
    rader = []
    for tjid, s in statusar.items():
        if s["tillstand"] in ("saknas", "okand"):
            continue
        lank = f'<a href="{e(s["url"])}" target="_blank">öppna</a>' if s.get("url") else ""
        rader.append(
            f'<tr><td>{e(s["namn"])}</td>'
            f'<td class="{s["tillstand"]}">{TILLSTANDSTEXT.get(s["tillstand"])}</td>'
            f"<td>{lank}</td></tr>"
        )
    if not rader:
        return "<p><em>Ingenting kör ännu.</em></p>"
    return "<table><tr><th>Tjänst</th><th>Läge</th><th></th></tr>" + "".join(rader) + "</table>"


def _finns(kmd: str) -> bool:
    try:
        return subprocess.run(
            ["bash", "-lc", f"command -v {kmd}"], capture_output=True, timeout=5
        ).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def block_miljo(_: str) -> str:
    m = labb.miljo()
    verktyg = ["git", "uv", "python3", "node", "gh", "kubectl", "caddy", "mcpo", "openclaw"]
    with ThreadPoolExecutor(max_workers=8) as pool:
        finns = dict(zip(verktyg, pool.map(_finns, verktyg)))
    prickar = " ".join(
        f'<span class="märke {"kor" if finns[v] else "saknas"}">{e(v)}</span>' for v in verktyg
    )
    rader = [
        ("Namnrymd", os.environ.get("KUBERNETES_NAMESPACE", "okänd")),
        ("Podd", os.environ.get("HOSTNAME", "okänd")),
        ("Profil vid start", " ".join(m.get("profil", [])) or "—"),
        ("Startad", m.get("startad", "—")),
        ("Panelen", labb.proxy_url(labb.panelport()) or f"http://127.0.0.1:{labb.panelport()}/"),
    ]
    publik = labb.panel_publik_port()
    if publik:
        rader.append(("Panelen utifrån", labb.egen_ingress_for(publik)
                      or f"port {publik} exponerades inte vid start"))
    tabell = "".join(f"<tr><td>{e(k)}</td><td>{e(v)}</td></tr>" for k, v in rader)
    knapp = (
        f'<form method="post" action=""><input type="hidden" name="nonce" value="{NONCE}">'
        f'<input type="hidden" name="id" value="grund">'
        f'<input type="hidden" name="handling" value="installera">'
        f'<button type="submit">Kör om grundinstallationen</button></form>'
    )
    return f'<p>{prickar}</p><table class="tabellsvag">{tabell}</table>{knapp}'


def _storlek(varde: str) -> str:
    """Kubernetes storleksangivelse till något läsbart: 173343481Ki → 165 GiB."""
    enheter = {"Ki": 1024, "Mi": 1024**2, "Gi": 1024**3, "Ti": 1024**4}
    for suffix, faktor in enheter.items():
        if varde.endswith(suffix):
            try:
                byte = float(varde[: -len(suffix)]) * faktor
            except ValueError:
                return varde
            return f"{byte / 1024**4:.1f} TiB" if byte >= 1024**4 else f"{byte / 1024**3:.0f} GiB"
    return varde


def block_namnrymd(_: str) -> str:
    ing = labb.ingresser()
    if not ing:
        return (
            "<p><em>Kunde inte läsa namnrymden. Det kräver läsrättigheter "
            "(<code>kubectl get ingress</code>).</em></p>"
        )
    rader = "".join(
        f'<tr><td>{e(i["namn"])}</td>'
        f'<td><a href="https://{e(i["host"])}/" target="_blank">{e(i["host"])}</a></td></tr>'
        for i in sorted(ing, key=lambda x: x["namn"])
    )
    return (
        "<table><tr><th>Adresser i namnrymden</th><th>Värdnamn</th></tr>" + rader + "</table>"
        "<p style='font-size:13.5px;color:var(--svag)'>Hämtat med "
        "<code>kubectl get ingress</code>. "
        "Det som ligger bakom ett inloggningsskydd svarar ändå på sin hälsokontroll.</p>"
    )


def block_kvot(_: str) -> str:
    """Vad som kör i namnrymden och vad det tar av kvoten.

    Finns för att det som deployats i namnrymden inte försvinner när den här
    podden gör det. Utan den här vyn är det ingen som ser att en installation
    står kvar och äter kvot efter att tjänsten den startades från är borta.
    """
    n = labb.namnrymden()
    if not n["arbetslaster"] and not n["volymer"]:
        return ("<p><em>Kunde inte läsa arbetslasterna. Det kräver läsrättigheter "
                "(<code>kubectl get deployments</code>).</em></p>")

    kvot = n["kvot"]
    poddar = kvot.get("count/pods", {})
    lagring = kvot.get("requests.storage", {})
    sammanfattning = []
    if poddar:
        sammanfattning.append(f'poddar {e(poddar.get("anvant"))} av {e(poddar.get("tak"))}')
    if lagring:
        sammanfattning.append(
            f'lagring {e(_storlek(lagring.get("anvant", "")))} av '
            f'{e(_storlek(lagring.get("tak", "")))}'
        )

    # Etiketten app.kubernetes.io/part-of sätts av manifesten i verktyg/, och
    # värdet är tjänstens id. Andra saker i namnrymden kan ha samma etikett med
    # ett annat värde — den räknas alltså inte som labbets bara för att den finns.
    def hor_till_labbet(post: dict) -> bool:
        return post.get("etiketter", {}).get("app.kubernetes.io/part-of") in labb.tjanster()

    rader = []
    for a in sorted(n["arbetslaster"], key=lambda x: (x["sort"], x["namn"])):
        del_av = a["etiketter"].get("app.kubernetes.io/part-of", "")
        rader.append(
            f'<tr><td>{e(a["namn"])}</td><td>{e(a["sort"])}</td><td>{e(a["lage"])}</td>'
            f'<td>{e(del_av)}</td></tr>'
        )
    for v in sorted(n["volymer"], key=lambda x: x["namn"]):
        del_av = v["etiketter"].get("app.kubernetes.io/part-of", "")
        rader.append(
            f'<tr><td>{e(v["namn"])}</td><td>Volym</td><td>{e(v["storlek"])}</td>'
            f'<td>{e(del_av)}</td></tr>'
        )
    tabell = (
        "<table><tr><th>Namn</th><th>Sort</th><th>Läge</th><th>Del av</th></tr>"
        + "".join(rader) + "</table>"
    )
    egna = sum(1 for a in n["arbetslaster"] if hor_till_labbet(a))
    notis = (
        f"<p style='font-size:13.5px;color:var(--svag)'>{' · '.join(sammanfattning)}. "
        f"{egna} av arbetslasterna är deployade härifrån och tas bort med "
        "<em>Ta bort</em> på tjänstens kort ovan.</p>"
    ) if sammanfattning else ""
    return tabell + notis


_BLOCKBYGGARE = {
    "verktyg": block_verktyg,
    "status": block_status,
    "miljo": block_miljo,
    "namnrymd": block_namnrymd,
    "kvot": block_kvot,
}


# ── Sidor ─────────────────────────────────────────────────────────────────


def skal(innehall: str, aktiv: str = "", titel: str = "Labbet") -> bytes:
    lankar = []
    for post in labb.navigering():
        pa = " pa" if post["fil"] == aktiv else ""
        lankar.append(
            f'<a class="{pa.strip()}" href="?sida={urllib.parse.quote(post["fil"])}">'
            f'{e(post["titel"])}</a>'
        )
    sida = f"""<!doctype html><html lang="sv"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titel)}</title><style>{STIL}</style></head><body>
<div class="ram">
<nav><h1>Labbet</h1>{"".join(lankar)}
<div class="grupp"><h1>Panelen</h1>
<a href="?sida=docs/60-miljo/panelen.md">Så funkar den</a>
<a href="?sida=docs/60-miljo/starta-labbet.md">Starta om miljön</a>
</div></nav>
<main>{innehall}
<div class="sidfot">Panelen renderar markdownfilerna i repot. Rätta i filen, inte i panelen.
&nbsp;·&nbsp; <a href="?sida=docs/START.md">Start</a></div>
</main></div></body></html>"""
    return sida.encode("utf-8")


def sida_markdown(rel: str) -> tuple[int, bytes]:
    fil = inom_repot(rel)
    if not fil or fil.suffix.lower() not in LASBARA_ANDELSER:
        return 404, skal(
            f"<h1>Hittar inte {e(rel)}</h1>"
            "<p>Filen finns inte i repot, eller är inte markdown.</p>"
        )
    return 200, skal(rendera_markdown(fil), aktiv=rel, titel=fil.stem)


def sida_logg(tjid: str) -> tuple[int, bytes]:
    handlingar = ("installera", "starta", "stoppa", "avinstallera", "koppla_eneo",
                  "uppsattning")
    känd = (
        tjid in labb.tjanster()
        or tjid in labb.uppsattningar()
        or any(labb.loggfil(tjid, h).exists() for h in handlingar)
    )
    if not känd or "/" in tjid:
        return 404, skal("<h1>Okänd tjänst</h1>")
    # En uppsättning har inget eget lås — den arbetar så länge någon av dess
    # tjänster gör det.
    ingaende = labb.uppsattningar().get(tjid, {}).get("tjanster", [])
    arbetar = labb.kors_nu(tjid) or any(labb.kors_nu(t) for t in ingaende)
    delar = []
    for handling in handlingar:
        fil = labb.loggfil(tjid, handling)
        if fil.exists():
            try:
                rader = fil.read_text(encoding="utf-8", errors="replace").splitlines()[-300:]
            except OSError:
                continue
            delar.append(f"<h2>{handling}</h2><pre class='logg'>{e(chr(10).join(rader))}</pre>")
    if not delar:
        # Kraschade kor.sh innan den hann skriva tjänstens logg står orsaken
        # här. Utan den här grenen syns bara "ingen logg ännu".
        panelogg = labb.LOGG / "panel-kor.log"
        rader = []
        if panelogg.exists():
            try:
                rader = panelogg.read_text(encoding="utf-8", errors="replace").splitlines()[-40:]
            except OSError:
                rader = []
        if rader:
            delar.append(
                "<p>Ingen logg för tjänsten. Sista raderna ur panelens egen logg:</p>"
                f"<pre class='logg'>{e(chr(10).join(rader))}</pre>"
            )
        else:
            delar.append("<p>Ingen logg ännu.</p>")
    rubrik = "arbetar just nu" if arbetar else "senaste körningen"
    uppdatera = '<meta http-equiv="refresh" content="3">' if arbetar else ""
    post = labb.tjanster().get(tjid) or labb.uppsattningar().get(tjid) or {}
    namn = post.get("namn", tjid)
    return 200, skal(
        f"{uppdatera}<h1>{e(namn)} — {rubrik}</h1>"
        f'<p><a href="?sida=docs/START.md">← Tillbaka till start</a>'
        + ("&nbsp;·&nbsp; Sidan uppdateras var tredje sekund." if arbetar else "")
        + "</p>" + "".join(delar)
    )


def sida_bekrafta(tjid: str) -> tuple[int, bytes]:
    """Sista steget före något destruktivt.

    Ingen knapp på ett tjänstekort tar bort något direkt. Den här sidan visar
    vad som faktiskt försvinner — hämtat med tjänstens egen `avinstallera_visa`
    ur manifestet — och har den enda knapp som kör det.
    """
    if tjid not in labb.tjanster() or not labb.tjanst(tjid).get("avinstallera"):
        return 404, skal("<h1>Går inte att ta bort</h1>"
                         "<p>Tjänsten har ingen avinstallation i manifestet.</p>")
    t = labb.tjanst(tjid)
    namn = t.get("namn", tjid)
    varning = t.get("avinstallera_varning", "Det här går inte att ångra.")
    visa = ""
    if t.get("avinstallera_visa"):
        try:
            ut = subprocess.run(["bash", "-lc", t["avinstallera_visa"]], cwd=ROT,
                                capture_output=True, text=True, timeout=20)
            text = (ut.stdout or ut.stderr).strip() or "(ingenting hittades)"
        except (OSError, subprocess.SubprocessError):
            text = "(kunde inte läsa)"
        visa = f"<h2>Det här försvinner</h2><pre class='logg'>{e(text)}</pre>"
    knapp = (
        f'<form method="post" action=""><input type="hidden" name="nonce" value="{NONCE}">'
        f'<input type="hidden" name="id" value="{e(tjid)}">'
        f'<input type="hidden" name="handling" value="avinstallera">'
        f'<button type="submit" class="primar">Ta bort {e(namn)}</button></form>'
        f'<a class="knapp" href="?sida=docs/START.md">Avbryt</a>'
    )
    return 200, skal(
        f"<h1>Ta bort {e(namn)}?</h1>"
        f'<div class="varning">{e(varning)}</div>{visa}{knapp}'
    )


def starta_handling(handling: str, tjid: str) -> str:
    """Startar kor.sh frånkopplat och returnerar vart vi ska skicka läsaren.

    Uppsättningar körs bara från terminalen. Panelens ingång är verktyget och
    dess knappar — se docs/60-miljo/panelen.md.
    """
    if tjid not in labb.tjanster() or handling not in (
        "installera", "starta", "stoppa", "avinstallera", "koppla_eneo"
    ):
        return "?sida=docs/START.md"
    kmd = ["verktyg/kor.sh", handling, tjid]
    mal = f"?logg={urllib.parse.quote(tjid)}"
    labb.se_till_att_kataloger_finns()
    # kor.sh skriver själv tjänstens logg. Panelens egen omdirigering går till
    # en separat fil — annars hamnar varje rad två gånger i loggvyn.
    with (labb.LOGG / "panel-kor.log").open("ab") as ut:
        subprocess.Popen(kmd, cwd=ROT, stdout=ut, stderr=ut, start_new_session=True)
    return mal


# ── HTTP ──────────────────────────────────────────────────────────────────


class Panel(http.server.BaseHTTPRequestHandler):
    server_version = "Labbpanelen"

    def _svara(self, kod: int, kropp: bytes, typ: str = "text/html; charset=utf-8",
               sandlada: bool = False) -> None:
        self.send_response(kod)
        self.send_header("Content-Type", typ)
        if sandlada:
            self.send_header("Content-Security-Policy", "default-src 'none'; sandbox")
        self.send_header("Content-Length", str(len(kropp)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(kropp)

    def do_GET(self) -> None:  # noqa: N802
        fråga = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        hämta = lambda n: (fråga.get(n) or [""])[0]  # noqa: E731

        if hämta("bild"):
            fil = inom_repot(hämta("bild"))
            if fil and fil.suffix.lower() in BILDANDELSER:
                typ = "image/svg+xml" if fil.suffix == ".svg" else f"image/{fil.suffix[1:]}"
                # SVG är körbar kod. Panelen kan starta processer, så en bild
                # får inte kunna köra skript i samma origin.
                return self._svara(200, fil.read_bytes(), typ, sandlada=True)
            return self._svara(404, b"", "text/plain")

        if hämta("fil"):
            fil = inom_repot(hämta("fil"))
            if fil:
                text = fil.read_text(encoding="utf-8", errors="replace")
                return self._svara(200, skal(
                    f"<h1>{e(fil.name)}</h1><pre>{e(text)}</pre>", titel=fil.name))
            return self._svara(404, skal("<h1>Hittar inte filen</h1>"))

        if hämta("logg"):
            kod, kropp = sida_logg(hämta("logg"))
            return self._svara(kod, kropp)

        if hämta("bekrafta"):
            kod, kropp = sida_bekrafta(hämta("bekrafta"))
            return self._svara(kod, kropp)

        rel = hämta("sida") or labb.katalog().get("panel", {}).get("startsida", "docs/START.md")
        kod, kropp = sida_markdown(rel)
        self._svara(kod, kropp)

    def do_POST(self) -> None:  # noqa: N802
        längd = int(self.headers.get("Content-Length") or 0)
        form = urllib.parse.parse_qs(self.rfile.read(längd).decode("utf-8"))
        hämta = lambda n: (form.get(n) or [""])[0]  # noqa: E731

        # Panelen kan starta processer. Nonce hindrar att en annan sida i
        # webbläsaren postar hit i smyg.
        if hämta("nonce") != NONCE:
            return self._svara(403, skal(
                "<h1>Sidan var för gammal</h1><p>Panelen har startats om sedan sidan laddades. "
                '<a href="?sida=docs/START.md">Ladda om</a> och försök igen.</p>'))

        mal = starta_handling(hämta("handling"), hämta("id"))
        self.send_response(303)
        self.send_header("Location", mal)   # relativ med flit — överlever proxyn
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        sys.stderr.write("  %s\n" % (format % args))


# Ett lösenord kortare än så här öppnar inte porten. Den är ett publikt värdnamn.
MINSTA_LOSEN = 12


class PublikPanel(Panel):
    """Samma panel på den exponerade porten, bakom Basic auth.

    Porten är ett publikt värdnamn, och panelen kan starta, stoppa och ta bort
    tjänster. Inget svar — inte ens en bild — lämnas ut utan inloggning.
    Lösenordet kommer ur Vault (PANEL_LOSEN), aldrig ur repot.
    """

    def _inloggad(self) -> bool:
        anv, losen = labb.panel_inloggning()
        typ, _, data = (self.headers.get("Authorization") or "").partition(" ")
        if typ.lower() != "basic":
            return False
        try:
            givet = base64.b64decode(data, validate=True)
        except ValueError:
            return False
        return secrets.compare_digest(givet, f"{anv}:{losen}".encode("utf-8"))

    def _neka(self) -> None:
        kropp = "Logga in. Lösenordet är PANEL_LOSEN i din Vault-hemlighet.\n".encode()
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Labbet", charset="UTF-8"')
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(kropp)))
        self.end_headers()
        self.wfile.write(kropp)

    def do_GET(self) -> None:  # noqa: N802
        if not self._inloggad():
            return self._neka()
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if not self._inloggad():
            return self._neka()
        super().do_POST()


def starta_publik(port: int) -> None:
    """Startar den publika lyssnaren i bakgrunden. Går den inte, kör 127.0.0.1 ändå."""
    anv, losen = labb.panel_inloggning()
    if not anv or len(losen) < MINSTA_LOSEN:
        print(f"PANEL_LOSEN saknas i Vault, eller är kortare än {MINSTA_LOSEN} tecken — "
              f"panelen startas inte på port {port}. Se docs/60-miljo/starta-labbet.md.",
              file=sys.stderr)
        return
    try:
        server = http.server.ThreadingHTTPServer(("0.0.0.0", port), PublikPanel)
    except OSError as e:
        print(f"Port {port} gick inte att öppna ({e.strerror}) — panelen nås bara via VS Code.",
              file=sys.stderr)
        return
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = labb.egen_ingress_for(port)
    if url:
        print(f"Utifrån:        {url}  (användare {anv}, lösenord PANEL_LOSEN)")
    else:
        print(f"Port {port} lyssnar, men exponerades inte när tjänsten startade — "
              "den nås inte utifrån. Se docs/60-miljo/starta-labbet.md.")


def main() -> int:
    # I bakgrunden går stdout till panel.log, och utan radbuffring hamnar
    # startraderna aldrig där — loggen ser då tom ut fast panelen kör.
    sys.stdout.reconfigure(line_buffering=True)
    port = labb.panelport()
    labb.se_till_att_kataloger_finns()
    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Panel)
    except OSError as e:
        if e.errno != errno.EADDRINUSE:
            raise
        print(f"Port {port} är redan upptagen — panelen kör troligen redan. "
              "Startar inte en till.", file=sys.stderr)
        return 1
    proxy = labb.proxy_url(port)
    print(f"Labbpanelen kör på http://127.0.0.1:{port}/")
    if proxy:
        print(f"I webbläsaren:  {proxy}")
        print("I VS Code:      Ctrl+Shift+P → Simple Browser: Show → klistra in URL:en")
    publik = labb.panel_publik_port()
    if publik:
        starta_publik(publik)
    print("Avsluta med Ctrl+C.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAvslutar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

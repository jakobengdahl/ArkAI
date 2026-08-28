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

import html
import http.server
import os
import re
import secrets
import subprocess
import sys
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
    ids = list(labb.tjanster())
    with ThreadPoolExecutor(max_workers=8) as pool:
        return dict(zip(ids, pool.map(labb.status, ids)))


TILLSTANDSTEXT = {
    "kor": "kör",
    "arbetar": "arbetar",
    "installerad": "installerad",
    "saknas": "ej installerad",
    "okand": "okänd",
}


def _knappar(tjid: str, s: dict) -> str:
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
            if s.get("url"):
                delar.append(f'<a class="knapp" href="{e(s["url"])}" target="_blank">Öppna</a>')
            if t.get("stoppa"):
                delar.append(form("stoppa", "Stoppa"))
        if t.get("dok"):
            dok = urllib.parse.quote(t["dok"])
            delar.append(f'<a class="knapp" href="?sida={dok}">Läs mer</a>')
        if labb.loggfil(tjid, "installera").exists() or labb.loggfil(tjid, "starta").exists():
            delar.append(f'<a class="knapp" href="?logg={e(tjid)}">Logg</a>')
    return "".join(delar)


def _tjanstekort(tjid: str, s: dict) -> str:
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
    return (
        f'<div class="kort"><h3>{e(t.get("namn", tjid))}'
        f'<span class="märke {s["tillstand"]}">{text}</span></h3>'
        f'<p>{e(t.get("beskrivning", ""))}</p>{varning}{_knappar(tjid, s)}</div>'
    )


def block_tjanster(_: str) -> str:
    statusar = _statusar()
    ordning = {"arbetar": 0, "kor": 1, "installerad": 2, "saknas": 3, "okand": 4}
    ids = sorted(statusar, key=lambda i: (ordning.get(statusar[i]["tillstand"], 9), i))
    return '<div class="rutnat">' + "".join(_tjanstekort(i, statusar[i]) for i in ids) + "</div>"


def block_uppsattningar(_: str) -> str:
    statusar = _statusar()
    kort = []
    for uid, u in labb.uppsattningar().items():
        delar = []
        for tjid in u["tjanster"]:
            s = statusar.get(tjid, {"tillstand": "okand"})
            namn = labb.tjanst(tjid).get("namn", tjid)
            delar.append(
                f'<span class="märke {s["tillstand"]}">{e(namn)}</span>'
            )
        arbetar = any(statusar.get(t, {}).get("tillstand") == "arbetar" for t in u["tjanster"])
        knapp = (
            f'<a class="knapp" href="?logg={e(uid)}">Arbetar …</a>'
            if arbetar
            else (
                f'<form method="post" action=""><input type="hidden" name="nonce" value="{NONCE}">'
                f'<input type="hidden" name="id" value="{e(uid)}">'
                f'<input type="hidden" name="handling" value="uppsattning">'
                f'<button type="submit" class="primar">Kör igång</button></form>'
            )
        )
        dok = (
            f'<a class="knapp" href="?sida={urllib.parse.quote(u["dok"])}">Läs mer</a>'
            if u.get("dok") else ""
        )
        kort.append(
            f'<div class="kort"><h3>{e(u["namn"])}</h3><p>{e(u.get("beskrivning", ""))}</p>'
            f'<p>{" ".join(delar)}</p>{knapp}{dok}</div>'
        )
    return '<div class="rutnat">' + "".join(kort) + "</div>"


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
    verktyg = ["git", "uv", "python3", "node", "gh", "open-webui", "mcpo", "openclaw"]
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
    tabell = "".join(f"<tr><td>{e(k)}</td><td>{e(v)}</td></tr>" for k, v in rader)
    knapp = (
        f'<form method="post" action=""><input type="hidden" name="nonce" value="{NONCE}">'
        f'<input type="hidden" name="id" value="grund">'
        f'<input type="hidden" name="handling" value="installera">'
        f'<button type="submit">Kör om grundinstallationen</button></form>'
    )
    return f'<p>{prickar}</p><table class="tabellsvag">{tabell}</table>{knapp}'


def block_namnrymd(_: str) -> str:
    ing = labb.ingresser()
    if not ing:
        return (
            "<p><em>Kunde inte läsa ingresser. Det kräver läsrättigheter i namnrymden "
            "(<code>kubectl get ingress</code>).</em></p>"
        )
    rader = "".join(
        f'<tr><td>{e(i["namn"])}</td>'
        f'<td><a href="https://{e(i["host"])}/" target="_blank">{e(i["host"])}</a></td></tr>'
        for i in sorted(ing, key=lambda x: x["namn"])
    )
    return (
        "<table><tr><th>Tjänst i namnrymden</th><th>Adress</th></tr>" + rader + "</table>"
        "<p style='font-size:13.5px;color:var(--svag)'>Hämtat med "
        "<code>kubectl get ingress</code>. "
        "Det som ligger bakom ett inloggningsskydd svarar ändå på sin hälsokontroll.</p>"
    )


def block_atgarder(_: str) -> str:
    """Knappar för sådant som inte är en tjänst men ska gå att köra härifrån."""
    atgarder = labb.atgarder()
    if not atgarder:
        return ""
    kort = []
    for aid, a in atgarder.items():
        arbetar = labb.kors_nu(aid)
        knappar = []
        if arbetar:
            knappar.append(f'<a class="knapp" href="?logg={e(aid)}">Visa vad som händer</a>')
        else:
            knappar.append(
                f'<form method="post" action=""><input type="hidden" name="nonce" value="{NONCE}">'
                f'<input type="hidden" name="id" value="{e(aid)}">'
                f'<input type="hidden" name="handling" value="atgard">'
                f'<button type="submit" class="primar">{e(a.get("knapp", "Kör"))}</button></form>'
            )
        if a.get("dok"):
            knappar.append(f'<a class="knapp" href="?sida={urllib.parse.quote(a["dok"])}">Läs mer</a>')
        if labb.loggfil(aid, "atgard").exists():
            knappar.append(f'<a class="knapp" href="?logg={e(aid)}">Logg</a>')
        kort.append(
            f'<div class="kort"><h3>{e(a.get("namn", aid))}</h3>'
            f'<p>{e(a.get("beskrivning", ""))}</p>{"".join(knappar)}</div>'
        )
    return '<div class="rutnat">' + "".join(kort) + "</div>"


_BLOCKBYGGARE = {
    "atgarder": block_atgarder,
    "tjanster": block_tjanster,
    "uppsattningar": block_uppsattningar,
    "status": block_status,
    "miljo": block_miljo,
    "namnrymd": block_namnrymd,
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
    handlingar = ("installera", "starta", "stoppa", "uppsattning", "atgard")
    känd = (
        tjid in labb.tjanster()
        or tjid in labb.uppsattningar()
        or tjid in labb.atgarder()
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


def starta_handling(handling: str, tjid: str) -> str:
    """Startar kor.sh frånkopplat och returnerar vart vi ska skicka läsaren."""
    if handling == "uppsattning":
        if tjid not in labb.uppsattningar():
            return "?sida=docs/START.md"
        kmd = ["verktyg/kor.sh", "uppsattning", tjid]
        mal = f"?logg={urllib.parse.quote(tjid)}"
    elif handling == "atgard":
        if tjid not in labb.atgarder():
            return "?sida=docs/START.md"
        kmd = ["verktyg/kor.sh", "atgard", tjid]
        mal = f"?logg={urllib.parse.quote(tjid)}"
    else:
        if tjid not in labb.tjanster() or handling not in ("installera", "starta", "stoppa"):
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


def main() -> int:
    port = labb.panelport()
    labb.se_till_att_kataloger_finns()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Panel)
    proxy = labb.proxy_url(port)
    print(f"Labbpanelen kör på http://127.0.0.1:{port}/")
    if proxy:
        print(f"I webbläsaren:  {proxy}")
        print("I VS Code:      Ctrl+Shift+P → Simple Browser: Show → klistra in URL:en")
    print("Avsluta med Ctrl+C.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAvslutar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

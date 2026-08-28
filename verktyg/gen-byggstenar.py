#!/usr/bin/env python3
"""Genererar en SVG per byggsten, i samma stil som docs/bilder/anatomi.svg.

Lådorna är tänkta att dras in i ett skissverktyg, inte att refereras från
dokumentationen. Därför: ljust läge i presentationsattribut, inget <style>-block
och inga externa resurser — ingenting som ett importfilter kan tappa bort.

    python3 verktyg/gen-byggstenar.py       # körs från repots rot

PNG:er (dubbel upplösning, för verktyg som inte tar SVG):

    uv run --with cairosvg python -c "import cairosvg, pathlib; \
      ut = pathlib.Path('docs/bilder/byggstenar/png'); ut.mkdir(exist_ok=True); \
      [cairosvg.svg2png(url=str(f), write_to=str(ut/(f.stem+'@2x.png')), scale=2) \
       for f in pathlib.Path('docs/bilder/byggstenar').glob('*.svg')]"

Se docs/bilder/byggstenar/README.md.
"""
import pathlib, html

UT = pathlib.Path("docs/bilder/byggstenar")

B, H = 300, 64            # ruta
PAD = 1                   # plats för streckbredden
W, HH = B + 2 * PAD, H + 2 * PAD

STIL = {
    # namn:        (fyllning, kant,      titelfärg, underradsfärg, opacitet underrad)
    "ruta":        ("#f4f4f7", "#d8d8de", "#1a1a1a", "#5f5f6a", "1"),
    "bas":         ("#1b1b6e", "#1b1b6e", "#ffffff", "#ffffff", ".85"),
    "markerad":    ("#e8f0fa", "#0b5fa5", "#1a1a1a", "#0b5fa5", "1"),
}

# (filnamn, titel, underrad, stil)
BYGGSTENAR = [
    ("anvandaren",                 "Användaren",                    "har uppgiften",                        "ruta"),
    ("applikationslagret",         "Applikationslagret",            "chatt, editor, flöde",                 "ruta"),
    ("api-lagret",                 "API-lagret",                    "den kontrollerade vägen in",           "ruta"),
    ("orkestrering",               "Orkestrering",                  "håller ihop stegen",                   "ruta"),
    ("modellen",                   "Modellen",                      "resonemang och text",                  "bas"),
    ("kontext-och-minne",          "Kontext och minne",             "RAG · minnesbank · graf",              "ruta"),
    ("verktygslagret",             "Verktygslagret",                "MCP · funktioner",                     "ruta"),
    ("arbetssatt",                 "Arbetssätt",                    "skills, mallar",                       "ruta"),
    ("kallsystem-register-dokument","Källsystem, register, dokument","det som verktygen och hämtningen når",  "ruta"),
    ("sakerhet-och-behorighet",    "Säkerhet och behörighet",       "åtkomst, loggning, filtrering",        "ruta"),
    ("driftmiljon",                "Driftmiljön",                   "var det körs",                         "markerad"),
    ("utvardering",                "Utvärdering",                   "kända fall, mätning, regressionstest", "markerad"),
    ("mansklig-oversyn",           "Mänsklig översyn",              "vem granskar vad, när och hur mycket", "markerad"),
    ("livscykelhantering",         "Livscykelhantering",            "modell, prompt, index, konfiguration", "markerad"),
]

MALL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"
     font-family="system-ui,-apple-system,'Segoe UI',sans-serif" font-size="14" fill="#1a1a1a"
     role="img" aria-labelledby="titel">
<title id="titel">{titel} — {underrad}</title>
<rect x="{pad}" y="{pad}" width="{b}" height="{bh}" rx="7" fill="{fyll}" stroke="{kant}"/>
<text x="17" y="27" font-size="14" font-weight="600" fill="{tf}">{titel}</text>
<text x="17" y="44" font-size="11.5" fill="{uf}"{op}>{underrad}</text>
</svg>
'''

UT.mkdir(parents=True, exist_ok=True)
for namn, titel, underrad, stil in BYGGSTENAR:
    fyll, kant, tf, uf, op = STIL[stil]
    svg = MALL.format(
        w=W, h=HH, pad=PAD + 0.5, b=B - 1, bh=H - 1,
        fyll=fyll, kant=kant, tf=tf, uf=uf,
        op="" if op == "1" else f' opacity="{op}"',
        titel=html.escape(titel), underrad=html.escape(underrad),
    )
    (UT / f"{namn}.svg").write_text(svg, encoding="utf-8")
    print(f"{namn}.svg  {stil}")

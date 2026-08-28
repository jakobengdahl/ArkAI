---
namn: svg-css-variabler-blir-svarta
beskrivning: Färger i figurer ska ligga i presentationsattribut, inte i CSS-variabler — annars blir bilden helsvart där CSS inte körs.
typ: verktyg
uppdaterad: 2026-08-17
---

En SVG som sätter sina färger med CSS-variabler (`fill:var(--ruta)` i ett
`<style>`-block) blir en helt svart bild i varje renderare som kör CSS men inte
stöder `var()` — och klassregeln vinner över presentationsattributet, så ett
`fill="#f4f4f7"` på samma element räddar ingenting. Lägg i stället alla ljusa färger i
presentationsattribut och låt `<style>` innehålla enbart avvikelserna för
`@media (prefers-color-scheme:dark)`.

**Varför:** figurerna i `docs/bilder/` ritades först med variabler för att kunna byta
palett på ett ställe. Renderade med cairosvg blev alla sex helt svarta rektanglar.
Samma sak gäller där CSS blockeras helt: labbpanelen serverar bilder i sandlåda
(`verktyg/panel/panel.py`, `?bild=`), och GitHub serverar dem med restriktiv CSP.
Med färgerna i attribut visas den ljusa versionen korrekt i alla tre lägena.

**Så använder du det:** följ uppbyggnaden i
[docs/bilder/README.md](../../docs/bilder/README.md). Kontrollera en ny figur genom
att rendera den innan den commitas:

    uv run --with cairosvg python -c "import cairosvg; cairosvg.svg2png(url='docs/bilder/namn.svg', write_to='/tmp/namn.png')"

Blir bilden svart ligger färgen på fel ställe.

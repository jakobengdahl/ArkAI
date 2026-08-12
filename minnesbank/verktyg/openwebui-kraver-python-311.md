---
namn: openwebui-kraver-python-311
beskrivning: Open WebUI kräver Python 3.11 medan Onyxias image har 3.13 — lös det med uv i stället för att röra systemets Python.
typ: verktyg
uppdaterad: 2026-08-12
---

Open WebUI (testat med 0.11.0) kör inte på Python 3.13, som är det Onyxias
datascience-image levererar. `uv` kan hämta hem en egen 3.11 och installera verktyget
isolerat mot den, utan att påverka systemets Python:

```bash
uv python install 3.11
uv tool install --python 3.11 open-webui
export PATH="$HOME/.local/bin:$PATH"
```

**Varför:** frestelsen är att `pip install` mot systemets Python och sedan börja
tvinga versioner. Det förstör imagens miljö och går inte att återställa utan att
starta om tjänsten.

**Så använder du det:** installationen hamnar under `~/.local`, alltså på den
persistenta volymen, och överlever poddomstarter — till skillnad från allt du
installerar med `apt`. Samma mönster fungerar för andra Python-verktyg med
versionskrav som krockar med imagen.

Relaterat: [[onyxia-port-8080-upptagen]], [[onyxia-inga-k8s-rattigheter]]

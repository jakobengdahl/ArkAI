---
namn: query-strang-overlever-proxyn
beskrivning: Egna webbgränssnitt i labbet ska routa via query-strängen och ha inline-CSS — då fungerar de bakom code-servers /proxy/ utan omstart.
typ: verktyg
uppdaterad: 2026-08-13
---

Bygger du något eget med webbgränssnitt i den här miljön: **routa via query-strängen
(`?sida=…`) och lägg all CSS inline.** Då innehåller sidan inte en enda absolut
sökväg, och den fungerar oförändrad både på `127.0.0.1:port` och bakom
`https://<vscode-url>/proxy/<port>/` — utan att porten behöver exponeras och utan
att tjänsten behöver startas om.

**Varför:** färdiga appar som Open WebUI går inte att nå via code-servers proxy,
eftersom de refererar allt med rotabsoluta sökvägar och saknar stöd för bassökväg
(se [[spa-fungerar-inte-bakom-sokvagsproxy]]). Slutsatsen brukar bli "exponera
porten vid start". Men problemet ligger i appen, inte i proxyn — skriver man
själv är det trivialt att undvika. Labbpanelen byggdes så och nås utan
portexponering.

Det ger också en gratis behörighetsmodell: en tjänst som bara binder till
`127.0.0.1` kan bara nås av den som har VS Code-sessionen. Det är rimligt för
något som kan starta processer.

**Så använder du det:** en enda endpoint, `?sida=`/`?logg=`-parametrar,
`<form action="">` och relativa `Location`-headers vid omdirigering. Se
`verktyg/panel/panel.py` och [panelen.md](../../docs/60-miljo/panelen.md).

Relaterat: [[spa-fungerar-inte-bakom-sokvagsproxy]], [[onyxia-behorigheter-satts-vid-start]]

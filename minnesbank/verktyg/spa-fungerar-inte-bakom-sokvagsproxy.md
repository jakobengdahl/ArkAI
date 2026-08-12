---
namn: spa-fungerar-inte-bakom-sokvagsproxy
beskrivning: Webbappar med absoluta tillgångssökvägar (Open WebUI m.fl.) fungerar inte bakom code-servers /proxy/PORT/ — exponera porten med eget värdnamn vid tjänststart i stället.
typ: verktyg
uppdaterad: 2026-08-12
---

code-servers inbyggda proxy — `https://<vscode-url>/proxy/8081/` — fungerar bara för
appar som använder **relativa** sökvägar. Moderna enkelsidiga webbappar gör oftast
inte det. Open WebUI 0.11.0 refererar `/_app/immutable/...` och `/api/...` absolut;
proxyn strippar prefixet innan anropet går vidare, appen vet inte att den ligger under
en sökväg, och webbläsaren löser sökvägarna mot domänroten — där code-server svarar i
stället. Resultatet är en trasig sida, inte ett tydligt fel.

`/absproxy/PORT/` skickar med hela sökvägen men hjälper inte: appen kan ändå inte
hantera prefixet.

**Varför:** vi dokumenterade proxyn som en "nödutgång" för att slippa starta om
tjänsten, utan att ha provat den i en webbläsare. Någon provade, och den fungerade
inte. Kontrollen efteråt visade att den inte *kan* fungera — Open WebUI har inget
stöd för bassökväg alls (`root_path`, `BASE_PATH` och liknande ger noll träffar i
paketet), och sökvägarna är inbyggda i frontend-bygget snarare än genererade vid
körning.

Lärdomen är egentligen två: proxyn duger inte för den här sortens appar, och en
nödutgång man inte testat är inte en nödutgång.

**Så använder du det:** avgör snabbt om en app kan ligga bakom proxyn:

```bash
curl -s http://127.0.0.1:<port>/ | grep -oE '(href|src)="[^"]*"' | head -5
```

Börjar sökvägarna med `/` — glöm proxyn. Exponera porten med eget värdnamn i stället:
**Network access → "Enable access to your service through specific ports"** när
tjänsten startar. Porten får då en egen ingress med `path: /`, vilket är vad appen
förväntar sig.

Inställningen går bara att sätta vid start, se
[[onyxia-behorigheter-satts-vid-start]]. Omstarten är billig — hemkatalogen är kvar.

Relaterat: [[onyxia-port-8080-upptagen]], [[openwebui-kraver-python-311]]

---
namn: tva-portar-ar-tva-origins
beskrivning: Onyxia ger varje exponerad port ett eget värdnamn, så en webbapp med skild frontend och backend behöver en proxy i podden som delar på sökväg — inte två portar.
typ: verktyg
uppdaterad: 2026-08-28
---

Varje exponerad port i en Onyxia-tjänst får ett eget värdnamn. För en applikation som
består av en frontend och ett API är det inte två adresser till samma sak, det är
**två origins**: sessionskakan som frontenden sätter följer inte med till API:et, och
inloggningen går sönder på ett sätt som ser ut som ett behörighetsfel.

Lösningen är en liten proxy i podden — Caddy eller nginx — som lyssnar på *en*
exponerad port och delar trafiken på sökväg. Applikationens egna anvisningar för
reverse proxy brukar tala om exakt vilka sökvägar som ska till API:et; ta den listan
rakt av i stället för att uppfinna en egen topologi.

**Varför:** Eneo har frontend på 3000 och backend på 8000 och delar dem i sitt
Traefik-exempel med `Host()` + `PathPrefix()`. Två exponerade Onyxia-portar hade gett
cross-origin-kakor. Med Caddy på 8084 och samma sökvägsdelning fungerar inloggning,
strömmande svar och SSR utan ändringar i Eneo.

**Så använder du det:** se [`verktyg/eneo/Caddyfile`](../../verktyg/eneo/Caddyfile)
för mönstret. Sätt applikationens `ORIGIN`/`PUBLIC_ORIGIN` till det exponerade
värdnamnet, och `X-Forwarded-Proto: https` i proxyn — ingressen har redan terminerat
TLS, så proxyn ser bara http.

Relaterat: [[en-ingress-regel-per-port]], [[spa-fungerar-inte-bakom-sokvagsproxy]], [[exponerad-port-kraver-inloggning]]

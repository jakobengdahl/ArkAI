---
namn: onyxia-port-8080-upptagen
beskrivning: Port 8080 är upptagen av code-server i Onyxias VS Code-tjänster — starta egna tjänster på 8081 eller högre.
typ: verktyg
uppdaterad: 2026-08-12
---

I Onyxias VS Code-tjänster lyssnar code-server självt på `127.0.0.1:8080`. Startar du
något eget på 8080 får du `[Errno 98] address already in use`, eller — värre — ett
`curl` mot `localhost:8080/health` som svarar `401 Unauthorized` från code-server och
får det att se ut som om din egen tjänst startat med ett auth-problem.

**Varför:** Open WebUI har 8080 som standardport, precis som code-server. Första
starten misslyckades och felmeddelandet dolde sig i 40 sekunders uppstartsloggar.

**Så använder du det:** använd 8081 och uppåt. Kontrollera först, `ss` finns inte i
imagen som standard:

```bash
timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/8081" && echo upptagen || echo ledig
```

Relaterat: [[openwebui-kraver-python-311]], [[onyxia-inga-k8s-rattigheter]]

---
namn: en-ingress-regel-per-port
beskrivning: Exponerar du två portar lägger Onyxia båda i samma ingress med ett värdnamn per regel — kod som tar första hosten pekar fel för den andra porten.
typ: verktyg
uppdaterad: 2026-08-28
---

Exponerar en Onyxia-tjänst flera portar skapas **en** ingress (`...-user`) med **en
regel per port**, var och en med sitt eget värdnamn: `...-user-8081...` och
`...-user-8084...`. Ingressen som helhet har alltså inget värdnamn — bara reglerna
har det. Kod som läser ingressen och tar `rules[0].host` svarar därför rätt för den
port som råkar stå först och fel för alla andra.

**Varför:** `verktyg/labb.py` gjorde precis det. Med bara Open WebUI exponerad
märktes ingenting. När Eneo lades till på 8084 svarade `labb.py ingress 8084` med
8081:s värdnamn — och det värdet går rakt in i Eneos `PUBLIC_ORIGIN`, där ett fel
värdnamn ger tyst trasig inloggning i stället för ett felmeddelande.

**Så använder du det:** para ihop värdnamn och port *inom* regeln, aldrig på
ingressnivå. Kontrollera med:

```bash
kubectl get ingress <namn> -o jsonpath='{range .spec.rules[*]}{.host}{" "}{.http.paths[0].backend.service.port.number}{"\n"}{end}'
python3 verktyg/labb.py ingress 8084
```

Relaterat: [[onyxia-behorigheter-satts-vid-start]], [[exponerad-port-kraver-inloggning]], [[tva-portar-ar-tva-origins]]

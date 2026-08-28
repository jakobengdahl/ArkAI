---
namn: forbjudet-ar-inte-saknat
beskrivning: Ett Forbidden-svar från kubectl på en klusterbred fråga betyder att du inte får titta, inte att resursen saknas — fråga med api-resources och auth can-i i stället.
typ: verktyg
uppdaterad: 2026-08-28
---

I en Onyxia-namnrymd är nästan allt klusterbrett förbjudet: `kubectl get crd`,
`get nodes`, `get storageclasses` svarar `Forbidden ... at the cluster scope`. Det
säger ingenting om huruvida objektet finns. Läser man svaret som "finns inte" drar man
fel slutsats om vad miljön klarar — och bygger runt ett hinder som inte finns.

**Varför:** `kubectl get crd | grep cnpg` gav tomt, och slutsatsen blev att
CloudNativePG-operatorn saknades och att katalogens `postgresql-cnpg` därför var
stängd. Fel: `kubectl api-resources` visar hela `postgresql.cnpg.io`-familjen, och
`kubectl auth can-i create clusters.postgresql.cnpg.io` svarar `yes`.

**Så använder du det:** fråga om det du faktiskt vill veta — vad som finns och vad du
får göra — inte om att lista objekt:

```bash
kubectl api-resources | grep -i <namn>          # finns typen?
kubectl auth can-i create <typ>                 # får jag skapa den?
```

Relaterat: [[onyxia-behorigheter-satts-vid-start]], [[sondera-tillstand-las-det-inte]]

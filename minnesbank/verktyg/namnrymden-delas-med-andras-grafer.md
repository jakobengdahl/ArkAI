---
namn: namnrymden-delas-med-andras-grafer
beskrivning: Namnrymden har flera CommunityOverview-instanser som andra driver. Våra resurser heter arkai-* och tas bort på etikett, aldrig på namn.
typ: verktyg
uppdaterad: 2026-10-13
---

Labbets namnrymd innehåller flera CommunityOverview-instanser som inte är våra:
`communityoverview-<namn>-dev`, var och en med deployment, service och PVC.
Metadatagrafens pilot är en av dem. Allt vi själva deployar heter därför `arkai-*`
och bär en egen etikett `app.kubernetes.io/part-of=…`. Borttagning väljer på
etiketten och aldrig på ett namnmönster.

**Varför:** när en egen grafinstans skulle läggas till låg det nära till hands att
döpa den efter appen. Då hade `kubectl delete … communityoverview*` eller ett slarvigt
`-l app=communityoverview` kunnat radera pilotens volym. Volymerna går inte att
återskapa.

**Så använder du det:** innan du deployar något nytt, kör
`kubectl get deploy,svc,pvc -o name` och välj ett prefix som inte krockar. Mönstret
finns i `verktyg/ta-bort-graf.sh` och `verktyg/ta-bort-eneo.sh`.

Relaterat: [[namnrymden-overlever-podden]], [[forbjudet-ar-inte-saknat]], [[ny-volym-kan-fastna-i-pending]]

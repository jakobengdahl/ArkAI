---
namn: namnrymden-overlever-podden
beskrivning: Det du deployar i namnrymden fortsätter köra och ta av kvoten när VS Code-tjänsten stoppas — att stoppa podden städar ingenting.
typ: verktyg
uppdaterad: 2026-08-28
---

En Onyxia-tjänst som stoppas tar med sig sin podd, men **inte** det den deployat i
namnrymden. Deployments, StatefulSets och volymer ligger kvar, kör vidare och
fortsätter räknas mot kvoten (poddar och lagring) tills någon aktivt tar bort dem.
Det är avsiktligt — det är därför man deployar i namnrymden i stället för i podden —
men det betyder att uppstädningen är ett eget steg som ingenting påminner om.

**Varför:** Eneo kör som fem arbetslaster och två volymer i namnrymden. Startar man
en ny labbmiljö varje gång man vill prova något, och stoppar den gamla, blir kvoten
uppäten av installationer vars VS Code-tjänst inte längre finns.

**Så använder du det:** panelens startsida visar vad som ligger i namnrymden och vad
det tar av kvoten, och tjänster som labbet deployat har en *Ta bort*-knapp. I
terminalen:

```bash
python3 verktyg/labb.py namnrymd        # allt, med kvoten
verktyg/kor.sh stoppa eneo              # skalar till noll, data kvar
verktyg/kor.sh avinstallera eneo        # tar bort, inklusive volymerna
```

Skillnaden mellan de två sista är hela poängen: *stoppa* släpper poddarna men
behåller lagringen, *avinstallera* släpper båda.

Relaterat: [[onyxia-behorigheter-satts-vid-start]], [[tva-portar-ar-tva-origins]], [[forbjudet-ar-inte-saknat]]

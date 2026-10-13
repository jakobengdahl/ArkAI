---
namn: ny-volym-kan-fastna-i-pending
beskrivning: Klustrets lagring kan sluta skapa nya volymer. Prova med en tom provvolym innan du felsöker manifesten, och bygg hellre på ~/work.
typ: verktyg
uppdaterad: 2026-10-13
---

En ny PVC i namnrymden kan bli stående i `Pending` med *"Waiting for a volume to be
created either by the external provisioner 'rook-ceph.rbd.csi.ceph.com'…"*, även när
specen är identisk med bundna volymer och kvoten inte är nådd. Det är klustrets
provisioner, inte manifestet. En podd som behöver volymen schemaläggs aldrig, och
`kubectl rollout status` väntar då i en kvart utan att säga varför.

**Varför:** 2026-10-13 skulle den egna grafen köras som arbetslast med egen volym.
Volymen skapades aldrig, och inte heller en tom provvolym på 1 Gi. Volymer skapade
dagen innan var bundna. Lagringsklasser och provisionerare går inte att se med
rollen `edit`, så det finns inget mer att felsöka härifrån.

**Så använder du det:**

- Står en PVC i `Pending`: skapa en tom provvolym med samma klass. Fastnar den också
  ligger felet i klustret. Ta bort provvolymen efteråt.
- Låt installationsskript vänta på `Bound` med en kort tidsgräns innan de väntar på
  poddar — se `verktyg/installera/eneo.sh` för hur det annars ser ut.
- Behöver något bara en katalog som överlever omstart: kör det i podden och lägg data
  under `~/work`, som redan är en bunden volym. Så kör den egna grafen
  (`docs/60-miljo/egen-graf.md`).

Relaterat: [[namnrymden-overlever-podden]], [[forbjudet-ar-inte-saknat]], [[namnrymden-delas-med-andras-grafer]]

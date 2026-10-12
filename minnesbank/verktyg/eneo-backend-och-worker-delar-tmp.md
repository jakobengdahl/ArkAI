---
namn: eneo-backend-och-worker-delar-tmp
beskrivning: Eneos backend lämnar uppladdade filer till workern via en sökväg i /tmp — körs de i olika poddar misslyckas varje kunskapsuppladdning tyst.
typ: verktyg
uppdaterad: 2026-10-12
---

Eneos backend skriver en uppladdad fil till `/tmp` och lägger bara sökvägen i
jobbkön. Workern öppnar sedan samma sökväg. Backend och worker måste därför se samma
`/tmp`. I Kubernetes med ReadWriteOnce-lagring betyder det två containrar i samma
podd som delar en `emptyDir`, inte två deployments. Det gäller i 2.2.2 också, även
med objektlagring inkopplad.

**Varför:** I 2.1.1-installationen hade backend och worker var sin podd. Varje
uppladdning till en kunskapskälla misslyckades i över en månad utan att det märktes.
Backend loggade bara INFO, gränssnittet visade ingenting. Felet fanns enbart i
workerns logg: `FileNotFoundError: [Errno 2] No such file or directory: '/tmp/<id>'`.
Eneos compose-fil delar volymen, och det föll bort i översättningen till manifest.

**Så använder du det:** När en compose-fil översätts till Kubernetes, leta efter
namngivna volymer som monteras i flera tjänster. De kan inte bli en `emptyDir`
per podd. Felsök Eneo-jobb i workern, inte i backend:

    kubectl logs deploy/eneo-backend -c worker | grep -E "Job failed|ERROR"

Relaterat: [[namnrymden-overlever-podden]], [[forbjudet-ar-inte-saknat]]

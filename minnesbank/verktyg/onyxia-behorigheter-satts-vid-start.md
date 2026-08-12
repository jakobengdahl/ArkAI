---
namn: onyxia-behorigheter-satts-vid-start
beskrivning: Kubernetes-roll, portar, AI-assistent och S3/Vault sätts när en Onyxia-tjänst startar och går inte att ändra efteråt — starta om i stället för att kämpa emot.
typ: verktyg
uppdaterad: 2026-08-12
---

Nästan allt som avgör vad en Onyxia-tjänst *kan* göra sätts i startformuläret och går
inte att ändra på en körande tjänst. Det gäller Kubernetes-rollen (`view` / `edit` /
`admin` över din egen namnrymd, **standard är `view`**), vilka portar som exponeras
med egen ingress, om AI-assistenten kopplas in, och om S3- och Vault-uppgifter
monteras in.

**Varför:** vi drog först slutsatsen att plattformen inte tillät oss att deploya
saker, eftersom `kubectl auth can-i create deployments` svarade `no` och `helm list`
gav "secrets is forbidden". Det var fel orsak. Rättigheterna fanns — tjänsten hade
bara startats med standardrollen `view`. Samma misstag är lätt att göra med
portexponering: man hittar inte inställningen och börjar bygga runt problemet i
stället.

**Så använder du det:** när något inte går, kontrollera *hur tjänsten startades*
innan du letar efter en teknisk lösning. Hemkatalogen (`/home/onyxia/work`) är
persistent, så en omstart med rätt inställningar kostar några minuter och du tappar
inget arbete. Att starta om är nästan alltid rätt val.

Att komma ihåg vid start:

- **Kubernetes permissions** — `edit` om du vill deploya själv
- **Network access** — porten du tänker köra något på, t.ex. 8081
- **AI Assistant** — kopplar in plattformens LLM i opencode och Continue
- **Git** — se [[onyxia-token-i-remote-url]]

Relaterat: [[onyxia-port-8080-upptagen]], [[openwebui-kraver-python-311]], [[api-nycklar-i-hemkatalogen]]

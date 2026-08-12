---
namn: onyxia-token-i-remote-url
beskrivning: Onyxia bakar in din GitHub-token i klartext i git-remotens URL — flytta den till gh:s credential helper direkt.
typ: verktyg
uppdaterad: 2026-08-12
---

När Onyxia klonar ett repo åt dig hamnar din personliga access-token i klartext i
remote-URL:en, alltså i `.git/config`:

```
origin  https://github_pat_11ABC...@github.com/konto/repo.git
```

Samma token ligger dessutom i miljövariabeln `GIT_PERSONAL_ACCESS_TOKEN` och syns
därmed i `env` för allt som kör i podden — inklusive AI-agenter som kör kommandon åt
dig.

**Varför:** det gör att kloningen fungerar automatiskt, vilket är rimligt. Men token
följer med i varje `git remote -v`, i skärmdumpar och i klistrade terminalutdrag. I
en miljö där vi medvetet låter verktyg läsa filer och köra kommandon är det värt de
30 sekunderna att städa bort.

**Så använder du det:** kör i varje ny tjänst, direkt efter start:

```bash
./verktyg/satt-upp-git-auth.sh
```

Det loggar in `gh` med token från miljön, sätter `gh` som credential helper och
skriver om remote-URL:en. Har en token redan hunnit läcka: **spärra den först**,
städa sedan. Se [docs/60-miljo/git-och-auth.md](../../docs/60-miljo/git-och-auth.md).

Relaterat: [[publikt-repo]]

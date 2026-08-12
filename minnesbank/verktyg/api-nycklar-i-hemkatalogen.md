---
namn: api-nycklar-i-hemkatalogen
beskrivning: Onyxia skriver fungerande LLM-API-nycklar i klartext i ~/.continue/config.yaml och ~/.config/opencode/opencode.jsonc — rensa innan du delar något därifrån.
typ: verktyg
uppdaterad: 2026-08-12
---

Slår du på **AI Assistant** när en tjänst startar skriver Onyxia in modell, bas-URL
och en fungerande API-nyckel i klartext i:

- `~/.continue/config.yaml`
- `~/.config/opencode/opencode.jsonc`

Hemkatalogen är persistent och filerna är läsbara för allt som kör i podden.

**Varför:** vi råkade titta i filerna av nyfikenhet på hur AI-assistent-valet
implementeras och hittade en aktiv nyckel. Det är samma mönster som med
git-token i remote-URL:en ([[onyxia-token-i-remote-url]]) — bekvämlighet som
plattformen väljer åt dig, och som är värd att känna till snarare än att upptäcka.

**Så använder du det:** de här filerna är exempel man gärna klistrar in när man
frågar om konfiguration — i en chatt, i ett ärende, i ett dokument. Rensa nyckeln
först:

```bash
sed -E 's/(apiKey"?[[:space:]]*[:=][[:space:]]*"?)[^",]*/\1<REDIGERAD>/' ~/.continue/config.yaml
```

Samma sak gäller `env` — kör aldrig ett rått `env` i något du delar. Både
`GIT_PERSONAL_ACCESS_TOKEN`, S3-uppgifter och `VAULT_TOKEN` ligger där.

Relaterat: [[onyxia-token-i-remote-url]], [[onyxia-behorigheter-satts-vid-start]], [[publikt-repo]]

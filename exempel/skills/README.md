# Skills

Exempel på arbetssätt paketerade som skills — instruktioner som ett AI-verktyg laddar
in när uppgiften kräver det.

Se [docs/20-tekniker/skills.md](../../docs/20-tekniker/skills.md) för vad skills är
och när de passar.

| Skill | Vad den gör |
|---|---|
| [granska-teknikbeskrivning/](granska-teknikbeskrivning/) | Granskar en fil i `docs/20-tekniker/` mot repots form |

## Formatet

En skill är en katalog med en `SKILL.md`. Frontmatter innehåller `name` och
`description`; resten är instruktionerna.

**`description` avgör om skillen används överhuvudtaget.** Den ligger alltid i
kontexten; innehållet laddas bara när verktyget bedömer att den är relevant. Skriv
den som ett svar på "när ska det här användas?" — och skriv gärna ut när den *inte*
ska användas, det är ofta det som gör valet tydligt.

En skill med bra innehåll och vag beskrivning laddas aldrig.

## Verktygsstöd

Formaten skiljer sig mellan verktyg. Claude Code letar i `.claude/skills/`, andra
verktyg har sina motsvarigheter. Katalogen här är verktygsoberoende — kopiera eller
symlänka dit ditt verktyg letar.

Att samma skill ska fungera i flera verktyg utan parallellt underhåll är en öppen
fråga. Se [docs/20-tekniker/skills.md](../../docs/20-tekniker/skills.md).

## Att skriva en egen

Ta ett arbetsmoment som görs ofta och har en form vi bryr oss om. Skriv ner hur det
går till, tillräckligt tydligt för att någon annan ska kunna följa det.

Det är nyttigt arbete oavsett AI — vilket också är varför det tar tid.

Mätpunkten för om en skill fungerar är inte om svaret blev bättre, utan om **två
personer får jämförbara resultat**. Det är den effekt skills faktiskt ger.

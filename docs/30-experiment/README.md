# Experiment

Ett experiment = en fil = ett svar.

Ett experiment ska gå att göra på en förmiddag. Blir det större är det förmodligen
flera experiment, eller en fråga som inte är tillräckligt vass än.

## Regeln

**Skriv slutsatsen först, och skriv den även när svaret är nej.**

Ett misslyckat experiment som inte dokumenteras kommer att göras om — inte för att
någon är slarvig, utan för att idén var rimlig. Det är därför den provades. Nästa
person får samma rimliga idé om ett halvår.

Se [minnesbanken om varför](../../minnesbank/arbetssatt/dokumentera-negativa-resultat.md).

## Namngivning

`EXP-NNN-kort-namn.md`, löpnummer. Återanvänd inte ett nummer.

## Arbetsgång

```bash
git switch -c exp/kort-namn
cp docs/30-experiment/MALL-experiment.md docs/30-experiment/EXP-NNN-kort-namn.md
# ... kör experimentet, skriv medan du gör det ...
./verktyg/kontrollera-innehall.sh
gh pr create --fill
```

Skriv medan du kör, inte efteråt. Detaljerna som är värda något — versionsnummer,
felmeddelandet, vad du provade som inte funkade — är borta efter en dag.

## När du är klar

Uppdatera tre saker utöver experimentfilen:

1. **Tabellen nedan.**
2. **[40-matchning/matris.md](../40-matchning/matris.md)** om du lärde dig något om
   vilken teknik som passar vilket användningsfall.
3. **[minnesbanken](../../minnesbank/)** om du lärde dig något som nästa person
   behöver veta *innan* de börjar.

Punkt 3 är hela poängen. Experimentet är berättelsen om vad som hände; minnesposten
är instruktionen till framtiden. Bara den ena överlever.

## Genomförda

| Nr | Experiment | Slutsats |
|---|---|---|
| [001](EXP-001-openwebui-i-onyxia.md) | Kan Open WebUI köras i en Onyxia-tjänst? | Ja, med `uv` och Python 3.11 på port 8081 |

## På tur

Ingen ordning, ingen som äger dem än. Ta något och skriv upp dig i en PR.

**Miljö och grunder**
- Peka Open WebUI mot [plattformens LLM-inferens](../60-miljo/sspcloud-llm.md) och
  jämför mot en extern modell på samma uppgift
- Nå Open WebUI via egen ingress i stället för code-servers proxy — bekräfta att
  portinställningen vid start fungerar som dokumenterat

**MCP och verktyg**
- Bygg [hello-mcp](../../exempel/mcp/hello-mcp/) och koppla in den i Continue,
  opencode och Open WebUI. Vad skiljer?
- Exponera ett befintligt CLI som MCP-verktyg — hur mycket arbete är det egentligen?
- Hur många verktyg kan kopplas in innan modellen börjar välja fel?

**Minne**
- Kör en session med minnesbanken inladdad mot en utan. Märks skillnaden på en
  riktig uppgift?
- Lägg 20–30 minnesposter i Neo4j och ställ tre frågor textindexet inte klarar
- Låt en modell skriva minnesposter i en vecka och granska vad som hamnade där

**Agentupplägg**
- Kör [Hermes](../20-tekniker/agentupplagg.md) mot plattformens inferens — vad hamnar
  i dess minne, och håller det?
- Kör [OpenClaw](../20-tekniker/agentupplagg.md) mot en chattkanal — ändras
  användningen av att agenten når en där kollegorna finns?
- Samma uppgift genom opencode, Continue och en kodagent till — vad skiljer?

**Pröva kartan** — varje punkt prövar en cell i
[typfall-och-byggstenar.md](../40-matchning/typfall-och-byggstenar.md)
- Samma uppgift med och utan hämtning mot eget material. Hur mycket av kvaliteten
  kom från underlaget och hur mycket från modellen?
- Samma flerstegsuppgift som chattbot respektive som agent. Vad vinner agenten, och
  vad blir svårare att felsöka?
- Samma uppgift på en liten och en stor modell. Var går gränsen där den mindre inte
  räcker? Svarar på en kostnads- och miljöfråga samtidigt
- Ta fram tio utvärderingsfall för en uppgift utan facit. Hur lång tid tog det, och
  gick det alls?

**Utforskande spår** — se [UF-002](../10-anvandningsfall/UF-002-stod-vid-byte-av-arbetsplattform.md)
- Låt en kodagent migrera en konstruerad äldre lösning till ett nytt mönster. Går
  ändringarna att granska på mindre tid än det tar att göra dem själv?
- Samma sak, men med våra egna riktlinjer och mallar inlagda som kunskapsunderlag.
  Vad ändras?
- Låt ett agentupplägg upptäcka avvikelser mellan vad koden gör och vad
  dokumentationen påstår. Var går gränsen mot att också få rätta dem?

**Mot produktion**
- Sätt upp Langfuse från katalogen och spåra en session. Vad går att svara på
  efteråt som annars inte gick?

# Starta labbet

Labbet startas med en **URL**. Den innehåller alla inställningar som måste sättas
när tjänsten skapas — port, minne, startskript, hemligheter — och som inte går att
ändra i efterhand. Klickar du på länken får du samma miljö som alla andra.

Det är hela poängen: "prova chattbot + verktyg" ska vara en länk, inte en
installationsanvisning.

## Innan första gången: lägg dina uppgifter i Vault

Onyxia har en inbyggd hemlighetshanterare. Hemligheten monteras in som
miljövariabler i tjänsten när den startar, vilket är hur nycklar och lösenord når
labbet **utan att någonsin ligga i repot**.

1. Hämta din API-nyckel till plattformens LLM-inferens.
   I [chattgränssnittet](https://llm.lab.sspcloud.fr): **Settings → Account →
   API Keys → Show**. Se [sspcloud-llm.md](sspcloud-llm.md).

2. Gå till **My Secrets** i SSP Cloud och skapa en hemlighet som heter
   `arkai-hemligheter` med de här variablerna:

   | Variabel | Värde |
   |---|---|
   | `OPENAI_API_KEY` | nyckeln från steg 1 |
   | `OPENAI_BASE_URL` | `https://llm.lab.sspcloud.fr/api` |
   | `OPENAI_MODEL` | modellnamnet du vill använda |
   | `METADATAGRAF_URL` | adressen till pilotinstansen av metadatagrafen |
   | `METADATAGRAF_TOKEN` | bearer-token för dess MCP-server |
   | `METADATAGRAF_BASIC` | `användare:lösenord` till dess webbgränssnitt |

   De tre sista behövs bara om du ska jobba mot metadatagrafen — se
   [metadatagrafen.md](metadatagrafen.md). Uppgifterna delas ut av den som driver
   piloten; de står inte här, eftersom repot är publikt.

3. Referera hemligheten i startformuläret (`vault.secret`) eller låt URL:en nedan
   göra det åt dig.

Byter du nyckel räcker det att uppdatera hemligheten och starta om tjänsten.

## URL:en

```
https://datalab.sspcloud.fr/launcher/ide/vscode-python
  ?autoLaunch=true
  &name=«arkai»
  &init.personalInit=«https://raw.githubusercontent.com/jakobengdahl/ArkAI/main/verktyg/onyxia-init.sh»
  &init.personalInitArgs=«bas openwebui»
  &git.repository=«https://github.com/jakobengdahl/ArkAI.git»
  &vault.secret=«arkai-hemligheter»
  &networking.user.enabled=true
  &networking.user.ports[0]=8081
  &kubernetes.role=«edit»
  &resources.limits.memory=«16Gi»
```

(En riktig URL står på en rad, och värden inom `«…»` URL-kodas. Onyxias
launcher-länkar följer samma mönster som andra projekt i SSP Cloud använder.)

| Parameter | Varför |
|---|---|
| `init.personalInit` | Startskriptet, hämtat direkt från `main`. Se nedan. |
| `init.personalInitArgs` | Profil: vilka tjänster som ska förinstalleras |
| `git.repository` | Repot klonas automatiskt till `~/work/ArkAI` |
| `vault.secret` | Hemligheten monteras som miljövariabler |
| `networking.user.ports[0]` | **8081 för Open WebUI.** Går inte att ändra i efterhand |
| `kubernetes.role` | `edit` om du vill kunna deploya i din namnrymd, annars `view` |
| `resources.limits.memory` | 16 GB räcker gott för det vi gör |

### Profiler

Argumentet till startskriptet styr vad som installeras automatiskt:

| Profil | Vad du får |
|---|---|
| `bas` | Panelen, Node, gh, git-auth. Under en minut |
| `bas openwebui` | Dessutom Open WebUI (~4 min). **Standardvalet** |
| `minimal` | Bara panelen — installera resten själv därifrån |

Orden är tjänst-id ur [`verktyg/labb.toml`](../../verktyg/labb.toml), så
`hello-mcp openclaw` fungerar också. `bas` är bara en etikett — grundmiljön
installeras ändå, eftersom den har `steg = "auto"` i manifestet. `minimal` är
det enda ordet med särskild betydelse: det hoppar över allt.

Allt annat installeras med en knapp i panelen när du behöver det. Du behöver alltså
inte välja rätt profil från början.

### Fler portar

En port måste exponeras **vid start** för att bli nåbar utifrån. Lägg till fler med
`networking.user.ports[1]=…`:

| Port | Tjänst | Behövs utifrån? |
|---|---|---|
| 8081 | Open WebUI | **Ja** — appen fungerar inte bakom en sökvägsproxy |
| 18789 | OpenClaw gateway | Ja, om du vill nå dess gränssnitt |
| 8082 | Labbpanelen | Nej — nås via code-servers proxy, och ska inte ligga öppet |
| 8083 | MCP-bryggan | Nej — bara Open WebUI i samma podd anropar den |

## Vad som händer när du klickat

| När | Vad | Hur lång tid |
|---|---|---|
| Tjänsten startar | `onyxia-init.sh` skriver inställningar och startar panelen | ~2 sekunder |
| VS Code öppnas | En terminal öppnas automatiskt och installerar grunden | ~10 sekunder |
| Strax därefter | Samma terminal installerar Open WebUI | ~4 minuter |
| Hela tiden | Panelen är igång och visar vad som pågår | — |

Startskriptet gör med flit **ingenting tungt**. Tjänsten blir inte tillgänglig
förrän det är klart, så allt som tar tid ligger i terminalfönstret i stället — där
du kan se det, och där det inte hindrar dig från att börja jobba.

Öppna panelen med `Ctrl+Shift+P` → *Simple Browser: Show* och URL:en som skrivs ut
i terminalen. Se [panelen.md](panelen.md).

## Om terminalen inte öppnas av sig själv

VS Code kör automatiska tasks bara om det är tillåtet. Startskriptet sätter
inställningen åt dig, men skulle den inte ha slagit igenom:

```
Ctrl+Shift+P → "Tasks: Run Task" → "Labbet: installera"
```

Panelen kör ändå — den startas av startskriptet, inte av tasken — och har en knapp
för grundinstallationen.

## Utan URL

Startar du en vanlig VS Code-tjänst från katalogen och klonar repot för hand:

```bash
cd ~/work/ArkAI
verktyg/labb-start.sh        # installerar grunden och startar panelen
```

Då får du allt utom det som måste bestämmas vid start: exponerade portar och
Vault-hemligheten. Open WebUI går att köra, men bara nås från terminalen.

## Att starta om är billigt

Hemkatalogen är persistent. Installerade verktyg, `~/work/.labb/` och repot ligger
kvar, och andra gången tar grundinstallationen sekunder i stället för minuter.
Behöver du en port du inte exponerade — starta om med rätt URL i stället för att
leta efter en teknisk lösning. Se
[minnesbanken](../../minnesbank/verktyg/onyxia-behorigheter-satts-vid-start.md).

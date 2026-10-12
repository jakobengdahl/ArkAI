# Starta labbet

Labbet startas med en **URL**. Den innehåller alla inställningar som måste sättas
när tjänsten skapas — port, minne, startskript, hemligheter — och som inte går att
ändra i efterhand. Klickar du på länken får du samma miljö som alla andra.

Det är hela poängen: "prova en AI-plattform med egna verktyg" ska vara en länk,
inte en installationsanvisning.

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
  &version=2.6.2
  &s3=default
  &init.personalInit=«https://raw.githubusercontent.com/jakobengdahl/ArkAI/main/verktyg/onyxia-init.sh»
  &init.personalInitArgs=«bas»
  &git.repository=«https://github.com/jakobengdahl/ArkAI.git»
  &git.branch=«main»
  &git.asCodeServerRoot=true
  &vault.secret=«arkai-hemligheter»
  &kubernetes.role=«edit»
  &networking.user.enabled=true
  &networking.user.ports[0]=8081
  &networking.user.ports[1]=8084
  &resources.requests.memory=«6Gi»
  &resources.limits.cpu=«15600m»
  &persistence.size=«50Gi»
```

(En riktig URL står på en rad, och värden inom `«…»` URL-kodas. Onyxias
launcher-länkar följer samma mönster som andra projekt i SSP Cloud använder.)

| Parameter | Varför |
|---|---|
| `init.personalInit` | Startskriptet, hämtat direkt från `main`. Se nedan. |
| `init.personalInitArgs` | Profil: vilka tjänster som ska förinstalleras |
| `git.repository` + `git.branch` | Repot klonas till `~/work/ArkAI`. Utan `branch` klonas standardgrenen |
| `git.asCodeServerRoot` | VS Code öppnar repot i stället för `~/work` — tasks och panel fungerar i båda fallen |
| `vault.secret` | Hemligheten monteras som miljövariabler |
| `kubernetes.role` | **`edit`.** Krävs för att kunna deploya Eneo i namnrymden. Standard är `view` |
| `networking.user.ports[0]` | **8081 för Hello-MCP över HTTP** — det är så Eneo når den. Går inte att ändra i efterhand |
| `networking.user.ports[1]` | **8084 för Eneo.** Detsamma |
| `version` | Chart-versionen. Pinnad så att alla får samma tjänst |
| `s3` | Kopplar in plattformens objektlagring |
| `resources.*` | 6 GiB begärt minne och gott om CPU. Eneo kör i namnrymden och tar inte av podden |
| `persistence.size` | 50 GiB. Mest för uv-cache och modellhämtningar — Eneos data ligger på egna volymer |

### Profiler

Argumentet till startskriptet styr vad som installeras automatiskt:

| Profil | Vad du får |
|---|---|
| `bas` | Panelen, Node, gh, git-auth. Under en minut. **Standardvalet** |
| `bas eneo` | Dessutom Eneo, deployat i namnrymden (~3 min) |
| `bas eneo hello-mcp` | Dessutom MCP-servern, redo att kopplas in i Eneo |
| `minimal` | Bara panelen — installera resten själv därifrån |

Orden är tjänst-id ur [`verktyg/labb.toml`](../../verktyg/labb.toml), så
`openclaw` fungerar också. `bas` är bara en etikett — grundmiljön installeras
ändå, eftersom den har `steg = "auto"` i manifestet. `minimal` är det enda ordet
med särskild betydelse: det hoppar över allt.

**Standardprofilen installerar inte Eneo.** Det är ett medvetet val: Eneo är sex
poddar i namnrymden som fortsätter kosta även när ingen använder dem, och en miljö
som startas för att titta på något annat ska inte dra igång dem. Ett klick i panelen
räcker när du vill ha dem — och *Stoppa* tar ner dem igen utan att förlora något.
Tjänster med `avvecklas = true` installeras aldrig automatiskt, inte ens om profilen
räknar upp dem.

Allt annat installeras med en knapp i panelen när du behöver det. Du behöver alltså
inte välja rätt profil från början.

### Fler portar

En port måste exponeras **vid start** för att bli nåbar utifrån. Lägg till fler med
`networking.user.ports[1]=…`:

| Port | Tjänst | Behövs utifrån? |
|---|---|---|
| 8081 | Hello-MCP över HTTP | **Ja** — Eneo kör i en annan podd och når den bara via ingressen |
| 8084 | Eneo | **Ja** — och det är där hela Eneo ligger, både gränssnitt och API |
| 18789 | OpenClaw gateway | Ja, om du vill nå dess gränssnitt |
| 8082 | Labbpanelen | Nej — nås via code-servers proxy, och ska inte ligga öppet |
| 8083 | MCP-bryggan (mcpo) | Nej — bara klienter i samma podd anropar den |

En exponerad port är ett **publikt värdnamn**, inte bara en väg in för dig. Allt som
läggs där behöver sitt eget skydd: Eneo har sin inloggning, Hello-MCP en token. Se
[minnesbanken](../../minnesbank/verktyg/exponerad-port-kraver-inloggning.md).

## Vad som händer när du klickat

| När | Vad | Hur lång tid |
|---|---|---|
| Tjänsten startar | `onyxia-init.sh` skriver inställningar, startar panelen och sätter igång installationen i bakgrunden | ~2 sekunder |
| Direkt därefter | Grunden och det profilen ber om installeras — **utan att du öppnar VS Code** | ~10 sekunder till ~5 minuter |
| Samma körning | Det som är installerat startas, och Eneo får sina modeller inkopplade | ~30 sekunder |
| Öppnar du VS Code | En terminal visar samma körning — den startar ingen ny | — |

Startskriptet gör med flit **ingenting tungt** själv: det startar installationen
frånkopplad och avslutar. Tjänsten blir alltså tillgänglig efter några sekunder,
och installationen fortsätter i bakgrunden. Loggen ligger i
`~/work/.labb/logg/labb-start.log`.

**Med profilen `bas eneo` behöver du inte öppna VS Code alls.** När installationen
är klar fungerar länken *Port 8084* på tjänstens sida i Onyxia — den går direkt till
Eneos inloggning. Innan dess ger den `502 Bad Gateway`; vänta och ladda om.
Inloggningen står i [eneo.md](eneo.md#köra-det).

Öppna panelen med `Ctrl+Shift+P` → *Simple Browser: Show* och URL:en som skrivs ut
i terminalen. Se [panelen.md](panelen.md).

## Om terminalen inte öppnas av sig själv

VS Code kör automatiska tasks bara om det är tillåtet. Startskriptet sätter
inställningen åt dig, men skulle den inte ha slagit igenom:

```
Ctrl+Shift+P → "Tasks: Run Task" → "Labbet: installera"
```

Panelen och installationen kör ändå — de startas av startskriptet, inte av
tasken. Tasken visar bara körningen.

## Utan URL

Startar du en vanlig VS Code-tjänst från katalogen och klonar repot för hand:

```bash
cd ~/work/ArkAI
verktyg/labb-start.sh        # installerar grunden och startar panelen
```

Då får du allt utom det som måste bestämmas vid start: Kubernetes-rollen, exponerade
portar och Vault-hemligheten. Utan `kubernetes.role=edit` går Eneo inte att
installera alls, och utan exponerad port når du varken Eneo utifrån eller
Hello-MCP från Eneo.

## Det du startat i namnrymden lever vidare

Eneo kör inte i podden utan som egna arbetslaster i namnrymden. Det är avsiktligt —
det är så en plattform ska köras, och det är därför den överlever en poddomstart —
men det betyder också att **den fortsätter köra och ta av kvoten när du stoppar
VS Code-tjänsten**. Panelens startsida visar vad du har igång och vad det kostar, och
tjänstekortet har en *Ta bort*-knapp. Se
[eneo.md](eneo.md#ta-bort-eneo-igen) och
[minnesbanken](../../minnesbank/verktyg/namnrymden-overlever-podden.md).

## Att starta om är billigt

Hemkatalogen är persistent. Installerade verktyg, `~/work/.labb/` och repot ligger
kvar, och andra gången tar grundinstallationen sekunder i stället för minuter.
Behöver du en port du inte exponerade — starta om med rätt URL i stället för att
leta efter en teknisk lösning. Se
[minnesbanken](../../minnesbank/verktyg/onyxia-behorigheter-satts-vid-start.md).

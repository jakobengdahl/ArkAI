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

**Klicka på länken** — du behöver ha gjort steget ovan med Vault först:

- **[Starta labbet med Eneo](https://datalab.sspcloud.fr/launcher/ide/vscode-python?autoLaunch=true&name=%C2%ABarkai%C2%BB&version=2.6.2&s3=default&init.personalInit=%C2%ABhttps%3A%2F%2Fraw.githubusercontent.com%2Fjakobengdahl%2FArkAI%2Fmain%2Fverktyg%2Fonyxia-init.sh%C2%BB&init.personalInitArgs=%C2%ABbas%20eneo%C2%BB&git.repository=%C2%ABhttps%3A%2F%2Fgithub.com%2Fjakobengdahl%2FArkAI.git%C2%BB&git.branch=%C2%ABmain%C2%BB&git.asCodeServerRoot=true&vault.secret=%C2%ABarkai-hemligheter%C2%BB&kubernetes.role=%C2%ABedit%C2%BB&networking.user.enabled=true&networking.user.ports[0]=8081&networking.user.ports[1]=8084&networking.user.ports[2]=8085&resources.requests.memory=%C2%AB6Gi%C2%BB&resources.limits.cpu=%C2%AB15600m%C2%BB&persistence.size=%C2%AB50Gi%C2%BB) ** — rekommenderad. Profil `bas eneo`.
  Eneo installeras, startas och får plattformens modeller inkopplade, utan att du
  öppnar VS Code.
- [Starta labbet med Eneo och egen graf](https://datalab.sspcloud.fr/launcher/ide/vscode-python?autoLaunch=true&name=%C2%ABarkai%C2%BB&version=2.6.2&s3=default&init.personalInit=%C2%ABhttps%3A%2F%2Fraw.githubusercontent.com%2Fjakobengdahl%2FArkAI%2Fmain%2Fverktyg%2Fonyxia-init.sh%C2%BB&init.personalInitArgs=%C2%ABbas%20eneo%20graf%C2%BB&git.repository=%C2%ABhttps%3A%2F%2Fgithub.com%2Fjakobengdahl%2FArkAI.git%C2%BB&git.branch=%C2%ABmain%C2%BB&git.asCodeServerRoot=true&vault.secret=%C2%ABarkai-hemligheter%C2%BB&kubernetes.role=%C2%ABedit%C2%BB&networking.user.enabled=true&networking.user.ports[0]=8081&networking.user.ports[1]=8084&networking.user.ports[2]=8085&resources.requests.memory=%C2%AB6Gi%C2%BB&resources.limits.cpu=%C2%AB15600m%C2%BB&persistence.size=%C2%AB50Gi%C2%BB) — profil `bas eneo graf`. Som
  ovan, plus en egen instans av grafappen med eget schema, inkopplad i Eneo. Se
  [egen-graf.md](egen-graf.md).
- [Starta labbet utan Eneo](https://datalab.sspcloud.fr/launcher/ide/vscode-python?autoLaunch=true&name=%C2%ABarkai%C2%BB&version=2.6.2&s3=default&init.personalInit=%C2%ABhttps%3A%2F%2Fraw.githubusercontent.com%2Fjakobengdahl%2FArkAI%2Fmain%2Fverktyg%2Fonyxia-init.sh%C2%BB&init.personalInitArgs=%C2%ABbas%C2%BB&git.repository=%C2%ABhttps%3A%2F%2Fgithub.com%2Fjakobengdahl%2FArkAI.git%C2%BB&git.branch=%C2%ABmain%C2%BB&git.asCodeServerRoot=true&vault.secret=%C2%ABarkai-hemligheter%C2%BB&kubernetes.role=%C2%ABedit%C2%BB&networking.user.enabled=true&networking.user.ports[0]=8081&networking.user.ports[1]=8084&networking.user.ports[2]=8085&resources.requests.memory=%C2%AB6Gi%C2%BB&resources.limits.cpu=%C2%AB15600m%C2%BB&persistence.size=%C2%AB50Gi%C2%BB) — profil `bas`. Bara panelen och
  grundverktygen. Eneo installeras med en knapp i panelen när du behöver det.

### Efter att du klickat

1. Onyxia startar tjänsten. Vänta tills den står som *Running* — under en minut.
2. Vänta ytterligare **5–10 minuter** första gången. Eneo installeras i bakgrunden.
3. Öppna tjänsten i Onyxia (*Open*) och klicka på länken **Port 8084**.
   Ger den `502 Bad Gateway` är installationen inte klar — vänta och ladda om.
4. Logga in med `arkai@arkai.se` som både användarnamn och lösenord.
   Modellerna finns redan: `gemma4-26b-moe` (standard), `qwen3-8-27b`,
   `qwen3-6-35b-moe` och embeddingmodellen `qwen3-embedding-8b`.

Saknas modellerna har nyckeln inte kommit med från Vault. Kontrollera hemligheten,
och tryck *Koppla in modellerna* på Eneos kort i panelen — eller starta om tjänsten.

VS Code behövs bara om du vill se installationen, läsa dokumentationen i panelen
eller arbeta i repot. Panelen nås från VS Code; adressen skrivs ut i terminalen.

### Vad länken innehåller

Uppdelad på rader:

```
https://datalab.sspcloud.fr/launcher/ide/vscode-python
  ?autoLaunch=true
  &name=«arkai»
  &version=2.6.2
  &s3=default
  &init.personalInit=«https://raw.githubusercontent.com/jakobengdahl/ArkAI/main/verktyg/onyxia-init.sh»
  &init.personalInitArgs=«bas eneo»
  &git.repository=«https://github.com/jakobengdahl/ArkAI.git»
  &git.branch=«main»
  &git.asCodeServerRoot=true
  &vault.secret=«arkai-hemligheter»
  &kubernetes.role=«edit»
  &networking.user.enabled=true
  &networking.user.ports[0]=8081
  &networking.user.ports[1]=8084
  &networking.user.ports[2]=8085
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
| `networking.user.ports[2]` | **8085 för den egna grafen.** Med i alla länkar, eftersom den inte går att lägga till senare |
| `version` | Chart-versionen. Pinnad så att alla får samma tjänst |
| `s3` | Kopplar in plattformens objektlagring |
| `resources.*` | 6 GiB begärt minne och gott om CPU. Eneo kör i namnrymden och tar inte av podden |
| `persistence.size` | 50 GiB. Mest för uv-cache och modellhämtningar — Eneos data ligger på egna volymer |

### Profiler

Argumentet till startskriptet styr vad som installeras automatiskt:

| Profil | Vad du får |
|---|---|
| `bas` | Panelen, Node, gh, git-auth. Under en minut |
| `bas eneo` | Dessutom Eneo, startat och med modellerna inkopplade (~5–10 min). **Rekommenderad** |
| `bas eneo graf` | Dessutom en egen graf med eget schema, inkopplad i Eneo. Se [egen-graf.md](egen-graf.md) |
| `bas eneo hello-mcp` | Dessutom MCP-servern, redo att kopplas in i Eneo |
| `minimal` | Bara panelen — installera resten själv därifrån |

Orden är tjänst-id ur [`verktyg/labb.toml`](../../verktyg/labb.toml), så
`openclaw` fungerar också. `bas` är bara en etikett — grundmiljön installeras
ändå, eftersom den har `steg = "auto"` i manifestet. `minimal` är det enda ordet
med särskild betydelse: det hoppar över allt.

**`bas eneo` är den rekommenderade profilen**, eftersom Eneo är det de flesta vill
prova. Eneo är fem arbetslaster i namnrymden som fortsätter kosta även när ingen
använder dem — även efter att VS Code-tjänsten stoppats. Startar du miljön för att
titta på något annat, använd länken utan Eneo. *Stoppa* på Eneos kort tar ner
poddarna utan att förlora något, och *Ta bort* tar bort allt.
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
| 8085 | Egen graf | Ja, för webbgränssnittet. Eneo försöker först nå grafen inne i namnrymden |
| 18789 | OpenClaw gateway | Ja, om du vill nå dess gränssnitt |
| 8082 | Labbpanelen | Nej — nås via code-servers proxy, och ska inte ligga öppet |
| 8083 | MCP-bryggan (mcpo) | Nej — bara klienter i samma podd anropar den |

En exponerad port är ett **publikt värdnamn**, inte bara en väg in för dig. Allt som
läggs där behöver sitt eget skydd: Eneo och den egna grafen har sin inloggning, Hello-MCP en token. Se
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

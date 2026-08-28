# Labbmiljön

Allt om SSP Cloud/Onyxia, verktygen och hur man får saker att köra.

| Fil | Vad det är |
|---|---|
| [starta-labbet.md](starta-labbet.md) | **Börja här.** URL:en som startar miljön, Vault-hemligheten, profilerna |
| [panelen.md](panelen.md) | Labbpanelen: dokumentationen renderad plus knappar för det som går att köra |
| [sspcloud-onyxia.md](sspcloud-onyxia.md) | Plattformen: tjänster, behörigheter, S3, Vault |
| [git-och-auth.md](git-och-auth.md) | Git, GitHub CLI, tokens — och fallgropen med token i remote-URL:en |
| [verktygslada.md](verktygslada.md) | Vad som installeras hur, och vad som överlever en omstart |
| [sspcloud-llm.md](sspcloud-llm.md) | Plattformens LLM-inferens och API-nyckel |
| [ai-verktyg-i-imagen.md](ai-verktyg-i-imagen.md) | opencode och Continue är förinstallerade |
| [openwebui.md](openwebui.md) | Open WebUI: installation, start, åtkomst |
| [eneo.md](eneo.md) | Eneo som alternativ till Open WebUI — förutsättningar och plan. Kräver en miljö startad med andra inställningar |
| [metadatagrafen.md](metadatagrafen.md) | Pilotinstansen med metadata som graf, och dess MCP-server |
| [delade-resurser.md](delade-resurser.md) | Projekt, S3, Vault — hur vi delar med varandra |

## I en ny tjänst

Startade du via [labbets URL](starta-labbet.md) är allt redan gjort: panelen kör,
och installationen pågår i ett terminalfönster. Annars:

```bash
cd ~/work/ArkAI
./verktyg/labb-start.sh            # installerar grunden och startar panelen
```

Vill du se vad som finns utan att ändra något:

```bash
./verktyg/kontrollera-miljo.sh     # vad finns, vad saknas
./verktyg/kor.sh status            # vad är installerat och vad kör
```

Verktygen installeras under `~/.local`, alltså på den persistenta volymen. Andra
gången du startar en tjänst tar grundinstallationen sekunder — se
[verktygslada.md](verktygslada.md).

## Tre saker som brukar överraska

**Port 8080 är upptagen** av code-server. Använd 8081 och uppåt.

**Behörigheter sätts när tjänsten startar.** Kubernetes-roll, exponerade portar,
AI-assistent — inget av det går att ändra i efterhand. Går något inte, kontrollera
hur tjänsten startades innan du letar efter en teknisk lösning.

**`apt`-installationer försvinner** vid omstart. `~/.local` och `~/work` är kvar.

Detsamma står i [minnesbanken](../../minnesbank/MINNE.md), som är den version
AI-verktygen läser.

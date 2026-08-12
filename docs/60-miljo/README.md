# Labbmiljön

Allt om SSP Cloud/Onyxia, verktygen och hur man får saker att köra.

| Fil | Vad det är |
|---|---|
| [sspcloud-onyxia.md](sspcloud-onyxia.md) | Plattformen: tjänster, behörigheter, S3, Vault |
| [git-och-auth.md](git-och-auth.md) | Git, GitHub CLI, tokens — och fallgropen med token i remote-URL:en |
| [verktygslada.md](verktygslada.md) | Installera om verktygen efter en omstart |
| [sspcloud-llm.md](sspcloud-llm.md) | Plattformens LLM-inferens och API-nyckel |
| [ai-verktyg-i-imagen.md](ai-verktyg-i-imagen.md) | opencode och Continue är förinstallerade |
| [openwebui.md](openwebui.md) | Open WebUI: installation, start, åtkomst |
| [delade-resurser.md](delade-resurser.md) | Projekt, S3, Vault — hur vi delar med varandra |

## I en ny tjänst

```bash
cd ~/work/ArkAI
./verktyg/kontrollera-miljo.sh      # vad finns, vad saknas
./verktyg/satt-upp-git-auth.sh      # git + gh, token ur remote-URL:en
export PATH="$HOME/.local/bin:$PATH"
```

Bara `gh`, `node` och nätverksverktygen behöver installeras om — se
[verktygslada.md](verktygslada.md). Resten ligger persistent under `~/`.

## Tre saker som brukar överraska

**Port 8080 är upptagen** av code-server. Använd 8081 och uppåt.

**Behörigheter sätts när tjänsten startar.** Kubernetes-roll, exponerade portar,
AI-assistent — inget av det går att ändra i efterhand. Går något inte, kontrollera
hur tjänsten startades innan du letar efter en teknisk lösning.

**`apt`-installationer försvinner** vid omstart. `~/.local` och `~/work` är kvar.

Detsamma står i [minnesbanken](../../minnesbank/MINNE.md), som är den version
AI-verktygen läser.

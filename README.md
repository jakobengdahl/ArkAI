# ArkAI

En öppen experimentyta för att lära oss vad AI faktiskt kan göra i vårt arbete med
arkitektur — och vad som krävs för att ta det hela vägen från demo till drift.

Repot är **publikt**. Läs [RIKTLINJER-INNEHALL.md](RIKTLINJER-INNEHALL.md) innan du
skriver något här. Kort version: inga verksamhetsinterna detaljer, inga namn på
personer eller system, inga hemligheter. Vi beskriver *mönster*, inte vår verksamhet.

## Vad vi försöker ta reda på

1. **Vilka användningsfall** i vårt arbete tjänar på AI — och vilka gör det inte?
2. **Vilka AI-tekniker** finns, och vad är de faktiskt bra på?
   (chattbot + verktyg via MCP/CLI, minnesbanker, kodagenter, skills, RAG, grafer …)
3. **Hur matchar man rätt teknik mot rätt användningsfall?**
4. **Vad krävs för att gå från PoC till produktion** — styrning, drift, kostnad, risk?

Fråga 3 och 4 är de svåra. Fråga 1 och 2 är förarbetet.

## Karta över repot

| Katalog | Innehåll |
|---|---|
| [docs/00-oversikt/](docs/00-oversikt/) | Vision, ordlista, mognadstrappa PoC → produktion |
| [docs/10-anvandningsfall/](docs/10-anvandningsfall/) | Användningsfall från verksamheten, avidentifierade |
| [docs/20-tekniker/](docs/20-tekniker/) | En sida per AI-teknik: vad den är, när den passar, vad den kostar |
| [docs/30-experiment/](docs/30-experiment/) | Labbloggar. Ett experiment = en fil = ett svar |
| [docs/40-matchning/](docs/40-matchning/) | Matrisen: vilken teknik löser vilket användningsfall |
| [docs/50-fran-poc-till-produktion/](docs/50-fran-poc-till-produktion/) | Checklistor, styrning, drift, kostnad |
| [docs/60-miljo/](docs/60-miljo/) | Labbmiljön: SSP Cloud/Onyxia, Open WebUI, verktyg, git-auth |
| [minnesbank/](minnesbank/) | Det **delade** minnet — vårt viktigaste experiment |
| [exempel/](exempel/) | Körbar kod: MCP-server, skills |
| [verktyg/](verktyg/) | Skript för att sätta upp och starta saker i labbet |

[AGENTS.md](AGENTS.md) är instruktionerna AI-verktyg läser när de jobbar i repot.
Läsvärd även för människor — konventionerna är desamma.

## Kom igång

```bash
git clone https://github.com/jakobengdahl/ArkAI.git
cd ArkAI
./verktyg/kontrollera-miljo.sh     # vad finns, vad saknas
```

Kör du i SSP Cloud? Börja med [docs/60-miljo/README.md](docs/60-miljo/README.md).
Där står också de tre sakerna som brukar överraska i miljön.

Ny och vill läsa dig in? [docs/README.md](docs/README.md) har en läsordning.

## Arbetssätt

Vi jobbar i små, avgränsade experiment. Ett experiment ska gå att göra på en
förmiddag och ska sluta med ett skrivet svar — även när svaret är "det här funkade
inte". Negativa resultat är billigare att läsa än att upprepa.

Lärdomen som nästa person behöver *innan* de börjar hör hemma i
[minnesbanken](minnesbank/), inte bara i experimentfilen. Det är den delen som gör
skillnad på ett repo och ett gemensamt minne.

Se [BIDRA.md](BIDRA.md) för hur du lägger till något.

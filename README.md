# ArkAI

En öppen experimentyta för att lära oss vad AI faktiskt kan göra i vårt arbete med
arkitektur — och vad som krävs för att ta det hela vägen från demo till drift.

Vi arbetar i en offentlig myndighet med statistikproduktion: insamling, bearbetning
och analys av data som blir faktabaserat beslutsunderlag för samhället. Processerna
följer i stora drag [GSBPM](https://statswiki.unece.org/display/GSBPM), vilket gör
dem ovanligt väl beskrivna — och därmed ovanligt tacksamma att resonera om när man
ska avgöra var AI faktiskt hjälper. Det vi gör här rör inte kärnverksamheten och
inga riktiga data.

Repot är **publikt**. Läs [RIKTLINJER-INNEHALL.md](RIKTLINJER-INNEHALL.md) innan du
skriver något här. Kort version: inga interna detaljer om system eller personer,
inga riktiga data, inga hemligheter. Att beskriva vilken sorts arbete vi gör är
däremot både tillåtet och nödvändigt — annars går det inte att bedöma om ett
användningsfall är relevant.

## Vad vi försöker ta reda på

1. **Vilka användningsfall** i vårt arbete tjänar på AI — och vilka gör det inte?
2. **Vilka AI-tekniker** finns, och vad är de faktiskt bra på?
   (chattbot + verktyg via MCP/CLI, minnesbanker, kodagenter, skills, RAG, grafer …)
3. **Hur matchar man rätt teknik mot rätt användningsfall?**
4. **Vad krävs för att gå från PoC till produktion** — styrning, drift, kostnad, risk?

Fråga 3 och 4 är de svåra. Fråga 1 och 2 är förarbetet.

Arbetet ska ge tre saker: kompetens som sitter i händerna, en karta över vilken
teknik olika slags fall kräver, och ett språk som håller i ett verksamhetsmöte. Se
[vision-och-mal.md](docs/00-oversikt/vision-och-mal.md).

Vi arbetar i **två spår**: vad vi själva ansvarar för, som kan gå hela vägen, och
utblickar mot verksamhet andra ansvarar för, där resultatet är ett underlag att ta
vidare tillsammans med dem — inte en lösning. Styrningen som gäller runtomkring finns
sammanfattad i [forutsattningar.md](docs/00-oversikt/forutsattningar.md).

## Karta över repot

| Katalog | Innehåll |
|---|---|
| [docs/00-oversikt/](docs/00-oversikt/) | Vision, ordlista, mognadstrappa PoC → produktion |
| [docs/10-anvandningsfall/](docs/10-anvandningsfall/) | Användningsfall från verksamheten, avidentifierade |
| [docs/20-tekniker/](docs/20-tekniker/) | En sida per AI-teknik: vad den är, när den passar, vad den kostar |
| [docs/30-experiment/](docs/30-experiment/) | Labbloggar. Ett experiment = en fil = ett svar |
| [docs/40-matchning/](docs/40-matchning/) | Matrisen: vilken teknik löser vilket användningsfall |
| [docs/50-fran-poc-till-produktion/](docs/50-fran-poc-till-produktion/) | Checklistor, styrning, drift, kostnad |
| [docs/60-miljo/](docs/60-miljo/) | Labbmiljön: SSP Cloud/Onyxia, Eneo, Open WebUI, verktyg, git-auth |
| [minnesbank/](minnesbank/) | Det **delade** minnet — vårt viktigaste experiment |
| [exempel/](exempel/) | Körbar kod: MCP-server, skills |
| [verktyg/](verktyg/) | Panelen, startskripten och katalogen över det som går att köra |

[AGENTS.md](AGENTS.md) är instruktionerna AI-verktyg läser när de jobbar i repot.
Läsvärd även för människor — konventionerna är desamma.

## Kom igång

Labbet körs i SSP Cloud och startas med en **URL** som har alla inställningar
förifyllda — port, minne, startskript, hemligheter. Se
[docs/60-miljo/starta-labbet.md](docs/60-miljo/starta-labbet.md).

När miljön är uppe installerar den sig själv i ett synligt terminalfönster, och
**labbpanelen** öppnas i VS Code: repots dokumentation renderad, plus knappar för
att installera och starta tjänster. Se
[docs/60-miljo/panelen.md](docs/60-miljo/panelen.md).

Utanför SSP Cloud, eller om du hellre skriver kommandon:

```bash
git clone https://github.com/jakobengdahl/ArkAI.git
cd ArkAI
./verktyg/labb-start.sh            # installerar grunden och startar panelen
./verktyg/kor.sh lista             # vad som går att köra
```

Ny och vill läsa dig in? [docs/README.md](docs/README.md) har en läsordning.

## Arbetssätt

Vi jobbar i små, avgränsade experiment. Ett experiment ska gå att göra på en
förmiddag och ska sluta med ett skrivet svar — även när svaret är "det här funkade
inte". Negativa resultat är billigare att läsa än att upprepa.

Lärdomen som nästa person behöver *innan* de börjar hör hemma i
[minnesbanken](minnesbank/), inte bara i experimentfilen. Det är den delen som gör
skillnad på ett repo och ett gemensamt minne.

Se [BIDRA.md](BIDRA.md) för hur du lägger till något.

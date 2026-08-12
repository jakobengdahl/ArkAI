# Open WebUI i labbmiljön

Open WebUI är ett chattgränssnitt som kan prata med flera modellbackends (OpenAI-
kompatibla API:er, Ollama) och som har inbyggt stöd för dokumentuppladdning, RAG,
verktygsanrop och flera användare. Vi använder det som **testbänk för chattbot-
upplägg**: hur känns det när en chattbot får tillgång till underliggande funktioner,
och hur mycket av upplevelsen sitter i gränssnittet snarare än i modellen?

Version som testats: **0.11.0**, installerad med `uv` under Python 3.11.

## Installation

Open WebUI finns **inte** i Onyxias katalog, och du kan inte köra containrar i
podden (ingen Docker, inga k8s-rättigheter). Vi installerar det som ett
Python-verktyg i VS Code-tjänsten i stället.

```bash
uv python install 3.11                       # kräver 3.11, imagen har 3.13
uv tool install --python 3.11 open-webui
export PATH="$HOME/.local/bin:$PATH"         # lägg i ~/.bashrc
```

Installationen tar några minuter och drar in en hel del beroenden. Den hamnar under
`~/.local`, alltså på den persistenta volymen, och överlever omstarter.

## Starta

```bash
./verktyg/starta-openwebui.sh --bakgrund
```

Skriptet läser `.env` (kopiera från `.env.example`), skapar datakatalogen och väntar
tills tjänsten svarar. Första starten tar ~40 sekunder extra eftersom en
embeddingmodell laddas ner.

Stoppa med `./verktyg/starta-openwebui.sh --stoppa`.

**Port 8080 går inte att använda** — code-server sitter där. Standard i skripten är
`8081`.

## Nå gränssnittet

### Rekommenderat: egen ingress

När du startar VS Code-tjänsten i Onyxia, gå till **Network access** och slå på
*"Enable access to your service through specific ports"* med porten `8081`. Tjänsten
får då en egen URL vid sidan av VS Code-URL:en.

Inställningen går bara att sätta vid start. Har du redan en tjänst igång får du
starta om den — hemkatalogen är persistent, så du tappar inget arbete.

### Nödutgång: code-servers proxy

Glömde du porten och vill inte starta om? code-server har en inbyggd proxy:

```
https://<din-vscode-url>/proxy/8081/
```

Den fungerar eftersom du redan är inloggad i code-server i webbläsaren. Var
beredd på att den kan bråka med Open WebUI:s statiska filer och WebSocket-anslutning
— gränssnittet är byggt för att ligga i roten av en domän. Fungerar det inte, prova
`/absproxy/8081/`. Fungerar inte det heller: starta om tjänsten med rätt portinställning.

## Konfiguration

Allt sätts via miljövariabler, lämpligast i `.env`:

| Variabel | Kommentar |
|---|---|
| `OPEN_WEBUI_PORT` | 8081 som standard |
| `DATA_DIR` | Var databas och uppladdningar hamnar. Gitignorerad. |
| `WEBUI_AUTH` | `False` hoppar över inloggning. Bara okej medan du är ensam användare. |
| `WEBUI_SECRET_KEY` | Sätt en gång (`openssl rand -hex 32`) och behåll — annars loggas alla ut vid omstart. |
| `ENABLE_OPENAI_API` / `OPENAI_API_BASE_URL` | Peka mot valfri OpenAI-kompatibel endpoint |
| `ENABLE_OLLAMA_API` / `OLLAMA_BASE_URL` | Om du kör en lokal modell |

Sätt `WEBUI_AUTH=True` så snart en kollega ska nå din instans. Ingressen är
åtkomlig för fler än dig.

## Vad vi vill testa här

Det här är poängen med att ha Open WebUI i labbet — inte att ha en chattbot, utan
att kunna variera upplägget och känna skillnaden:

1. **Chattbot + verktyg.** Koppla in våra egna funktioner och se var gränsen går
   mellan "modellen svarar" och "modellen gör". Se
   [20-tekniker/chattbot-plus-verktyg.md](../20-tekniker/chattbot-plus-verktyg.md).
2. **Kunskap kontra minne.** Open WebUI:s dokumentuppladdning ger RAG. Det är inte
   samma sak som en minnesbank. Att ställa dem mot varandra i samma gränssnitt gör
   skillnaden konkret — se [20-tekniker/minnesbank.md](../20-tekniker/minnesbank.md).
3. **Delad instans kontra egen.** Vad händer med kvaliteten när flera personer
   delar samma kunskapsbas i stället för att var och en laddar upp sina egna filer?
4. **Modellbyte.** Samma prompt, samma verktyg, olika modell. Hur mycket av
   resultatet sitter i modellvalet?

## Kända begränsningar i den här miljön

- Ingen container-körning i podden — Open WebUI:s funktioner som förutsätter Docker
  (t.ex. kodexekvering i sandlåda) fungerar inte.
- Tjänsten dör när podden startas om. `DATA_DIR` ligger persistent, så data finns
  kvar, men du måste starta om processen manuellt.
- Ingen inloggning mot SSP Clouds Keycloak är uppsatt. Kör med `WEBUI_AUTH=True` och
  lokala konton om fler ska in, och behandla instansen som ett labb — inte som något
  att lägga verkligt innehåll i.

## Alternativ värt att jämföra med

**[Eneo](https://eneo.ai/)** är en svensk, offentligt utvecklad AI-plattform med
uttalat fokus på offentlig sektor. Den är intressant som jämförelse just för att
frågorna den försöker lösa — förvaltning, behörigheter, spårbarhet, upphandlingsbarhet
— är precis de frågor som avgör om något går från PoC till produktion hos oss.

Open WebUI är snabbare att komma igång med och bättre för att förstå *tekniken*.
Lägg upp jämförelsen som ett eget experiment när grunderna sitter, och håll isär
"vad kan verktyget" från "vad krävs för att förvalta det".

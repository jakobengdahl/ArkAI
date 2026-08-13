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
verktyg/kor.sh installera openwebui
```

eller, om du hellre ser vad som händer:

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

### Tjänsten måste lyssna på poddens adress, inte bara på loopback

Startskriptet binder till `0.0.0.0`. Det är inte slarv: Onyxias portexponering
går via en Kubernetes-Service som når podden på dess **pod-IP**. En process som
bara lyssnar på `127.0.0.1` svarar då `502` genom ingressen, hur rätt allt annat
än är. Verifierat 2026-08-13 — `curl http://$(hostname -i):8081/health` ska svara
`200`, inte bara loopback-adressen.

Följden är att alla i namnrymden når instansen. Sätt `WEBUI_AUTH=True` i `.env`
innan du exponerar porten.

### Enda vägen som fungerar: egen ingress

När du startar VS Code-tjänsten i Onyxia, gå till **Network access** och slå på
*"Enable access to your service through specific ports"* med porten `8081`. Tjänsten
får då en egen URL — ett eget värdnamn där Open WebUI ligger i roten, vilket är vad
den kräver.

Inställningen går **bara** att sätta när tjänsten startar. Har du redan en tjänst
igång får du starta om den. Hemkatalogen är persistent, så du tappar inget arbete —
installationen och `DATA_DIR` finns kvar.

URL:en visas i Onyxia på tjänstens sida efter start.

### code-servers proxy fungerar inte — och kan inte fås att fungera

Det är frestande att tro att man kan slippa omstarten via code-servers inbyggda
proxy:

```
https://<din-vscode-url>/proxy/8081/      # ger en trasig sida
https://<din-vscode-url>/absproxy/8081/   # likaså
```

Det gör man inte. Verifierat 2026-08-12 med Open WebUI 0.11.0:

- Gränssnittet refererar allt med **absoluta sökvägar** — `/_app/immutable/...` för
  JavaScript och CSS, `/api/...` för anropen.
- `/proxy/<port>/` strippar prefixet innan anropet går vidare, så Open WebUI vet inte
  att den ligger under en sökväg och svarar med rotabsoluta sökvägar. Webbläsaren
  löser dem mot domänroten och träffar code-server i stället.
- Paketet har **inget stöd för bassökväg**. `root_path`, `BASE_PATH` eller
  motsvarande finns inte någonstans i koden, så det går inte att konfigurera bort.
  Sökvägarna är dessutom inbyggda i SvelteKit-bygget, inte genererade vid körning.
- `/absproxy/` skickar med hela sökvägen men löser inget, eftersom appen ändå inte
  kan hantera prefixet.

Det finns alltså ingen inställning att leta efter. Starta om tjänsten med
portexponeringen.

### Om du inte vill starta om just nu

Instansen fungerar utmärkt från terminalen — API:et bryr sig inte om sökvägar:

```bash
curl -s http://127.0.0.1:8081/health
curl -s http://127.0.0.1:8081/api/config | jq '{name, version}'
```

Och för att bara *chatta* finns plattformens centrala instans på
[llm.lab.sspcloud.fr](sspcloud-llm.md), som redan ligger i roten av sitt eget
värdnamn. Din egen instans behövs när du vill variera upplägget — inte för att
prata med en modell.

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

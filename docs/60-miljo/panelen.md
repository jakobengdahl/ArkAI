# Labbpanelen

Panelen är repots dokumentation renderad, plus knappar för det som går att köra.
Den finns för att man inte ska behöva kunna VS Code, terminalen och Onyxia för att
komma igång — men den tar inte bort något av det. Allt panelen gör går att göra
från terminalen, med samma kommandon.

Öppna den i VS Code:

```
Ctrl+Shift+P → "Simple Browser: Show" → klistra in panelens URL
```

URL:en skrivs ut när panelen startar. Den ser ut som
`https://<din-vscode-url>/proxy/8082/`.

## Två regler som förklarar allt annat

**Markdown är master.** Panelen har inget eget innehåll. Den renderar `.md`-filerna
som ligger i repot, och samma filer går att läsa på GitHub. Hittar du ett fel i
panelen rättar du filen, inte panelen.

**Inga absoluta sökvägar.** All navigering sker via query-strängen (`?sida=…`) och
all CSS ligger inline i sidan. Det är därför panelen fungerar oförändrad både på
`127.0.0.1:8082` och bakom code-servers `/proxy/8082/` — till skillnad från
Open WebUI, som antar att den ligger i roten av ett värdnamn och därför kräver en
egen ingress. Se
[minnesbanken](../../minnesbank/verktyg/spa-fungerar-inte-bakom-sokvagsproxy.md).

Konsekvensen är praktisk: panelen behöver ingen portexponering och inget omstart av
tjänsten. Den binder till `127.0.0.1` och kan bara nås av den som har den här
VS Code-sessionen — vilket är hela behörighetsmodellen för något som kan starta
processer.

## Vad du kan göra i den

| I panelen | I terminalen |
|---|---|
| Läsa dokumentationen med navigering | `less docs/…` |
| Se vad som är installerat och vad som kör | `verktyg/kor.sh status` |
| Installera och starta en tjänst | `verktyg/kor.sh installera openwebui` |
| Köra igång en hel uppsättning | `verktyg/kor.sh uppsattning chatt-med-verktyg` |
| Köra en åtgärd | `verktyg/kor.sh atgard koppla-openwebui` |
| Följa en installationslogg | `tail -f ~/work/.labb/logg/*.log` |
| Se tjänster som kör i namnrymden | `kubectl get ingress` |

Panelen anropar `verktyg/kor.sh`. Det är samma väg som terminalen använder, vilket
är avsiktligt: en installation du startade i terminalen låser knappen i panelen,
och tvärtom.

## Knapparna vet vad som redan pågår

Panelen gissar aldrig ett tillstånd — den sonderar det, varje gång sidan laddas:

| Vad panelen tittar på | Vad den drar för slutsats |
|---|---|
| Håller någon låset i `~/work/.labb/las/`? | **arbetar** — knappen blir "visa vad som händer" |
| Svarar hälsokontrollen eller porten? | **kör** — knappen blir "öppna" och "stoppa" |
| Lyckas `finns`-kommandot i manifestet? | **installerad** — knappen blir "starta" |
| Annars | **ej installerad** — knappen blir "installera" |

Därför spelar det ingen roll att en pod-omstart dödar alla processer men lämnar
kvar filerna: panelen påstår inte att något kör bara för att det gjorde det förut.

Låsen är av två slag, vilket är lätt att göra fel. `kor.sh` tar ett **exklusivt**
lås medan den arbetar; panelens avläsning tar ett **delat**. Två avläsningar stör
alltså inte varandra, medan en verklig körning syns för båda.

Ett delat lås utesluter ändå ett exklusivt under de mikrosekunder avläsningen
tar. Därför väntar `kor.sh` i två sekunder på låset i stället för att ge upp
direkt — annars kunde en sidladdning i olyckligt ögonblick få en installation
att svara "något körs redan".

## Vad panelen litar på

Manifestet är körbar kod. `finns`-kommandot körs varje gång en sida renderas, och
`installera`/`starta`/`stoppa` körs när du trycker på en knapp. Den som kan ändra
`verktyg/labb.toml` kan alltså köra kommandon i din miljö — och startskriptet
hämtar dessutom repots `main` direkt från GitHub.

Det är avsiktligt och ofrånkomligt för ett labb som ska kunna installera saker,
men det betyder att **`main` i det här repot är betrodd kod**. Granska ändringar i
`verktyg/` som om de gällde ett skript du kör som dig själv, för det är vad de är.
`.env` och annat som `.gitignore` täcker går däremot inte att läsa genom panelen.

## Lägga till en tjänst

Allt panelen vet står i [`verktyg/labb.toml`](../../verktyg/labb.toml). Lägg till
en tjänst där — inte i koden:

```toml
[tjanst.mittverktyg]
namn = "Mitt verktyg"
beskrivning = "En rad om vad det är bra för."
dok = "docs/20-tekniker/min-teknik.md"
typ = "lokal"            # lokal = process här, fjarr = kör någon annanstans,
                         # verktyg = stdio, startas av klienten
steg = "begaran"         # auto = installeras vid uppstart
port = 8084
finns = "command -v mittverktyg"
installera = "verktyg/installera/mittverktyg.sh"
starta = "verktyg/starta-mittverktyg.sh --bakgrund"
stoppa = "verktyg/starta-mittverktyg.sh --stoppa"
halsa = "http://127.0.0.1:8084/health"
```

En **uppsättning** är flera tjänster som ska fungera ihop:

```toml
[uppsattning.mitt-experiment]
namn = "Mitt experiment"
beskrivning = "Vad kombinationen är till för."
tjanster = ["openwebui", "mittverktyg", "mcpo"]
dok = "docs/30-experiment/EXP-00N-mitt-experiment.md"
```

## Dynamiska block i markdown

Panelen expanderar HTML-kommentarer när den renderar. På GitHub syns de inte alls,
vilket är poängen — markdownfilen förblir läsbar på båda ställena.

| Block | Vad det blir |
|---|---|
| `<!-- panel:uppsattningar -->` | Kort med "kör igång"-knappar |
| `<!-- panel:tjanster -->` | Kort per tjänst med status och knappar |
| `<!-- panel:atgarder -->` | Kort med knappar för sådant som inte är en tjänst |
| `<!-- panel:status -->` | Tabell över det som kör |
| `<!-- panel:miljo -->` | Verktyg, namnrymd, hur tjänsten startades |
| `<!-- panel:namnrymd -->` | Ingresser i namnrymden, som klickbara adresser |

## Åtgärder

Vissa saker ska gå att köra med en knapp utan att vara en tjänst — de har inget
tillstånd, de bara utförs. Just nu en: att koppla in modellen och
verktygsservrarna i Open WebUI, som är användbar när man installerat en ny
MCP-server.

De deklareras som `[atgard.<id>]` i [`verktyg/labb.toml`](../../verktyg/labb.toml):

```toml
[atgard.koppla-openwebui]
namn = "Koppla in modell och verktyg i Open WebUI"
beskrivning = "..."
knapp = "Koppla in"
kommando = "verktyg/konfigurera-openwebui.py --skriv"
dok = "docs/60-miljo/openwebui.md"
```

De går genom samma `kor.sh`, tar samma lås och skriver samma sorts logg som
tjänsterna. Id:n delar namnrymd med tjänsterna, så återanvänd inte ett id.

## Starta och stoppa panelen

```bash
verktyg/starta-panelen.sh --bakgrund
verktyg/starta-panelen.sh --stoppa
verktyg/starta-panelen.sh              # förgrunden, eller följ loggen om den redan kör
```

Normalt behöver du inte göra något av det — panelen startas av
[startskriptet](starta-labbet.md) när tjänsten startar.

## Var saker ligger

Allt panelen skriver hamnar i `~/work/.labb/`, utanför repot:

```
~/work/.labb/
  miljo.toml        hur tjänsten startades: profil, tidpunkt, namnrymd
  mcp.json          delad MCP-konfiguration, genererad ur labb.toml
  logg/             en logg per tjänst och handling
                    panel-kor.log = panelens egen, för fel som inträffar
                    innan kor.sh hunnit skriva tjänstens logg
  las/              låsfiler — det är dessa som gör knapparna säkra
  status/           anteckning om senaste körningen
```

Att det ligger utanför repot är medvetet: ingenting som skrivs där kan råka
commitas, och `git clean` tar inte bort din installationshistorik.
